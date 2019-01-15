# -*- coding: utf-8 -*-
#-----------------------------------------------------------
#
# MOPPI
# Copyright Serge Lhomme
# EMAIL: serge.lhomme (at) u-pec.fr
# WEB  : http://sergelhomme.fr/
#
# Extension permettant de preparer la mobilite du personnel en periode d'inondation
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

def classFactory(iface):
  from .moppi import Moppi
  return Moppi(iface)
