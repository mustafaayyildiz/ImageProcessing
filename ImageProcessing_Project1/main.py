# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from skimage import io, filters
from enum import Enum
import skimage.morphology as mp
import skimage.transform as tf
from skimage.exposure import rescale_intensity
from skimage.exposure import equalize_hist
from skimage.color import rgb2gray
import numpy as np
import os
import cv2

class FILTERS(Enum):
     GAUSSIAN = "Gaussian"
     LAPLACE = "Laplace"
     HESSIAN = "Hessian"
     PREWITT = "Prewitt"
     SATO = "Sato"
     MEDIAN = "Median"
     ROBERTS = "Roberts"
     GABOR = "Gabor"
     MEIJERING = "Meijering"
     ROBERTS_NEG_DIAG = "RobertsNegDiag"
     
class MORPHOLOGY(Enum):
    OPENING = "Opening"
    CLOSING = "Closing"
    EROSION = "Erosion"
    DILATION = "Dilation"
    WHITE_TOPHAT = "WhiteTophat"
    BLACK_TOPHAT = "BlackTophat"
    AREA_OPENING = "AreaOpening"
    AREA_CLOSING = "AreaClosing"
    DIAMETER_OPENING = "DiameterOpening"
    DIAMETER_CLOSING = "DiameterClosing"
    
class TRANSFORMS(Enum):
    ROTATION = "Rotation"
    RESIZING = "Resizing"
    RESCALING = "Rescaling"
    SWIRL = "Swirl"
    RADON = "Radon"
    

class Root(Tk):
    filePath = ""
    def __init__(self):
        super(Root, self).__init__()
        self.title("Image Processing Project")
        self.minsize(640, 400)
        
        #Main Tab
        tabControl = ttk.Notebook(self)
        #Filter Tab
        self.tabContent = ttk.Frame(tabControl)
        tabControl.add(self.tabContent, text="Content")
        
        tabControl.pack(expan = 1, fill = "both")
        self.fillToTabContent()
    
    #CONTENT
    def fillToTabContent(self):
        self.findImgPath()
        self.selectFilter()
        self.selectMorphology()
        self.selectTransform()
        self.videoCapture()
        self.histogram()
        self.rescaleIntensity()
        self.loadImageBefore()
        self.loadImageAfter()
        
    
    #FIND_IMAGE
    def findImgPath(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Load Image")
        labelFrame.grid(column=0, row=0)
        #Button
        button = ttk.Button(labelFrame, text="Open A File", command=self.fileDialog)
        button.grid(column=0, row=0)
        #Label
        self.imgPath = ttk.Label(labelFrame, text="")
        self.imgPath.grid(column=0, row=1)
    
    def fileDialog(self):
        self.filePath = filedialog.askopenfilename(initialdir="C:/Users/musta/.spyder-py3/Projects/ImageProcessing_Project1", title="Select A File", filetype=(("jpeg", "*.jpg"), ("png", "*.png")))
        self.file = os.path.basename(self.filePath)
        self.file = self.file.split(".")
        self.imgPath.configure(text=self.file[0] + "." + self.file[1])
        #Change Image
        image = Image.open(self.filePath)
        photo = ImageTk.PhotoImage(image)
        #Change Label
        self.labelBeforeImg.configure(image=photo)
        self.labelBeforeImg.image = photo
        
        self.img = io.imread(self.filePath, flatten=True)
    
    #BEFORE
    def loadImageBefore(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Before")
        labelFrame.grid(column=1, row=0)
        #Image
        image = Image.open("notImg.png")
        photo = ImageTk.PhotoImage(image)
        #Label
        self.labelBeforeImg = ttk.Label(labelFrame, image=photo)
        self.labelBeforeImg.image = photo
        self.labelBeforeImg.grid(column=0, row=0)
    
    #AFTER
    def loadImageAfter(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="After")
        labelFrame.grid(column=2, row=0)
        #Image
        image = Image.open("notImg.png")
        photo = ImageTk.PhotoImage(image)
        #Label
        self.labelAfterImg = ttk.Label(labelFrame, image=photo)
        self.labelAfterImg.image = photo
        self.labelAfterImg.grid(column=0, row=0)
        
    def selectFilter(self):
        self.selectedFilter = StringVar()
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Select Filter")
        labelFrame.grid(column=0, row=1)#padx =1 , pady=3
        #Combobox
        comboFilter = ttk.Combobox(labelFrame, width=15, textvariable=self.selectedFilter)
        myFilterArr = []
        for myFilter in FILTERS:
            myFilterArr.append(myFilter.value)
            comboFilter['values'] = myFilterArr
        comboFilter.grid(column=0, row=0)
        #Button
        button = ttk.Button(labelFrame, text="Select", command=self.applyFilter)
        button.grid(column=1, row=0)
        #Label
        self.labelFilterMsg = ttk.Label(labelFrame, text="")
        self.labelFilterMsg.grid(column=0, row=1)
    
    def applyFilter(self):
        selectedFilter = self.selectedFilter.get()
        if selectedFilter != "" and self.filePath != "":
            self.labelFilterMsg.configure(text="selected ->" + selectedFilter + " Filter")
            if selectedFilter == FILTERS.GAUSSIAN.value:
                self.gaussianFilter()
            elif selectedFilter == FILTERS.LAPLACE.value:
                self.laplaceFilter()
            elif selectedFilter == FILTERS.HESSIAN.value:
                self.hessianFilter()
            elif selectedFilter == FILTERS.PREWITT.value:
                self.prewittFilter()
            elif selectedFilter == FILTERS.SATO.value:
                self.satoFilter()
            elif selectedFilter == FILTERS.MEDIAN.value:
                self.medianFilter()
            elif selectedFilter == FILTERS.ROBERTS.value:
                self.robertsFilter()
            elif selectedFilter == FILTERS.GABOR.value:
                self.gaborFilter()
            elif selectedFilter == FILTERS.MEIJERING.value:
                self.meijeringFilter()
            elif selectedFilter == FILTERS.ROBERTS_NEG_DIAG.value:
                self.robertsNegDiagFilter()
                
    def selectMorphology(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Select Morphology")
        labelFrame.grid(column=1, row=1)
        #Combobox
        self.selectedMorphology = StringVar()
        comboMorphology = ttk.Combobox(labelFrame, width=15, textvariable=self.selectedMorphology)
        myMorphologyArr = []
        for myMorphology in MORPHOLOGY:
            myMorphologyArr.append(myMorphology.value)
            comboMorphology['values'] = myMorphologyArr
        comboMorphology.grid(column=0, row=0)
        #Button
        button = ttk.Button(labelFrame, text="Select", command=self.applyMorphology)
        button.grid(column=1, row=0)
        #Label
        self.labelMorphologyMsg = ttk.Label(labelFrame, text="")
        self.labelMorphologyMsg.grid(column=0, row=1)
        
    def applyMorphology(self):
        selectedMorphology = self.selectedMorphology.get()
        if selectedMorphology != "" and self.filePath != "":
            self.labelMorphologyMsg.configure(text="selected ->" + selectedMorphology + " Morphology")
            if selectedMorphology == MORPHOLOGY.OPENING.value:
                self.opening()
            elif selectedMorphology == MORPHOLOGY.CLOSING.value:
                self.closing()
            elif selectedMorphology == MORPHOLOGY.EROSION.value:
                self.erosion()
            elif selectedMorphology == MORPHOLOGY.DILATION.value:
                self.dilation()
            elif selectedMorphology == MORPHOLOGY.WHITE_TOPHAT.value:
                self.whiteTophat()
            elif selectedMorphology == MORPHOLOGY.BLACK_TOPHAT.value:
                self.blackTophat()
            elif selectedMorphology == MORPHOLOGY.AREA_OPENING.value:
                self.areaOpening()
            elif selectedMorphology == MORPHOLOGY.AREA_CLOSING.value:
                self.areaClosing()
            elif selectedMorphology == MORPHOLOGY.DIAMETER_OPENING.value:
                self.diameterOpening()
            elif selectedMorphology == MORPHOLOGY.DIAMETER_CLOSING.value:
                self.diameterClosing()
    
    def selectTransform(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Select Transform")
        labelFrame.grid(column=2, row=1)
        #Combobox
        self.selectedTransform = StringVar()
        comboTransform = ttk.Combobox(labelFrame, textvariable=self.selectedTransform)
        myTransformArr = []
        for myTransform in TRANSFORMS:
            myTransformArr.append(myTransform.value)
            comboTransform['values'] = myTransformArr
        comboTransform.grid(column=0, row=0)
        #Button
        button = ttk.Button(labelFrame, text="Select", command=self.applyTransform)
        button.grid(column=1, row=0)
        #Label
        self.labelTransformMsg = ttk.Label(labelFrame, text="")
        self.labelTransformMsg.grid(column=0, row=1)
        
    def applyTransform(self):
        selectedTransform = self.selectedTransform.get()
        if selectedTransform != "" and self.filePath != "":
            self.labelTransformMsg.configure(text="selected ->" + selectedTransform + " Transform")
            if selectedTransform == TRANSFORMS.ROTATION.value:
                self.rotate()
            elif selectedTransform == TRANSFORMS.RESIZING.value:
                self.resizing()
            elif selectedTransform == TRANSFORMS.RESCALING.value:
                self.rescaling()
            elif selectedTransform == TRANSFORMS.SWIRL.value:
                self.swirl()
            elif selectedTransform == TRANSFORMS.RADON.value:
                self.radon()
    
    #VideoCapture
    def videoCapture(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Video Capture")
        labelFrame.grid(column=0, row=2)
        #Label
        labelMsg = ttk.Label(labelFrame, text="videodan çıkmak için 'q' ya basınız.")
        labelMsg.grid(column=0, row=1)
        #Button
        button = ttk.Button(labelFrame, text="Edge Detection", command=self.applyVideoCapture)
        button.grid(column=0, row=0)
    
    #VideoCapture
    def applyVideoCapture(self):
        cap = cv2.VideoCapture(0)

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # perform edge detection
            """laplacian = cv2.Laplacian(gray,cv2.CV_64F)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)"""
            edges = cv2.Canny(gray, 100, 200)
            # Display the resulting frame
            cv2.imshow('Edge Detection',edges)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    #end of videoCapture
    
    #Rescale_Intensity
    def rescaleIntensity(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Rescale Intensity")
        labelFrame.grid(column=1, row=2)
        #Label1
        labelInRangeMsg = ttk.Label(labelFrame, text="In Range")
        labelInRangeMsg.grid(column=0, row=0)
        #Combobox1
        rangeArr = ("image", "dtype", "dtype-name", "2-tuple")
        self.selectedInRange = StringVar()
        comboInRange = ttk.Combobox(labelFrame, textvariable=self.selectedInRange)
        comboInRange['values'] = rangeArr
        comboInRange.grid(column=1, row=0)
        #Label2
        labelOutRangeMsg = ttk.Label(labelFrame, text="Out Range")
        labelOutRangeMsg.grid(column=0, row=1)
        #Combobox2
        self.selectedOutRange = StringVar()
        comboOutRange = ttk.Combobox(labelFrame, textvariable=self.selectedOutRange)
        comboOutRange['values'] = rangeArr
        comboOutRange.grid(column=1, row=1)
        #Button
        button = ttk.Button(labelFrame, text="Look Result", command=self.applyRescaleIntensity)
        button.grid(column=1, row=2)
    
    def applyRescaleIntensity(self):
        selectedInRange = self.selectedInRange.get()
        selectedOutRange = self.selectedOutRange.get()
        if selectedInRange != "" and selectedOutRange != "":
            result = rescale_intensity(self.img, selectedInRange, selectedOutRange)
            #Convert float64 to uint8
            result = result / result.max()
            result = 255 * result
            result = result.astype(np.uint8)
            self.displayImage(result, "filter", "RescaleIntensity")
    #end of RescaleIntensity
    
    #HISTOGRAM
    def histogram(self):
        #LabelFrame
        labelFrame = ttk.LabelFrame(self.tabContent, text="Histogram")
        labelFrame.grid(column=2, row=2)
        #Button
        button = ttk.Button(labelFrame, text="Look Result", command=self.applyHistogram)
        button.grid(column=0, row=0)
        
    def applyHistogram(self):
        img = equalize_hist(self.img)
        self.displayImage(img, "filter", "Histogram")
    #end of histogram
    
    #FILTERS
    def gaussianFilter(self):
        #Apply Filter
        filteredImg = filters.gaussian(self.img, sigma=1)
        self.displayImage(filteredImg, "filter", FILTERS.GAUSSIAN.value)
    
    def laplaceFilter(self):
        self.img = rgb2gray(self.img)
        filteredImg = filters.laplace(self.img)
        #Convert float64 to uint8
        filteredImg = filteredImg / filteredImg.max()
        filteredImg = 255 * filteredImg
        filteredImg = filteredImg.astype(np.uint8)
        self.displayImage(filteredImg, "filter", FILTERS.LAPLACE.value)
        
    def hessianFilter(self):
        filteredImg = filters.hessian(self.img)
        self.displayImage(filteredImg, "filter", FILTERS.HESSIAN.value)
    
    def prewittFilter(self):
        #Convert float64 to uint8
        self.img = self.img / self.img.max()
        self.img = 255 * self.img
        self.img = self.img.astype(np.uint8)
        filteredImg = filters.prewitt(self.img)
        self.displayImage(filteredImg, "filter", FILTERS.PREWITT.value)
    
    def satoFilter(self):
        filteredImg = filters.sato(self.img, sigmas=range(0,10,2), black_ridges="True")
        self.displayImage(filteredImg, "filter", FILTERS.SATO.value)
    
    def medianFilter(self):
        #Convert float64 to uint8
        self.img = self.img / self.img.max()
        self.img = 255 * self.img
        self.img = self.img.astype(np.uint8)
        #Convert to Gray
        self.img = rgb2gray(self.img)
        filteredImg = filters.median(self.img)
        self.displayImage(filteredImg, "filter", FILTERS.MEDIAN.value)
    
    def robertsFilter(self):
        filteredImg = filters.roberts(self.img)
        self.displayImage(filteredImg, "filter", FILTERS.ROBERTS.value)
    
    def gaborFilter(self):
        #Convert float64 to uint8
        self.img = self.img / self.img.max()
        self.img = 255 * self.img
        self.img = self.img.astype(np.uint8)
        filteredReal, filteredImg = filters.gabor(self.img, frequency=0.6)
        self.displayImage(filteredReal, "filter", FILTERS.GABOR.value)
    
    def meijeringFilter(self):
        filteredImg = filters.meijering(self.img, sigmas=range(1, 10, 2))
        self.displayImage(filteredImg, "filter", FILTERS.MEIJERING.value)
        
    def robertsNegDiagFilter(self):
        #Convert float64 to uint8
        self.img = self.img / self.img.max()
        self.img = 255 * self.img
        self.img = self.img.astype(np.uint8)
        filteredImg = filters.roberts_neg_diag(self.img)
        self.displayImage(filteredImg, "filter", FILTERS.ROBERTS_NEG_DIAG.value)
    #end of filters 
    
    #MORPHOLOGIES            
    def opening(self):
        self.convertToUint8()
        img = mp.opening(self.img, mp.square(15))
        self.displayImage(img, "morphology", MORPHOLOGY.OPENING.value)
        
    def closing(self):
        self.convertToUint8()
        img = mp.closing(self.img, mp.square(15))
        self.displayImage(img, "morphology", MORPHOLOGY.CLOSING.value)

    def erosion(self):
        self.convertToUint8()
        img = mp.erosion(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.EROSION.value)
        
    def dilation(self):
        self.convertToUint8()
        img = mp.dilation(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.DILATION.value)
        
    def whiteTophat(self):
        self.convertToUint8()
        img = mp.white_tophat(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.WHITE_TOPHAT.value)
    
    def blackTophat(self):
        self.convertToUint8()
        img = mp.black_tophat(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.BLACK_TOPHAT.value)
        
    def areaOpening(self):
        self.convertToUint8()
        img = mp.area_opening(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.AREA_OPENING.value)
    
    def areaClosing(self):
        self.convertToUint8()
        img = mp.area_closing(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.AREA_CLOSING.value)
        
    def diameterOpening(self):
        self.convertToUint8()
        img = mp.diameter_opening(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.DIAMETER_OPENING.value)
        
    def diameterClosing(self):
        self.convertToUint8()
        img = mp.diameter_closing(self.img)
        self.displayImage(img, "morphology", MORPHOLOGY.DIAMETER_CLOSING.value)
    #end of morphologies
    
    #TRANSFORM
    def rotate(self):
        transformedImg = tf.rotate(self.img, 15)
        self.displayImage(transformedImg, "transform", TRANSFORMS.ROTATION.value)
        
    def resizing(self):
        tranformedImg = tf.resize(self.img, (self.img.shape[0]-59, self.img.shape[1]-24))
        self.displayImage(tranformedImg, "transform", TRANSFORMS.RESIZING.value)
    
    def rescaling(self):
        transformedImg = tf.rescale(self.img, 0.50, multichannel=False)
        self.displayImage(transformedImg, "transform", TRANSFORMS.RESCALING.value)
        
    def swirl(self):
        transformedImg = tf.swirl(self.img, rotation=3)
        self.displayImage(transformedImg, "transform", TRANSFORMS.SWIRL.value)
        
    def radon(self):
        transformedImg = tf.radon(self.img)
        #Convert float64 to uint8
        transformedImg = transformedImg / transformedImg.max()
        transformedImg = 255 * transformedImg
        transformedImg = transformedImg.astype(np.uint8)
        self.displayImage(transformedImg, "transform", TRANSFORMS.RADON.value)    
    # end of Transform
    
    def displayImage(self, img, savePath, filterName):
        #Save Image
        saveName = savePath + "/" + self.file[0] + filterName + "." + self.file[1]
        io.imsave(saveName, img)
        #Save Message
        labelMsg = ttk.Label(self.tabContent, text="Photo is saved")
        labelMsg.grid(column=0, row=3)
        #Change Image
        image = Image.open(os.path.split(self.filePath)[0] + "/" + saveName)
        photo = ImageTk.PhotoImage(image)
        #Change Label
        self.labelAfterImg.configure(image=photo)
        self.labelAfterImg.image = photo
        
    def convertToUint8(self):
        self.img = self.img / self.img.max()
        self.img = 255 * self.img
        self.img = self.img.astype(np.uint8)

if __name__ == '__main__':
    root = Root()
    root.mainloop()
    