from random import randrange

# get layer
ls = QgsProject.instance().layerStore()
layer = ls.mapLayersByName('run')[0]

# attribute
attr = 'class'

# get unique values
values = layer.fields().indexFromName(attr)
unique_ids = layer.dataProvider().uniqueValues(values)

# define categories
categories = []
for unique_id in unique_ids:
    # initialize the default symbol for this geometry type
    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setOpacity(0.5)

    # random fill color black outline
    layer_style = dict()
    layer_style['color'] = '%d, %d, %d' % (randrange(0, 256), randrange(0, 256), randrange(0, 256))
    layer_style['outline'] = '#000000'
    symbolLayer = QgsSimpleFillSymbolLayer.create(layer_style)

    if symbolLayer is not None:
        symbol.changeSymbolLayer(0, symbolLayer)

    category = QgsRendererCategory(unique_id, symbol, str(unique_id))
    categories.append(category)

renderer = QgsCategorizedSymbolRenderer(attr, categories)

# assign the created renderer to the layer
if renderer is not None:
    layer.setRenderer(renderer)
layer.triggerRepaint()
