from PIL import Image, ImageEnhance, ImageFilter
from PIL import *
import time
import base64
import numpy as np
from io import BytesIO
import persistence

def imageToBase64(img):
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    base64Img = base64.b64encode(buffer.getvalue())
    return 'data:image/jpg;base64,' + str(base64Img, encoding='utf-8')

def imgTransfer(img):
    '''
    图片预处理，二值化，图片增强
    :param img: 原始图片 Image
    :return:    图片 Image
    '''
    # newImg = img.filter(ImageFilter.MedianFilter())
    newImg = img.convert('1')
    return newImg

def imgSegment(img):
    '''
    切分验证码的前三个字符图片
    :param img: 完整图片
    :return: 三个验证码小图数组
    '''
    s = 5
    w = 30
    h = 33
    t = 12
    segments = []

    for i in range(3):
        tile = img.crop((s+w*i, t, s+w*(i+1), h))
        segments.append(tile)
    return segments

def getBinaryPix(img):
    '''
    获取图像的二值化数学值
    :param img:
    :return:
    '''
    matImg = np.array(img)
    rows, cols = matImg.shape
    for i in range(rows):
        for j in range(cols):
            if(matImg[i, j] <= 128):
                matImg[i, j] = 0
            else:
                matImg[i, j] =1
    binpix = np.ravel(matImg)
    return binpix

def save(img, value):
    base64Img = imageToBase64(img)
    binpix = getBinaryPix(img).tolist()
    binpix = [str(i) for i in binpix]
    content = ','.join(binpix)
    collection = persistence.openConnection()
    persistence.addImageToCollection(collection, base64Img, content, value)

def process(img, lNumber, operator, rNumber):
    '''
    训练识别
    :param img:
    :param lNumber:
    :param operator:
    :param rNumber:
    :return:
    '''

    segments = imgSegment(img)
    if segments and len(segments) == 3:
        lImg = imgTransfer(segments[0])
        opImg = imgTransfer(segments[1])
        rImg = imgTransfer(segments[2])

        # lImg.show(command='fim')
        # opImg.show(command='fim')
        # rImg.show(command='fim')

        save(lImg, lNumber)
        save(opImg, operator)
        save(rImg, rNumber)




