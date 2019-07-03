""" Load a layer and change the fill color to red. """
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *


def run_script(iface):
    project = QgsProject.instance()
    project.removeAllMapLayers()
    wb = QgsVectorLayer('C:/Users/Kelm/sciebo/Arbeit/Lehre/_Daten/Stadtbezirke_Bochum.shp', 'Stadtbezirke_Bochum', 'ogr')
    project.instance().addMapLayer(wb)
    renderer = wb.renderer()
    symb = renderer.symbol()
    symb.setColor(QColor(Qt.red))
    wb.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(wb.id())