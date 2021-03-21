from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2


class PeopleDetect(object):

    def __init__(self):
        # 1、定义HOG对象
        self.hog = cv2.HOGDescriptor()
        # 2、设置SVM分类器
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detectImg(self, imagePath):
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()
        '''
        构造了一个尺度scale=1.05的图像金字塔，以及一个分别在x方向和y方向步长为(4,4)像素大小的滑窗
        scale的尺度设置得越大，在图像金字塔中层的数目就越少，相应的检测速度就越快，但是尺度太大会导致行人出现漏检；
        同样的，如果scale设置得太小，将会急剧的增加图像金字塔的层数，这样不仅耗费计算资源，而且还会急剧地增加检测过程
        中出现的假阳数目(也就是不是行人的被检测成行人)。这表明，scale是在行人检测过程中它是一个重要的参数，
        需要对scale进行调参。我会在后面的文章中对detectMultiScale中的每个参数做些调研。
        '''
        rects, weights = self.hog.detectMultiScale(image, winStride=(4, 4),
            padding=(8, 8), scale=1.05)
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 应用非极大抑制方法，通过设置一个阈值来抑制那些重叠的边框
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        # show some information on the number of bounding boxes
        filename = imagePath[imagePath.rfind("/") + 1:]
        print("[INFO] {}: {} original boxes, {} after suppression".format(
            filename, len(rects), len(pick)))
        # show the output images
        # cv2.imshow("Before NMS", orig)
        # cv2.imshow("After NMS", image)
        return orig, image, len(pick)

    def detectVideo(self, frame):
        image = frame
        image = imutils.resize(image, width=min(400, image.shape[1]))
        orig = image.copy()
        rects, weights = self.hog.detectMultiScale(image, winStride=(4, 4),
            padding=(8, 8), scale=1.05)
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # 应用非极大抑制方法，通过设置一个阈值来抑制那些重叠的边框
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
        return orig, image, len(pick)
