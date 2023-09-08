
from OCR.helpers.contours import sort_contours
from OCR.helpers.text_extract import text_extraction
from OCR.helpers.constants import doc_image_dirctory_name
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import  pandas as pd
from OCR.helpers.pdf_to_image import convert_pdf_in_images
from OCR.helpers.remove_img import remove_jpg_files

def document_data(path):
    try:
        convert_pdf_in_images(path)
    except Exception as error:
        return str(error)    

    df=pd.DataFrame()
    for img_path in os.listdir(doc_image_dirctory_name):
        try:
            img = cv2.imread(doc_image_dirctory_name+img_path,0)
            table_img = img
            # [390:2050,370:1480]
            thresh,img_bin = cv2.threshold(table_img,128,255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
        except Exception as error:
            print(error)
            
        # Length(width) of kernel as 100th of total width
        kernel_len = np.array(table_img).shape[1]//100
        # Defining a vertical kernel to detect all vertical lines of image 
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        # Defining a horizontal kernel to detect all horizontal lines of image
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        #Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

        #Use horizontal kernel to detect and save the horizontal lines in a jpg
        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
        
        # Combine horizontal and vertical lines in a new third image, with both having same weight.
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        #Eroding and thesholding the image
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    
        bitxor = cv2.bitwise_xor(table_img,img_vh)
        bitnot = cv2.bitwise_not(bitxor)

        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, boundingBoxes = sort_contours(contours, method='top-to-bottom')

        #Creating a list of heights for all detected boxes
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        
        #Get mean of heights
        mean = np.mean(heights)

        #Create list box to store all boxes in  
        box = []
        # Get position (x,y), width and height for every contour and show the contour on image
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w<1000 and h<500):
                cv2.rectangle(table_img,(x,y),(x+w,y+h),(0,255,0),2)
                box.append([x,y,w,h])

        #Creating two lists to define row and column in which cell is located
        row=[]
        column=[]
        j=0
        #Sorting the boxes to their respective row and column
        for i in range(len(box)):
            if(i==0):
                column.append(box[i])
                previous=box[i]
            else:
                if(box[i][1]==previous[1]):
                    column.append(box[i])
                    previous=box[i]
                    if(i==len(box)-1):
                        row.append(column)    
                else:
                    row.append(column)
                    column=[]
                    previous = box[i]
                    column.append(box[i])

        countcol = 0
        for i in range(len(row)):
            countcol = len(row[i])
            if countcol > countcol:
                countcol = countcol
        center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center=np.array(center)
        center.sort() 

        finalboxes = []
        for i in range(len(row)):
            lis=[]
            for k in range(countcol):
                lis.append([])
            for j in range(len(row[i])):
                diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
                minimum = min(diff)
                indexing = list(diff).index(minimum)
                lis[indexing].append(row[i][j])
            finalboxes.append(lis)

        outer=text_extraction(finalboxes,bitnot)

        arr = np.array(outer)    
        pdf_dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
        df=pd.concat([pdf_dataframe,df])
        remove_jpg_files(doc_image_dirctory_name)


    return df
    
