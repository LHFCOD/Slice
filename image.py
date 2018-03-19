from PIL import Image
from xml.etree import ElementTree
##导入os，用来删除文件
import os
rootDirectory = '1'
xml_file_text = open(rootDirectory + '/DSI0/MoticDigitalSlideImage').read()
root = ElementTree.fromstring(xml_file_text)
LayerCount = int(root.find('./ImageMatrix/LayerCount').attrib['value'])
Layer0 = root.find('./ImageMatrix/Layer0')
maxRowValue = int(Layer0.find('./Rows').attrib['value'])
maxColsValue = int(Layer0.find('./Cols').attrib['value'])
scaleRowValue = maxRowValue
scaleColsValue = maxColsValue

cellWidth=int(root.find('./ImageMatrix/CellWidth').attrib['value'])
cellHeight=int(root.find('./ImageMatrix/CellHeight').attrib['value'])
##对所有图层进行遍历，除去最小的图层
for layerIndex in range(1, LayerCount - 1):
    Layer = root.find('./ImageMatrix/Layer' + str(layerIndex))
    RowValue = int(Layer.find('./Rows').attrib['value'])
    ColsValue = int(Layer.find('./Cols').attrib['value'])
    ##文件夹名字
    name = Layer.find('./Scale').attrib['value']
    ##补全为全目录
    name = rootDirectory + '/DSI0/' + name + '/'
    scaleColsValue /= 2
    scaleRowValue /= 2
    mRowValue = 1-(RowValue - scaleRowValue)
    mColsValue = 1-(ColsValue - scaleColsValue)
    pad_RowValue = '%04d' % (RowValue-1)
    if (mRowValue > 0):
        tileHeight=mRowValue*cellHeight
        for colsIndex in range(0, ColsValue):
            pad_colsIndex='%04d' % colsIndex
            fullPath=name + pad_RowValue + '_' + pad_colsIndex
            clipBox=(0,0,cellWidth,tileHeight)
            im=Image.open(fullPath)
            ##如果已经剪切过
            if im.height<cellHeight:
                continue
            region=im.crop(clipBox)
            im.close()
            os.remove(fullPath)
            region.save(fullPath)
    pad_ColsValue = '%04d' % (ColsValue-1)
    if (mColsValue > 0):
        tileWidth=mColsValue*cellWidth
        for rowIndex in range(0, RowValue):
            pad_rowIndex = '%04d' % rowIndex
            fullPath = name + pad_rowIndex + '_' + pad_ColsValue
            clipBox = (0, 0, tileWidth, cellHeight)
            im = Image.open(fullPath)
            ##如果已经剪切过
            if im.width<cellWidth:
                continue
            ##如果为右下角图片
            if rowIndex==RowValue-1:
                clipBox = (0, 0, tileWidth, im.height)
            region = im.crop(clipBox)
            im.close()
            os.remove(fullPath)
            region.save(fullPath)
