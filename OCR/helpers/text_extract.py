import pytesseract
import cv2

def text_extraction(finalboxes,bitnot):
    outer=[]
    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner=''
            if(len(finalboxes[i][j])==0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                    finalimg = bitnot[x:x+h, y:y+w]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                    resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel,iterations=1)
                    erosion = cv2.erode(dilation, kernel,iterations=1)
                    
                    erosion=255-erosion
                    erosion=cv2.cvtColor(erosion,cv2.COLOR_GRAY2BGR) 
                    cv2.imwrite('erosion.jpg',erosion)
                    erosion=cv2.imread('erosion.jpg')
                    final_h, final_w = erosion.shape[:2]
                    erosion=erosion[10:final_h-5,10:final_w-5]  

                    out = pytesseract.image_to_string(erosion,config='--psm 6')
                    out=out.replace('\n', ' ')
                    out=out.replace('\x0c','')
                    out=out.strip()
                    
                    if(len(out)==0):
                        out = pytesseract.image_to_string(erosion,config='--psm 6')
                        out=out.replace('\n', ' ')
                        out=out.replace('\x0c','')
                        out=out.strip()
                    inner = inner +" "+ out
                outer.append(inner)
    return outer