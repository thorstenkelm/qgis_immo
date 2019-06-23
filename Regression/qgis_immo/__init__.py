# -*- coding: utf-8 -*-
"""
/***************************************************************************
 gqisImmo
                                 A QGIS plugin
 TODO
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-06-19
        copyright            : (C) 2019 by TODO
        email                : TODO
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load gqisImmo class from file gqisImmo.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .qgis_immo import gqisImmo
    return gqisImmo(iface)
