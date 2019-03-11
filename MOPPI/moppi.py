# -*- coding: utf-8 -*-
#-----------------------------------------------------------
#
# MOPPI
# Copyright Serge Lhomme
# EMAIL: serge.lhomme (at) u-pec.fr
# WEB  : http://sergelhomme.fr/
#
# Extension permettant de préparer la mobilité du personnel en période d'inondation
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from PyQt4 import QtXml
from qgis.gui import *

import os
import sys
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
import networkx as nx
import numpy as np
import urllib.request
import requests
import math
from scipy.cluster.vq import kmeans, vq
from scipy.cluster.hierarchy import linkage, fcluster
import random
import copy
import time

from dialoggeocodage import DialogGeocodage
from dialoggeocodagelay  import DialogGeocodageLay
from dialoggeocodageinfo import DialogGeocodageInfo
from dialogdistancierlay  import DialogDistancierLay
from dialogdistancierinfo  import DialogDistancierInfo
from dialogdistancierinfotm  import DialogDistancierInfoTM
from dialogdistancierinfoshp  import DialogDistancierInfoShp
from dialogdistancierinfoshp2  import DialogDistancierInfoShp2

from dialogclustering import DialogClustering
from dialogclustinfo import DialogClustInfo

from dialogoptim import DialogOptim
from dialogoptiminfo import DialogOptimInfo

class Moppi:

	def __init__(self, iface):
		self.iface = iface

	def initGui(self):
		self.action = QAction("Geocodage", self.iface.mainWindow())
		QObject.connect(self.action, SIGNAL("activated()"), self.run)
		self.actionb = QAction("Clustering", self.iface.mainWindow())
		QObject.connect(self.actionb, SIGNAL("activated()"), self.runclust)
		self.actionc = QAction("Optimisation", self.iface.mainWindow())
		QObject.connect(self.actionc, SIGNAL("activated()"), self.runoptim)

		self.iface.addPluginToMenu("&MOPPI...", self.action)
		self.iface.addPluginToMenu("&MOPPI...", self.actionb)
		self.iface.addPluginToMenu("&MOPPI...", self.actionc)

	def unload(self):
		self.iface.removePluginMenu("&MOPPI...",self.action)
		self.iface.removePluginMenu("&MOPPI...",self.actionb)
		self.iface.removePluginMenu("&MOPPI...",self.actionc)

  #----------------------------------------------------------------------------------------------------------------------------------------                 Geocodage            -----------------------------------------------------------------------------------------------------------------------------------
	def run(self):
		global canvas
		canvas = self.iface.mapCanvas()
		global allLayers
		allLayers = canvas.layers()
		global count
		count = canvas.layerCount()
		global lay
		lay = []
		for i in allLayers:
			lay = lay + [str(i.name())]
		self.dlg = DialogGeocodage(self.iface.mainWindow())
		self.dlg.ui.comboBox.addItems(['Geocodage', 'Distancier'])
		self.dlg.ui.buttonBox.accepted.connect(self.geocodchoice)
		self.dlg.show()

	def geocodchoice(self):
		tool = self.dlg.ui.comboBox.currentText()
		if tool == 'Geocodage' :
			self.dlg2 = DialogGeocodageLay(self.iface.mainWindow())
			self.dlg2.ui.comboBox.addItems(lay)
			self.dlg2.ui.buttonBox.accepted.connect(self.geocodinfo)
			self.dlg2.show()
		tool = self.dlg.ui.comboBox.currentText()
		if tool == 'Distancier' :
			self.dlg2 = DialogDistancierLay(self.iface.mainWindow())
			self.dlg2.ui.comboBox.addItems(lay)
			self.dlg2.ui.comboBoxb.addItems(lay)
			self.dlg2.ui.comboBoxc.addItems(["One Mode (Voiture)", "One Mode (TC)", "Two Modes"])
			self.dlg2.ui.comboBoxd.addItems(["Shapefiles", "API"])
			self.dlg2.ui.buttonBox.accepted.connect(self.distancierinfo)
			self.dlg2.show()

	def geocodinfo(self):
		table = self.dlg2.ui.comboBox.currentText()
		for j in range(count):
			if str(table) == str(lay[j]) :
				ind = j
		global aLayer
		aLayer = allLayers[int(ind)]
		global provider
		provider = aLayer.dataProvider()
		global field
		field = provider.fields()
		global fields
		fields = []
		for i in range(field.count()):
			fields = fields+[str(field[i].name())]
		fields2 = [""] + fields
		self.dlg3 = DialogGeocodageInfo(self.iface.mainWindow())
		self.dlg3.ui.comboBox.addItems(fields2)
		self.dlg3.ui.comboBox2.addItems(fields2)
		self.dlg3.ui.comboBox3.addItems(fields)
		self.dlg3.ui.comboBox4.addItems(fields)
		self.dlg3.ui.comboBox5.addItems(fields)
		self.dlg3.ui.buttonBox.accepted.connect(self.geocodcal)
		self.dlg3.show()

	def geocodcal(self):
		street = self.dlg3.ui.comboBox.currentText()
		postalc = self.dlg3.ui.comboBox2.currentText()
		namel = self.dlg3.ui.comboBox3.currentText()
		id = self.dlg3.ui.comboBox4.currentText()
		met = self.dlg3.ui.comboBox5.currentText()
		if str(street) != "":
			Idstreet = provider.fieldNameIndex(str(street))
		else :
			Idstreet = 99999999
		if str(postalc) != "":
			Idpostalc = provider.fieldNameIndex(str(postalc))
		else :
			Idpostalc = 99999999
		Idnamel = provider.fieldNameIndex(str(namel))
		Idid = provider.fieldNameIndex(str(id))
		Idmet = provider.fieldNameIndex(str(met))
		attrs = []
		tabadrr = []
		tabid = []
		feat = QgsFeature()
		fit1 = provider.getFeatures()
		i = 0
		while fit1.nextFeature(feat):
			attrs = attrs + [feat.attributes()]
			adrr = ""
			if Idstreet != 99999999 :
				adrr = adrr + str(feat.attributes()[Idstreet]) + ","
			if Idpostalc != 99999999 :
				adrr = adrr + str(feat.attributes()[Idpostalc])+ ","
			adrr = adrr + str(feat.attributes()[Idnamel])
			tabadrr = tabadrr + [adrr]
			tabid = tabid + [[int(feat.attributes()[Idid]), int(feat.attributes()[Idmet])]]
		prb_err = []
		crsSrc = QgsCoordinateReferenceSystem(4326)
		crsDest = QgsCoordinateReferenceSystem(2154)
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		vln = QgsVectorLayer("Point?crs=epsg:2154", "Nodes", "memory")
		prn = vln.dataProvider()
		vln.startEditing()
		prn.addAttributes( [QgsField("ID", QVariant.Int), QgsField("Adresse", QVariant.String), QgsField("Long", QVariant.Double), QgsField("Lat", QVariant.Double), QgsField("Nbr", QVariant.Int), QgsField("Met", QVariant.Int)] )
		vln.commitChanges()
		for i in range(len(tabadrr)):
			req = "http://photon.komoot.de/api/?q="
			reqfin = str(req)+str(tabadrr[i])
			try :
				reqfin2 = reqfin.replace(" ","%20")
				f2 = urllib.request.urlopen(reqfin2)
				d2 = str(f2.read())
				lon = d2.split('coordinates":[')
				lon2 = lon[1].split(",")
				x = lon2[0]
				lat = lon2[1].split("]")
				y = lat[0]
				fet = QgsFeature()
				pointCRSdest = xform.transform(QgsPoint(float(x), float(y)))
				fet.setGeometry( QgsGeometry.fromPoint(pointCRSdest) )
				fet.setAttributes( [ int(tabid[i][0]) , str(tabadrr[i]), float(x), float(y), int(1), int(tabid[i][1]) ] )
				vln.startEditing()
				prn.addFeatures( [ fet ] )
				vln.commitChanges()
			except :
				prb_err = prb_err + [[tabid[i],tabadrr[i]]]
		if prb_err != []:
			testgeo, ok = QInputDialog.getItem(None," Message_Erreur : ","Vous avez " + str(len(prb_err)) + " erreurs de geocodage. Voulez-vous utiliser Google Map pour y remedier ? Il vous faut une clef API.", ["Non", "Oui"], editable = False)
			if ok :
				if str(testgeo) == "Non" :
					QMessageBox.information(None, " Message_Erreur : ", str(prb_err))
				if str(testgeo) == "Oui" :
					keycode, ok2 = QInputDialog.getText(None,"La clef", "La clef :", QLineEdit.Normal)
					if ok2 :
						prb_err2 = []
						for i in range(len(prb_err)):
							try :
								req = "https://maps.googleapis.com/maps/api/geocode/xml?address=" + str(prb_err[i][1])
								reqfin = str(req) + "&key=" + str(keycode)
								r = requests.get(str(reqfin))
								d2 = str(r.text)
								lat=d2.split("<lat>")
								lat2=lat[1].split("</lat>")
								y=lat2[0]
								lon=d2.split("<lng>")
								lon2=lon[1].split("</lng>")
								x=lon2[0]
								fet = QgsFeature()
								pointCRSdest = xform.transform(QgsPoint(float(x), float(y)))
								fet.setGeometry( QgsGeometry.fromPoint(pointCRSdest) )
								fet.setAttributes( [ int(prb_err[i][0]) , str(prb_err[i][1]), float(x), float(y), int(1), int(1) ] )
								vln.startEditing()
								prn.addFeatures( [ fet ] )
								vln.commitChanges()
							except :
								prb_err2 = prb_err2 + [[prb_err[i][0],prb_err[i][1]]]
						if len(prb_err2) > 0 :
							QMessageBox.information(None, " Message_Erreur : ", str(prb_err2))
		QgsMapLayerRegistry.instance().addMapLayer(vln)
		QMessageBox.information(None, " Message : ", "Thanks To Photon and OpenStreetMap")

	def distancierinfo(self):
		table_dep = self.dlg2.ui.comboBox.currentText()
		table_arr = self.dlg2.ui.comboBoxb.currentText()
		mod = self.dlg2.ui.comboBoxc.currentText()
		datares = self.dlg2.ui.comboBoxd.currentText()
		for j in range(count):
			if str(table_dep) == str(lay[j]) :
				ind = j
		global aLayer
		aLayer = allLayers[int(ind)]
		global provider
		provider = aLayer.dataProvider()
		global field
		field = provider.fields()
		global fields
		fields = []
		for i in range(field.count()):
			fields = fields+[str(field[i].name())]
		for j in range(count):
			if str(table_arr) == str(lay[j]) :
				ind = j
		global bLayer
		bLayer = allLayers[int(ind)]
		global providerb
		providerb = bLayer.dataProvider()
		global fieldb
		fieldb = providerb.fields()
		global fieldsb
		fieldsb = []
		for i in range(fieldb.count()):
			fieldsb = fieldsb+[str(fieldb[i].name())]
		if mod=="One Mode (Voiture)" and datares == "API" :
			self.dlg3 = DialogDistancierInfo(self.iface.mainWindow())
			self.dlg3.ui.comboBox.addItems(fields)
			self.dlg3.ui.comboBoxb.addItems(fields)
			self.dlg3.ui.comboBoxc.addItems(fields)
			self.dlg3.ui.comboBoxe.addItems(fields)
			self.dlg3.ui.comboBox2.addItems(fieldsb)
			self.dlg3.ui.comboBox2b.addItems(fieldsb)
			self.dlg3.ui.comboBox2c.addItems(fieldsb)
			self.dlg3.ui.comboBox2e.addItems(fieldsb)
			self.dlg3.ui.buttonBox.accepted.connect(self.distancierOMcarcal)
			self.dlg3.show()
		if mod=="One Mode (TC)" and datares == "API" :
			self.dlg3 = DialogDistancierInfo(self.iface.mainWindow())
			self.dlg3.ui.comboBox.addItems(fields)
			self.dlg3.ui.comboBoxb.addItems(fields)
			self.dlg3.ui.comboBoxc.addItems(fields)
			self.dlg3.ui.comboBoxe.addItems(fields)
			self.dlg3.ui.comboBox2.addItems(fieldsb)
			self.dlg3.ui.comboBox2b.addItems(fieldsb)
			self.dlg3.ui.comboBox2c.addItems(fieldsb)
			self.dlg3.ui.comboBox2e.addItems(fieldsb)
			self.dlg3.ui.buttonBox.accepted.connect(self.distancierOMtccal)
			self.dlg3.show()
		if mod=="Two Modes" and datares == "API" :
			self.dlg3 = DialogDistancierInfoTM(self.iface.mainWindow())
			self.dlg3.ui.comboBox.addItems(fields)
			self.dlg3.ui.comboBoxb.addItems(fields)
			self.dlg3.ui.comboBoxc.addItems(fields)
			self.dlg3.ui.comboBoxf.addItems(fields)
			self.dlg3.ui.comboBox2.addItems(fieldsb)
			self.dlg3.ui.comboBox2b.addItems(fieldsb)
			self.dlg3.ui.comboBox2c.addItems(fieldsb)
			self.dlg3.ui.comboBox2f.addItems(fieldsb)
			self.dlg3.ui.buttonBox.accepted.connect(self.distancierTMcal)
			self.dlg3.show()
		if mod=="One Mode (Voiture)" and datares == "Shapefiles" :
			t = u"La couche réseau : "
			Arc,ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
			if ok :
				t = u"La couche noeud associée : "
				Noeud,ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
				if ok :
					for j in range(count):
						if str(Arc) == str(lay[j]) :
							ind = j
					global cLayer
					cLayer = allLayers[int(ind)]
					global providerc
					providerc = cLayer.dataProvider()
					global fieldc
					fieldc = providerc.fields()
					global fieldsc
					fieldsc = []
					for i in range(fieldc.count()):
						fieldsc = fieldsc+[str(fieldc[i].name())]
					for j in range(count):
						if str(Noeud) == str(lay[j]) :
							ind = j
					global dLayer
					dLayer = allLayers[int(ind)]
					global providerd
					providerd = dLayer.dataProvider()
					global fieldd
					fieldd = providerd.fields()
					global fieldsd
					fieldsd = []
					for i in range(fieldd.count()):
						fieldsd = fieldsd+[str(fieldd[i].name())]
					self.dlg3 = DialogDistancierInfoShp(self.iface.mainWindow())
					self.dlg3.ui.comboBox.addItems(fields)
					self.dlg3.ui.comboBoxb.addItems(fieldsc)
					self.dlg3.ui.comboBoxc.addItems(fieldsc)
					self.dlg3.ui.comboBoxd.addItems(fields)
					self.dlg3.ui.comboBox2.addItems(fieldsb)
					self.dlg3.ui.comboBox2b.addItems(fieldsc)
					self.dlg3.ui.comboBox2c.addItems(fieldsd)
					self.dlg3.ui.comboBox2d.addItems(fieldsb)
					self.dlg3.ui.buttonBox.accepted.connect(self.distancierShpcarcal)
					self.dlg3.show()
		if mod=="One Mode (TC)" and datares == "Shapefiles" :
			t = u"La couche réseau : "
			Arc,ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
			if ok :
				t = u"La couche noeud associée : "
				Noeud,ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
				if ok :
					for j in range(count):
						if str(Arc) == str(lay[j]) :
							ind = j
					global cLayer
					cLayer = allLayers[int(ind)]
					global providerc
					providerc = cLayer.dataProvider()
					global fieldc
					fieldc = providerc.fields()
					global fieldsc
					fieldsc = []
					for i in range(fieldc.count()):
						fieldsc = fieldsc+[str(fieldc[i].name())]
					for j in range(count):
						if str(Noeud) == str(lay[j]) :
							ind = j
					global dLayer
					dLayer = allLayers[int(ind)]
					global providerd
					providerd = dLayer.dataProvider()
					global fieldd
					fieldd = providerd.fields()
					global fieldsd
					fieldsd = []
					for i in range(fieldd.count()):
						fieldsd = fieldsd+[str(fieldd[i].name())]
					self.dlg3 = DialogDistancierInfoShp(self.iface.mainWindow())
					self.dlg3.ui.comboBox.addItems(fields)
					self.dlg3.ui.comboBoxb.addItems(fieldsc)
					self.dlg3.ui.comboBoxc.addItems(fieldsc)
					self.dlg3.ui.comboBoxd.addItems(fields)
					self.dlg3.ui.comboBox2.addItems(fieldsb)
					self.dlg3.ui.comboBox2b.addItems(fieldsc)
					self.dlg3.ui.comboBox2c.addItems(fieldsd)
					self.dlg3.ui.comboBox2d.addItems(fieldsb)
					self.dlg3.ui.buttonBox.accepted.connect(self.distancierShptccal)
					self.dlg3.show()
		if mod=="Two Modes" and datares == "Shapefiles" :
			t = u"La couche réseau (Voiture) : "
			Arc, ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
			if ok :
				t = u"La couche noeud associée : "
				Noeud, ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
				if ok :
					for j in range(count):
						if str(Arc) == str(lay[j]) :
							ind = j
					global cLayer
					cLayer = allLayers[int(ind)]
					global providerc
					providerc = cLayer.dataProvider()
					global fieldc
					fieldc = providerc.fields()
					global fieldsc
					fieldsc = []
					for i in range(fieldc.count()):
						fieldsc = fieldsc+[str(fieldc[i].name())]
					for j in range(count):
						if str(Noeud) == str(lay[j]) :
							ind = j
					global dLayer
					dLayer = allLayers[int(ind)]
					global providerd
					providerd = dLayer.dataProvider()
					global fieldd
					fieldd = providerd.fields()
					global fieldsd
					fieldsd = []
					for i in range(fieldd.count()):
						fieldsd = fieldsd+[str(fieldd[i].name())]
					t = u"La couche réseau (TC) : "
					Arc2, ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
					if ok :
						t = u"La couche noeud associée : "
						Noeud2, ok = QInputDialog.getItem(None,"Reseau",t.encode('latin-1'), lay, editable = False)
						if ok :
							for j in range(count):
								if str(Arc2) == str(lay[j]) :
									ind = j
							global cLayer2
							cLayer2 = allLayers[int(ind)]
							global providerc2
							providerc2 = cLayer2.dataProvider()
							global fieldc2
							fieldc2 = providerc2.fields()
							global fieldsc2
							fieldsc2 = []
							for i in range(fieldc2.count()):
								fieldsc2 = fieldsc2+[str(fieldc2[i].name())]
							for j in range(count):
								if str(Noeud2) == str(lay[j]) :
									ind = j
							global dLayer2
							dLayer2 = allLayers[int(ind)]
							global providerd2
							providerd2 = dLayer2.dataProvider()
							global fieldd2
							fieldd2 = providerd2.fields()
							global fieldsd2
							fieldsd2 = []
							for i in range(fieldd2.count()):
								fieldsd2 = fieldsd2 + [str(fieldd2[i].name())]
							self.dlg3 = DialogDistancierInfoShp2(self.iface.mainWindow())
							self.dlg3.ui.comboBox.addItems(fields)
							self.dlg3.ui.comboBoxb.addItems(fieldsc)
							self.dlg3.ui.comboBoxc.addItems(fieldsc)
							self.dlg3.ui.comboBoxd.addItems(fieldsc2)
							self.dlg3.ui.comboBoxe.addItems(fieldsc2)
							self.dlg3.ui.comboBoxf.addItems(fields)
							self.dlg3.ui.comboBox2.addItems(fieldsb)
							self.dlg3.ui.comboBox2b.addItems(fieldsc)
							self.dlg3.ui.comboBox2c.addItems(fieldsd)
							self.dlg3.ui.comboBox2d.addItems(fieldsc2)
							self.dlg3.ui.comboBox2e.addItems(fieldsd2)
							self.dlg3.ui.comboBox2f.addItems(fieldsb)
							self.dlg3.ui.buttonBox.accepted.connect(self.distancierShpTMcal)
							self.dlg3.show()

	def distancierOMcarcal(self):
		idpers = self.dlg3.ui.comboBox.currentText()
		longpers = self.dlg3.ui.comboBoxb.currentText()
		latpers = self.dlg3.ui.comboBoxc.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		perslong = provider.fieldNameIndex(str(longpers))
		perslat = provider.fieldNameIndex(str(latpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		longeta = self.dlg3.ui.comboBox2b.currentText()
		lateta = self.dlg3.ui.comboBox2c.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		etalong = providerb.fieldNameIndex(str(longeta))
		etalat = providerb.fieldNameIndex(str(lateta))
		cle = str(self.dlg3.ui.lineedit.text())
		metpers = self.dlg3.ui.comboBoxe.currentText()
		metpersid = provider.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2e.currentText()
		metetaid = providerb.fieldNameIndex(str(meteta))
		feat = QgsFeature()
		fit = provider.getFeatures()
		tab1 = []
		tablemetpers = []
		while fit.nextFeature(feat):
			tab1 = tab1 + [[ int(feat.attributes()[persid]), float(feat.attributes()[perslong]), float(feat.attributes()[perslat]) ]]
			tablemetpers = tablemetpers + [int(feat.attributes()[metpersid])]
		fit = providerb.getFeatures()
		tab2 = []
		tablemeteta = []
		while fit.nextFeature(feat):
			tab2 = tab2 + [[ int(feat.attributes()[etaid]), float(feat.attributes()[etalong]), float(feat.attributes()[etalat]) ]]
			tablemeteta = tablemeteta + [int(feat.attributes()[metetaid])]
		crsSrc = QgsCoordinateReferenceSystem(4326)
		crsDest = QgsCoordinateReferenceSystem(2154)
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		vl = QgsVectorLayer("LineString?scr=epsg:2154", "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(len(tab1)):
			for j in range(len(tab2)):
				if tablemetpers[i] == tablemeteta[j] :
					adresse = "https://api.mapbox.com/directions/v5/mapbox/driving/"+str(tab1[i][1])+","+str(tab1[i][2])+";"+str(tab2[j][1])+","+str(tab2[j][2])+"?access_token="+str(cle)
					r = requests.get(str(adresse))
					d = str(r.text)
					t = d.split('duration":')
					t2 = t[1].split(',')
					res = t2[0]
					pointCRSdest = xform.transform(float(tab1[i][1]) , float(tab1[i][2]))
					pointCRSdest2 = xform.transform(float(tab2[j][1]) , float(tab2[j][2]))
					fet = QgsFeature()
					fet.setGeometry( QgsGeometry.fromPolyline([ pointCRSdest , pointCRSdest2 ]) )
					fet.setAttributes( [ int(tab1[i][0]), int(tab2[j][0]), float(res) ] )
					pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def distancierOMtccal(self):
		datet, ok = QInputDialog.getText(None, "Date",  "Date et heure de depart : ", QLineEdit.Normal, "20180223T082500")
		idpers = self.dlg3.ui.comboBox.currentText()
		longpers = self.dlg3.ui.comboBoxb.currentText()
		latpers = self.dlg3.ui.comboBoxc.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		perslong = provider.fieldNameIndex(str(longpers))
		perslat = provider.fieldNameIndex(str(latpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		longeta = self.dlg3.ui.comboBox2b.currentText()
		lateta = self.dlg3.ui.comboBox2c.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		etalong = providerb.fieldNameIndex(str(longeta))
		etalat = providerb.fieldNameIndex(str(lateta))
		cle = str(self.dlg3.ui.lineedit.text())
		metpers = self.dlg3.ui.comboBoxe.currentText()
		metpersid = provider.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2e.currentText()
		metetaid = providerb.fieldNameIndex(str(meteta))
		feat = QgsFeature()
		fit = provider.getFeatures()
		tab1 = []
		tablemetpers = []
		while fit.nextFeature(feat):
			tab1 = tab1 + [[ int(feat.attributes()[persid]), float(feat.attributes()[perslong]), float(feat.attributes()[perslat]) ]]
			tablemetpers = tablemetpers + [int(feat.attributes()[metpersid])]
		fit = providerb.getFeatures()
		tab2 = []
		tablemeteta = []
		while fit.nextFeature(feat):
			tab2 = tab2 + [[ int(feat.attributes()[etaid]), float(feat.attributes()[etalong]), float(feat.attributes()[etalat]) ]]
			tablemeteta = tablemeteta + [int(feat.attributes()[metetaid])]
		crsSrc = QgsCoordinateReferenceSystem(4326)
		crsDest = QgsCoordinateReferenceSystem(2154)
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		vl = QgsVectorLayer("LineString?scr=epsg:2154", "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(len(tab1)):
			for j in range(len(tab2)):
				if tablemetpers[i] == tablemeteta[j] :
					adresse = "https://api.navitia.io/v1/journeys?from="+str(tab1[i][1])+";"+str(tab1[i][2])+"&to="+str(tab2[j][1])+";"+str(tab2[j][2])+"&datetime="+str(datet)
					r = requests.get(str(adresse), auth=(str(cle), ''), verify=False)
					d = str(r.text)
					t = d.split('durations')
					t2 = t[1].split('"total":')
					t3 = t2[1].split(',')
					res = t3[0]
					pointCRSdest = xform.transform(float(tab1[i][1]) , float(tab1[i][2]))
					pointCRSdest2 = xform.transform(float(tab2[j][1]) , float(tab2[j][2]))
					fet = QgsFeature()
					fet.setGeometry( QgsGeometry.fromPolyline([ pointCRSdest , pointCRSdest2 ]) )
					fet.setAttributes( [ int(tab1[i][0]), int(tab2[j][0]), float(res) ] )
					pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def distancierTMcal(self):
		datet, ok = QInputDialog.getText(None, "Date",  "Date et heure de depart : ", QLineEdit.Normal, "20180223T082500")
		idpers = self.dlg3.ui.comboBox.currentText()
		longpers = self.dlg3.ui.comboBoxb.currentText()
		latpers = self.dlg3.ui.comboBoxc.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		perslong = provider.fieldNameIndex(str(longpers))
		perslat = provider.fieldNameIndex(str(latpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		longeta = self.dlg3.ui.comboBox2b.currentText()
		lateta = self.dlg3.ui.comboBox2c.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		etalong = providerb.fieldNameIndex(str(longeta))
		etalat = providerb.fieldNameIndex(str(lateta))
		cle = str(self.dlg3.ui.lineedit.text())
		cle2 = str(self.dlg3.ui.lineedit2.text())
		metpers = self.dlg3.ui.comboBoxf.currentText()
		metpersid = provider.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2f.currentText()
		metetaid = providerb.fieldNameIndex(str(meteta))
		feat = QgsFeature()
		fit = provider.getFeatures()
		tab1 = []
		tablemetpers = []
		while fit.nextFeature(feat):
			tab1 = tab1 + [[ int(feat.attributes()[persid]), float(feat.attributes()[perslong]), float(feat.attributes()[perslat]) ]]
			tablemetpers = tablemetpers + [int(feat.attributes()[metpersid])]
		fit = providerb.getFeatures()
		tab2 = []
		tablemeteta = []
		while fit.nextFeature(feat):
			tab2 = tab2 + [[ int(feat.attributes()[etaid]), float(feat.attributes()[etalong]), float(feat.attributes()[etalat]) ]]
			tablemeteta = tablemeteta + [int(feat.attributes()[metetaid])]
		crsSrc = QgsCoordinateReferenceSystem(4326)
		crsDest = QgsCoordinateReferenceSystem(2154)
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		vl = QgsVectorLayer("LineString?scr=epsg:2154", "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Tps_Voit", QVariant.Double) ] )
		pr.addAttributes( [ QgsField("Tps_Tc", QVariant.Double) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(len(tab1)):
			for j in range(len(tab2)):
				if tablemetpers[i] == tablemeteta[j] :
					adresse = "https://api.mapbox.com/directions/v5/mapbox/driving/"+str(tab1[i][1])+","+str(tab1[i][2])+";"+str(tab2[j][1])+","+str(tab2[j][2])+"?access_token="+str(cle)
					r = requests.get(str(adresse))
					d = str(r.text)
					t = d.split('duration":')
					t2 = t[1].split(',')
					res = t2[0]
					adresse = "https://api.navitia.io/v1/journeys?from="+str(tab1[i][1])+";"+str(tab1[i][2])+"&to="+str(tab2[j][1])+";"+str(tab2[j][2])+"&datetime="+str(datet)
					r = requests.get(str(adresse), auth=(str(cle2), ''))
					d = str(r.text)
					t = d.split('durations')
					t2 = t[1].split('"total":')
					t3 = t2[1].split(',')
					res2 = t3[0]
					if res <= res2 :
						mini = res
					else :
						mini = res2
					pointCRSdest = xform.transform(float(tab1[i][1]) , float(tab1[i][2]))
					pointCRSdest2 = xform.transform(float(tab2[j][1]) , float(tab2[j][2]))
					fet = QgsFeature()
					fet.setGeometry( QgsGeometry.fromPolyline([ pointCRSdest , pointCRSdest2 ]) )
					fet.setAttributes( [ int(tab1[i][0]), int(tab2[j][0]), float(res), float(res2), float(mini) ] )
					pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def distancierShpcarcal(self):
		vitesse = 20 * 1000 / float(3600)
		epsg = canvas.mapRenderer().destinationCrs().authid()
		idpers = self.dlg3.ui.comboBox.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		idstart = self.dlg3.ui.comboBoxb.currentText()
		startid = providerc.fieldNameIndex(str(idstart))
		idend = self.dlg3.ui.comboBox2b.currentText()
		endid = providerc.fieldNameIndex(str(idend))
		iddist = self.dlg3.ui.comboBoxc.currentText()
		distid = providerc.fieldNameIndex(str(iddist))
		idnoeud = self.dlg3.ui.comboBox2c.currentText()
		noeudid = providerd.fieldNameIndex(str(idnoeud))
		metpers = self.dlg3.ui.comboBoxd.currentText()
		metpersid = providerc.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2d.currentText()
		metetaid = providerd.fieldNameIndex(str(meteta))
		table = []
		feat = QgsFeature()
		fit = providerc.getFeatures()
		while fit.nextFeature(feat):
			attrsstart = feat.attributes()[int(startid)]
			attrsend = feat.attributes()[int(endid)]
			attrsdist = feat.attributes()[int(distid)]
			table = table+[(int(attrsstart), int(attrsend), float(attrsdist))]
		G = nx.Graph()
		G.add_weighted_edges_from(table)
		tableidpers = []
		tablemetpers = []
		affecpers = []
		distpers = []
		geompers = []
		for pt_feature in aLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geompers = geompers + [geom]
			pers = pt_feature.attributes()[persid]
			tableidpers = tableidpers + [int(pers)]
			met = pt_feature.attributes()[metpersid]
			tablemetpers = tablemetpers + [int(met)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = id
				if n == 0 :
					test = 1
					marge = marge + 50
			affecpers = affecpers + [int(idmin)]
			distpers = distpers + [float(math.sqrt(distmin))]
		tableideta = []
		tablemeteta = []
		affeceta = []
		disteta = []
		geometa = []
		for pt_feature in bLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geometa = geometa + [geom]
			eta = pt_feature.attributes()[etaid]
			tableideta = tableideta + [int(eta)]
			etab = pt_feature.attributes()[metetaid]
			tablemeteta = tablemeteta + [int(etab)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = id
				if n == 0 :
					test = 1
					marge = marge + 50
			affeceta = affeceta + [int(idmin)]
			disteta = disteta + [float(math.sqrt(distmin))]
		vl = QgsVectorLayer("LineString?scr=epsg:"+str(epsg), "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		vec = []
		for i in range(len(tableidpers)):
			for j in range(len(tableideta)):
				if tablemetpers[i] == tablemeteta[j] :
					try :
						dist = float(nx.shortest_path_length(G, affecpers[i], affeceta[j], weight='weight')) + ( distpers[i] / float(vitesse) ) + ( disteta[j] / float(vitesse) )
						vec = vec + [[tableidpers[i],tableideta[j],dist]]
					except :
						dist = 9999999999
						vec = vec + [[tableidpers[i],tableideta[j],dist]]
					fet = QgsFeature()
					fet.setGeometry( QgsGeometry.fromPolyline([ geompers[i] , geometa[j] ]) )
					fet.setAttributes( [ tableidpers[i], tableideta[j], dist ] )
					pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def distancierShptccal(self):
		vitesse = 10 * 1000 / float(3600)
		epsg = canvas.mapRenderer().destinationCrs().authid()
		idpers = self.dlg3.ui.comboBox.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		idstart = self.dlg3.ui.comboBoxb.currentText()
		startid = providerc.fieldNameIndex(str(idstart))
		idend = self.dlg3.ui.comboBox2b.currentText()
		endid = providerc.fieldNameIndex(str(idend))
		iddist = self.dlg3.ui.comboBoxc.currentText()
		distid = providerc.fieldNameIndex(str(iddist))
		idnoeud = self.dlg3.ui.comboBox2c.currentText()
		noeudid = providerd.fieldNameIndex(str(idnoeud))
		metpers = self.dlg3.ui.comboBoxd.currentText()
		metpersid = providerc.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2d.currentText()
		metetaid = providerd.fieldNameIndex(str(meteta))
		table = []
		feat = QgsFeature()
		fit = providerc.getFeatures()
		while fit.nextFeature(feat):
			attrsstart = feat.attributes()[int(startid)]
			attrsend = feat.attributes()[int(endid)]
			attrsdist = feat.attributes()[int(distid)]
			table = table + [(int(attrsstart), int(attrsend), float(attrsdist))]
		G = nx.Graph()
		G.add_weighted_edges_from(table)
		tableidpers = []
		tablemetpers = []
		affecpers = []
		distpers = []
		geompers = []
		for pt_feature in aLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geompers = geompers + [geom]
			pers = pt_feature.attributes()[persid]
			tableidpers = tableidpers + [int(pers)]
			met = pt_feature.attributes()[metpersid]
			tablemetpers = tablemetpers + [int(met)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = [int(id)]
					if dist == distmin :
						idmin = idmin + [int(id)]
				if n == 0 :
					test = 1
					marge = marge + 50
			affecpers = affecpers + [idmin]
			distpers = distpers + [float(math.sqrt(distmin))]
		tableideta = []
		tablemeteta = []
		affeceta = []
		disteta = []
		geometa = []
		for pt_feature in bLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geometa = geometa + [geom]
			eta = pt_feature.attributes()[etaid]
			tableideta = tableideta + [int(eta)]
			etab = pt_feature.attributes()[metetaid]
			tablemeteta = tablemeteta + [int(etab)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = [int(id)]
					if dist == distmin :
						idmin = idmin + [int(id)]
				if n == 0 :
					test = 1
					marge = marge + 50
			affeceta = affeceta + [idmin]
			disteta = disteta + [float(math.sqrt(distmin))]
		vl = QgsVectorLayer("LineString?scr=epsg:"+str(epsg), "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		vec = []
		for i in range(len(tableidpers)):
			for j in range(len(tableideta)):
				if tablemetpers[i] == tablemeteta[j] :
					d = 9999999999
					for k in range(len(affecpers[i])):
						for l in range(len(affeceta[j])):
							try :
								dcal = nx.shortest_path_length(G, affecpers[i][k], affeceta[j][l], weight='weight')
								if dcal < d :
									d = dcal
							except :
								"Do Nothing"
					if d == 9999999999 :
						dist = d
					else :
						dist = d + ( distpers[i] / float(vitesse) ) + ( disteta[j] / float(vitesse) )
					fet = QgsFeature()
					fet.setGeometry( QgsGeometry.fromPolyline([ geompers[i] , geometa[j] ]) )
					fet.setAttributes( [ tableidpers[i], tableideta[j], dist ] )
					pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def distancierShpTMcal(self):
		vitesse = 20 * 1000 / float(3600)
		epsg = canvas.mapRenderer().destinationCrs().authid()
		idpers = self.dlg3.ui.comboBox.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		ideta = self.dlg3.ui.comboBox2.currentText()
		etaid = providerb.fieldNameIndex(str(ideta))
		idstart = self.dlg3.ui.comboBoxb.currentText()
		startid = providerc.fieldNameIndex(str(idstart))
		idend = self.dlg3.ui.comboBox2b.currentText()
		endid = providerc.fieldNameIndex(str(idend))
		iddist = self.dlg3.ui.comboBoxc.currentText()
		distid = providerc.fieldNameIndex(str(iddist))
		idnoeud = self.dlg3.ui.comboBox2c.currentText()
		noeudid = providerd.fieldNameIndex(str(idnoeud))
		metpers = self.dlg3.ui.comboBoxf.currentText()
		metpersid = providerc.fieldNameIndex(str(metpers))
		meteta = self.dlg3.ui.comboBox2f.currentText()
		metetaid = providerd.fieldNameIndex(str(meteta))
		table = []
		feat = QgsFeature()
		fit = providerc.getFeatures()
		while fit.nextFeature(feat):
			attrsstart = feat.attributes()[int(startid)]
			attrsend = feat.attributes()[int(endid)]
			attrsdist = feat.attributes()[int(distid)]
			table = table+[(int(attrsstart), int(attrsend), float(attrsdist))]
		G = nx.Graph()
		G.add_weighted_edges_from(table)
		tableidpers = []
		tablemetpers = []
		affecpers = []
		distpers = []
		geompers = []
		for pt_feature in aLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geompers = geompers + [geom]
			pers = pt_feature.attributes()[persid]
			tableidpers = tableidpers + [int(pers)]
			met = pt_feature.attributes()[metpersid]
			tablemetpers = tablemetpers + [int(met)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = id
				if n == 0 :
					test = 1
					marge = marge + 50
			affecpers = affecpers + [int(idmin)]
			distpers = distpers + [float(math.sqrt(distmin))]
		tableideta = []
		tablemeteta = []
		affeceta = []
		disteta = []
		geometa = []
		for pt_feature in bLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geometa = geometa + [geom]
			eta = pt_feature.attributes()[etaid]
			tableideta = tableideta + [int(eta)]
			etab = pt_feature.attributes()[metetaid]
			tablemeteta = tablemeteta + [int(etab)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = id
				if n == 0 :
					test = 1
					marge = marge + 50
			affeceta = affeceta + [int(idmin)]
			disteta = disteta + [float(math.sqrt(distmin))]
		vec = []
		for i in range(len(tableidpers)):
			for j in range(len(tableideta)):
				if tablemetpers[i] == tablemeteta[j] :
					try :
						dist = float(nx.shortest_path_length(G, affecpers[i], affeceta[j], weight='weight')) + ( distpers[i] / float(vitesse) ) + ( disteta[j] / float(vitesse) )
						vec = vec + [[tableidpers[i],tableideta[j],dist]]
					except :
						dist = 9999999999
						vec = vec + [[tableidpers[i],tableideta[j],dist]]
		vitesse = 10 * 1000 / float(3600)
		idstart2 = self.dlg3.ui.comboBoxd.currentText()
		startid2 = providerc2.fieldNameIndex(str(idstart2))
		idend2 = self.dlg3.ui.comboBox2d.currentText()
		endid2 = providerc2.fieldNameIndex(str(idend2))
		iddist2 = self.dlg3.ui.comboBoxe.currentText()
		distid2 = providerc2.fieldNameIndex(str(iddist2))
		idnoeud2 = self.dlg3.ui.comboBox2e.currentText()
		noeudid2 = providerd2.fieldNameIndex(str(idnoeud2))
		table = []
		feat = QgsFeature()
		fit = providerc2.getFeatures()
		while fit.nextFeature(feat):
			attrsstart = feat.attributes()[int(startid2)]
			attrsend = feat.attributes()[int(endid2)]
			attrsdist = feat.attributes()[int(distid2)]
			table = table + [(int(attrsstart), int(attrsend), float(attrsdist))]
		G = nx.Graph()
		G.add_weighted_edges_from(table)
		tableidpers = []
		affecpers = []
		distpers = []
		geompers = []
		for pt_feature in aLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geompers = geompers + [geom]
			pers = pt_feature.attributes()[persid]
			tableidpers = tableidpers + [int(pers)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer2.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid2]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = [int(id)]
					if dist == distmin :
						idmin = idmin + [int(id)]
				if n == 0 :
					test = 1
					marge = marge + 50
			affecpers = affecpers + [idmin]
			distpers = distpers + [float(math.sqrt(distmin))]
		tableideta = []
		affeceta = []
		disteta = []
		geometa = []
		for pt_feature in bLayer.getFeatures():
			geom = pt_feature.geometry().asPoint()
			geometa = geometa + [geom]
			eta = pt_feature.attributes()[etaid]
			tableideta = tableideta + [int(eta)]
			test = 1
			marge = 10
			while test == 1 :
				test = 0
				n = 0
				distmin = 100000000000000000000000
				cands = dLayer2.getFeatures(QgsFeatureRequest().setFilterRect(QgsRectangle(geom[0]-marge,geom[1]-marge,geom[0]+marge,geom[1]+marge)))
				for pt2_feature in cands:
					n = n + 1
					id = pt2_feature[noeudid2]
					geom2 = pt2_feature.geometry().asPoint()
					dist = geom2.sqrDist(geom)
					if dist < distmin :
						distmin = dist
						idmin = [int(id)]
					if dist == distmin :
						idmin = idmin + [int(id)]
				if n == 0 :
					test = 1
					marge = marge + 50
			affeceta = affeceta + [idmin]
			disteta = disteta + [float(math.sqrt(distmin))]
		vec2 = []
		for i in range(len(tableidpers)):
			for j in range(len(tableideta)):
				if tablemetpers[i] == tablemeteta[j] :
					d = 9999999999
					for k in range(len(affecpers[i])):
						for l in range(len(affeceta[j])):
							try :
								dcal = nx.shortest_path_length(G, affecpers[i][k], affeceta[j][l], weight='weight')
								if dcal < d :
									d = dcal
							except :
								"Do Nothing"
					if d == 9999999999 :
						dist = d
						vec2 = vec2 + [[tableidpers[i],tableideta[j],dist]]
					else :
						dist = d + ( distpers[i] / float(vitesse) ) + ( disteta[j] / float(vitesse) )
						vec2 = vec2 + [[tableidpers[i],tableideta[j],dist]]
		vl = QgsVectorLayer("LineString?scr=epsg:"+str(epsg), "Distancier", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("Id_Pers", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Id_Eta", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Temps", QVariant.Double) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(len(vec)):
			ind1 = tableidpers.index(vec[i][0])
			ind2 = tableideta.index(vec[i][1])
			if vec[i][2] <= vec2[i][2] :
				fet = QgsFeature()
				fet.setGeometry( QgsGeometry.fromPolyline([ geompers[ind1] , geometa[ind2] ]) )
				fet.setAttributes( [ vec[i][0], vec[i][1], vec[i][2] ] )
				pr.addFeatures( [ fet ] )
			else :
				fet = QgsFeature()
				fet.setGeometry( QgsGeometry.fromPolyline([ geompers[ind1] , geometa[ind2] ]) )
				fet.setAttributes( [ vec2[i][0], vec2[i][1], vec2[i][2] ] )
				pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

  #----------------------------------------------------------------------------------------------------------------------------------------                  Clustering              -----------------------------------------------------------------------------------------------------------------------------------
	def runclust(self):
		global canvas
		canvas = self.iface.mapCanvas()
		global allLayers
		allLayers = canvas.layers()
		global count
		count = canvas.layerCount()
		global lay
		lay = []
		for i in allLayers:
			lay = lay + [str(i.name())]
		self.dlg = DialogClustering(self.iface.mainWindow())
		self.dlg.ui.comboBox.addItems(lay)
		self.dlg.ui.comboBox2.addItems(['Oui', 'Non'])
		self.dlg.ui.comboBox3.addItems(['Nombre de groupes', 'Distance maximum'])
		self.dlg.ui.buttonBox.accepted.connect(self.clustinfo)
		self.dlg.show()

	def clustinfo(self):
		table = self.dlg.ui.comboBox.currentText()
		cont = self.dlg.ui.comboBox2.currentText()
		met = self.dlg.ui.comboBox3.currentText()
		for j in range(count):
			if str(table) == str(lay[j]) :
				ind = j
		global aLayer
		aLayer = allLayers[int(ind)]
		global provider
		provider = aLayer.dataProvider()
		global field
		field = provider.fields()
		global fields
		fields = []
		for i in range(field.count()):
			fields = fields+[str(field[i].name())]
		self.dlg2 = DialogClustInfo(self.iface.mainWindow())
		self.dlg2.ui.comboBox.addItems(fields)
		self.dlg2.ui.comboBox2.addItems(fields)
		if met == "Nombre de groupes" and cont == "Non":
			self.dlg2.ui.label3.setText(QApplication.translate("Dialog", "Nombre de groupes", None))
			self.dlg2.ui.buttonBox.accepted.connect(self.kmeancal)
		if met == "Nombre de groupes" and cont == "Oui":
			self.dlg2.ui.label3.setText(QApplication.translate("Dialog", "Nombre de groupes", None))
			self.dlg2.ui.buttonBox.accepted.connect(self.kmeancal)
			t = u"Cette méthode ne prend pas en compte les contraintes spatiales"
			QMessageBox.information(None, " Message : ", t.encode('latin-1'))
		if met == "Distance maximum" and cont == "Non":
			self.dlg2.ui.label3.setText(QApplication.translate("Dialog", "Distance maximum", None))
			self.dlg2.ui.buttonBox.accepted.connect(self.cahcal)
		if met == "Distance maximum" and cont == "Oui":
			self.dlg2.ui.label3.setText(QApplication.translate("Dialog", "Distance maximum", None))
			self.dlg2.ui.buttonBox.accepted.connect(self.cahcal2)
		self.dlg2.show()

	def kmeancal(self):
		idtab = self.dlg2.ui.comboBox.currentText()
		idnbr = self.dlg2.ui.comboBox2.currentText()
		gr = int(self.dlg2.ui.lineedit3.text())
		tabid = provider.fieldNameIndex(str(idtab))
		nbrid = provider.fieldNameIndex(str(idnbr))
		feat = QgsFeature()
		fit = provider.getFeatures()
		tabpt = []
		tabptid = []
		tabval = []
		while fit.nextFeature(feat):
			tabpt = tabpt + [[float(feat.geometry().asPoint().x()), float(feat.geometry().asPoint().y())]]
			tabptid = tabptid + [ int(feat.attributes()[tabid]) ]
			tabval = tabval  + [ int(feat.attributes()[nbrid]) ]
		atabpt = np.array(tabpt)
		centroids,_ = kmeans(atabpt,gr)
		ids,_ = vq(atabpt,centroids)
		valres = [0] * gr
		nbcol = int(provider.fields().count())
		aLayer.startEditing()
		provider.addAttributes( [ QgsField("ID_CLUST", QVariant.Int) ] )
		aLayer.commitChanges()
		aLayer.startEditing()
		for i in range(len(ids)):
			aLayer.changeAttributeValue(i,nbcol,int(ids[i]))
			valres[int(ids[i])] = valres[int(ids[i])] + tabval[i]
		aLayer.commitChanges()
		epsg = canvas.mapRenderer().destinationCrs().authid()
		vl = QgsVectorLayer("Point?scr=epsg:"+str(epsg), "New_Points", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("ID", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Nombre", QVariant.Int) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(len(centroids)):
			fet = QgsFeature()
			fet.setGeometry( QgsGeometry.fromPoint(QgsPoint( float(centroids[i][0]) , float(centroids[i][1]) ) ) )
			fet.setAttributes( [ i, valres[i] ] )
			pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def cahcal(self):
		idtab = self.dlg2.ui.comboBox.currentText()
		idnbr = self.dlg2.ui.comboBox2.currentText()
		dist = int(self.dlg2.ui.lineedit3.text())
		tabid = provider.fieldNameIndex(str(idtab))
		nbrid = provider.fieldNameIndex(str(idnbr))
		feat = QgsFeature()
		fit = provider.getFeatures()
		tabpt = []
		tabptid = []
		tabval = []
		while fit.nextFeature(feat):
			tabpt = tabpt + [[float(feat.geometry().asPoint().x()), float(feat.geometry().asPoint().y())]]
			tabptid = tabptid + [ int(feat.attributes()[tabid]) ]
			tabval = tabval  + [ int(feat.attributes()[nbrid]) ]
		atabpt = np.array(tabpt)
		z = linkage(atabpt,method='complete',metric='euclidean')
		grcah = fcluster(z,t=dist,criterion='distance')
		valx = [0] * max(grcah)
		valy = [0] * max(grcah)
		valres = [0] * max(grcah)
		nbcol = int(provider.fields().count())
		aLayer.startEditing()
		provider.addAttributes( [ QgsField("ID_CLUST", QVariant.Int) ] )
		aLayer.commitChanges()
		aLayer.startEditing()
		for i in range(len(grcah)):
			aLayer.changeAttributeValue(i,nbcol,int(grcah[i]))
			valx[int(grcah[i])-1] = valx[int(grcah[i])-1] + (tabval[i] * tabpt[i][0])
			valy[int(grcah[i])-1] = valy[int(grcah[i])-1] + (tabval[i] * tabpt[i][1])
			valres[int(grcah[i])-1] = valres[int(grcah[i])-1] + tabval[i]
		aLayer.commitChanges()
		epsg = canvas.mapRenderer().destinationCrs().authid()
		vl = QgsVectorLayer("Point?scr=epsg:"+str(epsg), "New_Points", "memory")
		pr = vl.dataProvider()
		vl.startEditing()
		pr.addAttributes( [ QgsField("ID", QVariant.Int) ] )
		pr.addAttributes( [ QgsField("Nombre", QVariant.Int) ] )
		vl.commitChanges()
		vl.startEditing()
		for i in range(max(grcah)):
			fet = QgsFeature()
			x = valx[i] / float(valres[i])
			y = valy[i] / float(valres[i])
			fet.setGeometry( QgsGeometry.fromPoint(QgsPoint( float(x) , float(y) ) ) )
			fet.setAttributes( [ i+1 , valres[i] ] )
			pr.addFeatures( [ fet ] )
		vl.commitChanges()
		QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

	def cahcal2(self):
		icont, ok = QInputDialog.getItem(None,"Contrainte","La couche contrainte : ", lay, editable = False)
		if ok :
			for j in range(count):
				if str(icont) == str(lay[j]) :
					indcont = j
			contLayer = allLayers[int(indcont)]
			providercont = contLayer.dataProvider()
			feat = QgsFeature()
			fit = providercont.getFeatures()
			geomcont = []
			while fit.nextFeature(feat):
				geomcont = geomcont + [ feat.geometry().exportToWkt() ]
			grcont = [[]] * len(geomcont)
			idtab = self.dlg2.ui.comboBox.currentText()
			idnbr = self.dlg2.ui.comboBox2.currentText()
			dist = int(self.dlg2.ui.lineedit3.text())
			tabid = provider.fieldNameIndex(str(idtab))
			nbrid = provider.fieldNameIndex(str(idnbr))
			feat = QgsFeature()
			fit = provider.getFeatures()
			tabpt = []
			tabptid = []
			tabval = []
			j = 0
			while fit.nextFeature(feat):
				tabpt = tabpt + [[ float(feat.geometry().asPoint().x()), float(feat.geometry().asPoint().y()) ]]
				tabptid = tabptid + [ int(feat.attributes()[tabid]) ]
				tabval = tabval  + [ int(feat.attributes()[nbrid]) ]
				for i in range(len(geomcont)):
					if feat.geometry().intersects( QgsGeometry.fromWkt(geomcont[i]) ):
						grcont[i] = grcont[i] +[j]
				j = j + 1
			atabpt = np.array(tabpt)
			m = 0
			grcah2 = np.array([0]*len(tabval))
			for i in range(len(grcont)):
				if len(grcont[i]) > 1:
					z = linkage(atabpt[grcont[i]],method='complete',metric='euclidean')
					grcah = fcluster(z,t=dist,criterion='distance')
					grcah2[[grcont[i]]] = list(np.array(list(grcah)) + m)
					m = m + max(grcah)
				if len(grcont[i]) == 1:
					m = m + 1
					grcah2[[grcont[i]]] = [[m]]
			valx = [0] * max(grcah2)
			valy = [0] * max(grcah2)
			valres = [0] * max(grcah2)
			nbcol = int(provider.fields().count())
			aLayer.startEditing()
			provider.addAttributes( [ QgsField("ID_CLUST", QVariant.Int) ] )
			aLayer.commitChanges()
			aLayer.startEditing()
			for i in range(len(grcah2)):
				aLayer.changeAttributeValue(i,nbcol,int(grcah2[i]))
				valx[int(grcah2[i])-1] = valx[int(grcah2[i])-1] + (tabval[i] * tabpt[i][0])
				valy[int(grcah2[i])-1] = valy[int(grcah2[i])-1] + (tabval[i] * tabpt[i][1])
				valres[int(grcah2[i])-1] = valres[int(grcah2[i])-1] + tabval[i]
			aLayer.commitChanges()
			epsg = canvas.mapRenderer().destinationCrs().authid()
			vl = QgsVectorLayer("Point?scr=epsg:"+str(epsg), "New_Points", "memory")
			pr = vl.dataProvider()
			vl.startEditing()
			pr.addAttributes( [ QgsField("ID", QVariant.Int) ] )
			pr.addAttributes( [ QgsField("Nombre", QVariant.Int) ] )
			vl.commitChanges()
			vl.startEditing()
			for i in range(max(grcah2)):
				fet = QgsFeature()
				x = valx[i] / float(valres[i])
				y = valy[i] / float(valres[i])
				fet.setGeometry( QgsGeometry.fromPoint(QgsPoint( float(x) , float(y) ) ) )
				fet.setAttributes( [ i+1 , valres[i] ] )
				pr.addFeatures( [ fet ] )
			vl.commitChanges()
			QgsMapLayerRegistry.instance().addMapLayer(vl)
		QMessageBox.information(None, " Message : ", "Fin")

  #----------------------------------------------------------------------------------------------------------------------------------------                 Optimisation            -----------------------------------------------------------------------------------------------------------------------------------
	def runoptim(self):
		global canvas
		canvas = self.iface.mapCanvas()
		global allLayers
		allLayers = canvas.layers()
		global count
		count = canvas.layerCount()
		global lay
		lay = []
		for i in allLayers:
			lay = lay + [str(i.name())]
		self.dlg = DialogOptim(self.iface.mainWindow())
		self.dlg.ui.comboBox.addItems(lay)
		self.dlg.ui.comboBox2.addItems(lay)
		self.dlg.ui.comboBox3.addItems(lay)
		self.dlg.ui.comboBox4.addItems(['Exacte', 'Approchee'])
		self.dlg.ui.buttonBox.accepted.connect(self.optiminfo)
		self.dlg.show()

	def optiminfo(self):
		table = self.dlg.ui.comboBox.currentText()
		for j in range(count):
			if str(table) == str(lay[j]) :
				ind = j
		global aLayer
		aLayer = allLayers[int(ind)]
		global provider
		provider = aLayer.dataProvider()
		global field
		field = provider.fields()
		global fields
		fields = []
		for i in range(field.count()):
			fields = fields+[str(field[i].name())]
		table2 = self.dlg.ui.comboBox2.currentText()
		for j in range(count):
			if str(table2) == str(lay[j]) :
				ind = j
		global aLayer2
		aLayer2 = allLayers[int(ind)]
		global provider2
		provider2 = aLayer2.dataProvider()
		global field2
		field2 = provider2.fields()
		global fields2
		fields2 = []
		for i in range(field2.count()):
			fields2 = fields2+[str(field2[i].name())]
		table3 = self.dlg.ui.comboBox3.currentText()
		for j in range(count):
			if str(table3) == str(lay[j]) :
				ind = j
		global aLayer3
		aLayer3 = allLayers[int(ind)]
		global provider3
		provider3 = aLayer3.dataProvider()
		global field3
		field3 = provider3.fields()
		global fields3
		fields3 = []
		for i in range(field3.count()):
			fields3 = fields3+[str(field3[i].name())]
		algo = str(self.dlg.ui.comboBox4.currentText())
		self.dlg2 = DialogOptimInfo(self.iface.mainWindow())
		self.dlg2.ui.comboBox.addItems(fields)
		self.dlg2.ui.comboBox2.addItems(fields)
		self.dlg2.ui.comboBox3.addItems(fields2)
		self.dlg2.ui.comboBox4.addItems(fields2)
		self.dlg2.ui.comboBox5.addItems(fields3)
		self.dlg2.ui.comboBox6.addItems(fields3)
		self.dlg2.ui.comboBox7.addItems(fields3)
		if algo == "Exacte":
				self.dlg2.ui.buttonBox.accepted.connect(self.optimexacal)
		if algo == "Approchee":
				self.dlg2.ui.buttonBox.accepted.connect(self.optimapproxcal)
		self.dlg2.show()

	def optimexacal(self):
		idpers = self.dlg2.ui.comboBox.currentText()
		nbrpers = self.dlg2.ui.comboBox2.currentText()
		ideta = self.dlg2.ui.comboBox3.currentText()
		nbreta = self.dlg2.ui.comboBox4.currentText()
		iddep = self.dlg2.ui.comboBox5.currentText()
		idarr = self.dlg2.ui.comboBox6.currentText()
		dist = self.dlg2.ui.comboBox7.currentText()
		persid = provider.fieldNameIndex(str(idpers))
		persnbr = provider.fieldNameIndex(str(nbrpers))
		etaid = provider2.fieldNameIndex(str(ideta))
		etanbr = provider2.fieldNameIndex(str(nbreta))
		arrid = provider3.fieldNameIndex(str(idarr))
		depid = provider3.fieldNameIndex(str(iddep))
		dista = provider3.fieldNameIndex(str(dist))
		G = nx.DiGraph()
		feat = QgsFeature()
		fit = provider.getFeatures()
		tabpersid = []
		tabpersnbr = []
		while fit.nextFeature(feat):
			tabpersid = tabpersid + [ int(feat.attributes()[persid]) ]
			tabpersnbr = tabpersnbr + [ int(feat.attributes()[persnbr]) ]
			G.add_node(int(feat.attributes()[persid]), demand=-int(feat.attributes()[persnbr]))
		feat = QgsFeature()
		fit = provider2.getFeatures()
		tabetaid = []
		tabetanbr = []
		while fit.nextFeature(feat):
			tabetaid = tabetaid + [ int(feat.attributes()[etaid]) ]
			tabetanbr = tabetanbr + [ int(feat.attributes()[etanbr]) ]
			G.add_node(int(feat.attributes()[etaid]), demand=int(feat.attributes()[etanbr]))
		feat = QgsFeature()
		fit = provider3.getFeatures()
		tab = []
		dist = []
		while fit.nextFeature(feat):
			tab = tab + [[ int(feat.attributes()[depid]), int(feat.attributes()[arrid]) ]]
			dist = dist + [int(feat.attributes()[dista])]
			w = int(tabpersnbr[tabpersid.index(int(feat.attributes()[depid]))])
			G.add_edge(int(feat.attributes()[depid]), int(feat.attributes()[arrid]), weight=int(feat.attributes()[dista]), capacity=w)
		UG = G.to_undirected()
		r = list(nx.connected_components(UG))
		d = {}
		for i in range(len(r)):
			H = G.subgraph(r[i]).copy()
			v = dict(nx.get_node_attributes(H, 'demand'))
			vald = np.array(list(v.items()))
			s = sum(vald[:,1])
			if s > 0 :
				li = list(H.nodes())
				H.add_node(987654321, demand=-int(s))
				for i in range(len(li)):
					if v[li[i]] > 0 :
						H.add_edge(987654321, int(li[i]), weight=99999999999, capacity=int(s))
			if s < 0 :
				li = list(H.nodes())
				H.add_node(987654321, demand=-int(s))
				for i in range(len(li)):
					if v[li[i]] < 0 :
						H.add_edge(int(li[i]), 987654321, weight=99999999999, capacity=-int(v[li[i]]))
			flowCost, flowDict = nx.network_simplex(H)
			d.update(dict(flowDict))
		nbcol=int(provider.fields().count())
		aLayer.startEditing()
		for i in range(len(tabetaid)):
			provider.addAttributes( [ QgsField("Eta_"+str(tabetaid[i]), QVariant.Int) ] )
		provider.addAttributes( [ QgsField("Total", QVariant.Int), QgsField("Dispo", QVariant.Int), QgsField("Taux", QVariant.Double), QgsField("Statut", QVariant.Int), QgsField("TPS_1h", QVariant.Int), QgsField("TPS_45", QVariant.Int) ] )
		aLayer.commitChanges()
		aLayer.startEditing()
		for i in range(len(tabpersid)):
			tot = 0
			tot1h = 0
			tot45 = 0
			for j in range(len(tabetaid)):
				try :
					ind = tab.index([int(tabpersid[i]),int(tabetaid[j])])
					if dist[ind] == 9999999999 :
						aLayer.changeAttributeValue(i,nbcol + j, -int(d[int(tabpersid[i])][int(tabetaid[j])]))
					if dist[ind] < 9999999999 :
						aLayer.changeAttributeValue(i,nbcol + j,int(d[int(tabpersid[i])][int(tabetaid[j])]))
						if int(d[int(tabpersid[i])][int(tabetaid[j])]) != 0 :
							tot = tot + 1
							if dist[ind] < 36000 :
								tot1h = tot1h + 1
								if dist[ind] < 27000:
									tot45 = tot45 + 1
				except :
					aLayer.changeAttributeValue(i,nbcol + j, 0)
			aLayer.changeAttributeValue(i, nbcol + j + 1,tot)
			aLayer.changeAttributeValue(i, nbcol + j + 3, tot/float(tabpersnbr[i]))
			aLayer.changeAttributeValue(i, nbcol + j + 5,tot1h)
			aLayer.changeAttributeValue(i, nbcol + j + 6,tot45)
			if tabpersnbr[i] == tot :
				aLayer.changeAttributeValue(i, nbcol + j + 2, 1)
				if tot45 == tot :
					aLayer.changeAttributeValue(i, nbcol + j + 4, 3)
				if tot45 != tot :
					aLayer.changeAttributeValue(i, nbcol + j + 4, 2)
				if tot1h != tot :
					aLayer.changeAttributeValue(i, nbcol + j + 4, 1)
			else :
				aLayer.changeAttributeValue(i, nbcol + j + 2, 0)
				aLayer.changeAttributeValue(i, nbcol + j + 4, 0)
		aLayer.commitChanges()
		nbcol=int(provider2.fields().count())
		aLayer2.startEditing()
		provider2.addAttributes( [ QgsField("Total", QVariant.Int), QgsField("Dispo", QVariant.Int), QgsField("Taux", QVariant.Double), QgsField("Statut", QVariant.Int), QgsField("TPS_1h", QVariant.Int), QgsField("TPS_45", QVariant.Int) ] )
		aLayer2.commitChanges()
		aLayer2.startEditing()
		for i in range(len(tabetaid)):
			tot = 0
			tot1h = 0
			tot45 = 0
			for j in range(len(tabpersid)):
				try :
					ind = tab.index([int(tabpersid[j]),int(tabetaid[i])])
					if dist[ind] != 9999999999 :
						if int(d[int(tabpersid[j])][int(tabetaid[i])]) != 0 :
							tot = tot + 1
							if dist[ind] < 36000 :
								tot1h = tot1h + 1
								if dist[ind] < 27000:
									tot45 = tot45 + 1
				except :
					"Do Nothing"
			aLayer2.changeAttributeValue(i, nbcol, tot)
			aLayer2.changeAttributeValue(i, nbcol + 2, tot/float(tabetanbr[i]))
			aLayer2.changeAttributeValue(i, nbcol + 4, tot1h)
			aLayer2.changeAttributeValue(i, nbcol + 5, tot45)
			if tabetanbr[i] == tot :
				aLayer2.changeAttributeValue(i, nbcol + 1, 1)
				if tot45 == tot :
					aLayer2.changeAttributeValue(i, nbcol + 3, 3)
				if tot45 != tot :
					aLayer2.changeAttributeValue(i, nbcol + 3, 2)
				if tot1h != tot :
					aLayer2.changeAttributeValue(i, nbcol + 3, 1)
			else :
				aLayer2.changeAttributeValue(i, nbcol + 1, 0)
				aLayer2.changeAttributeValue(i, nbcol + 3, 0)
		aLayer2.commitChanges()
		QMessageBox.information(None, " Message : ", "Fin")

	def optimapproxcal(self):
			idpers = self.dlg2.ui.comboBox.currentText()
			nbrpers = self.dlg2.ui.comboBox2.currentText()
			ideta = self.dlg2.ui.comboBox3.currentText()
			nbreta = self.dlg2.ui.comboBox4.currentText()
			iddep = self.dlg2.ui.comboBox5.currentText()
			idarr = self.dlg2.ui.comboBox6.currentText()
			dist = self.dlg2.ui.comboBox7.currentText()
			persid = provider.fieldNameIndex(str(idpers))
			persnbr = provider.fieldNameIndex(str(nbrpers))
			etaid = provider2.fieldNameIndex(str(ideta))
			etanbr = provider2.fieldNameIndex(str(nbreta))
			arrid = provider3.fieldNameIndex(str(idarr))
			depid = provider3.fieldNameIndex(str(iddep))
			dista = provider3.fieldNameIndex(str(dist))
			feat = QgsFeature()
			fit = provider.getFeatures()
			tabpersid = []
			tabpersnbr = []
			pid = []
			i = 0
			while fit.nextFeature(feat):
				tabpersid = tabpersid + [ int(feat.attributes()[persid]) ]
				tabpersnbr = tabpersnbr + [ int(feat.attributes()[persnbr]) ]
				pid = pid + [i] * int(feat.attributes()[persnbr])
				i = i + 1
			feat = QgsFeature()
			fit = provider2.getFeatures()
			tabetaid = []
			tabetanbr = []
			eid = []
			eidfin = []
			i = 0
			while fit.nextFeature(feat):
				tabetaid = tabetaid + [ int(feat.attributes()[etaid]) ]
				tabetanbr = tabetanbr + [ int(feat.attributes()[etanbr]) ]
				eid = eid + [i]
				eidfin = eidfin + [i] * int(feat.attributes()[etanbr])
				i = i + 1
			feat = QgsFeature()
			fit = provider3.getFeatures()
			dist = []
			vecdist = []
			for i in range(len(tabpersid)):
				ligne = []
				for j in range(len(tabetaid)):
					fit.nextFeature(feat)
					ligne = ligne + [int(feat.attributes()[dista])]
					vecdist = vecdist + [[int(feat.attributes()[dista]),i,j]]
				dist = dist + [ligne]
			trivecdist = sorted(vecdist)
			capeta = copy.copy(tabetanbr)
			capeaffec = [0] * len(eid)
			persaffec = [0] * len(pid)
			vec = ['NULL'] * len(pid)
			tot = 0
			for i in range(len(trivecdist)):
				idpers = trivecdist[i][1]
				ideta = trivecdist[i][2]
				if persaffec[idpers] == 0 and capeaffec[ideta] < capeta[ideta] :
					persaffec[idpers] = 1
					capeaffec[ideta] = capeaffec[ideta] + 1
					vec[idpers] = [trivecdist[i][0],idpers,ideta]
					tot = tot + trivecdist[i][0]
			trivec  = sorted(vec, reverse = True)
			atrivec = np.array(trivec)
			i = 0
			while i < len(vec) :
				minval = 0
				idpers1 = trivec[i][1]
				ideta1 = trivec[i][2]
				for j in range(len(vec)):
					if j != i and ideta1 != trivec[j][2] :
						idpers2 = trivec[j][1]
						ideta2 = trivec[j][2]
						val = dist[idpers2][ideta1] + dist[idpers1][ideta2] - trivec[i][0] - trivec[j][0]
						if val < minval :
							minval = val
							id1 = idpers2
							id2 = idpers1
							ide1 = ideta2
							ide2 = ideta1
							js = j
				if minval < 0 :
					trivec[i] = [dist[id2][ide1],id2,ide1]
					trivec[js] = [dist[id1][ide2],id1,ide2]
					trivec = sorted(trivec,reverse = True)
					i = 0
				else :
					i = i + 1
			atrivec = np.array(trivec)
			nbcol = int(provider.fields().count())
			aLayer.startEditing()
			for i in range(len(tabetaid)):
				provider.addAttributes( [ QgsField("Eta_"+str(tabetaid[i]), QVariant.Int) ] )
			aLayer.commitChanges()
			aLayer.startEditing()
			tabres = []
			for i in range(len(tabpersid)):
				ligneres = []
				for j in range(len(tabetaid)):
					aLayer.changeAttributeValue(i,nbcol+j,0)
					ligneres = ligneres + [0]
				tabres = tabres + [ligneres]
			aLayer.commitChanges()
			aLayer.startEditing()
			for i in range(len(trivec)):
				if trivec[i][0] == 9999999999 :
					tabres[trivec[i][1]][trivec[i][2]] = tabres[trivec[i][1]][trivec[i][2]] - 1
					val = tabres[trivec[i][1]][trivec[i][2]]
					aLayer.changeAttributeValue(trivec[i][1],nbcol+trivec[i][2], val)
				if trivec[i][0] != 9999999999 :
					tabres[trivec[i][1]][trivec[i][2]] = tabres[trivec[i][1]][trivec[i][2]] + 1
					val = tabres[trivec[i][1]][trivec[i][2]]
					aLayer.changeAttributeValue(trivec[i][1],nbcol+trivec[i][2], val)
			aLayer.commitChanges()
			QMessageBox.information(None, " Message : ", "Fin")
