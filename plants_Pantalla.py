import numpy as np
from PIL import ImageGrab
import cv2
import threading
from pynput import mouse

class Control(object):
  ciclo=False
  posX=0
  posY=0
  clicks=0

def on_scroll(x,y,dx,dy):
  cv2.destroyAllWindows()
  Control.ciclo=False

def on_move(x,y):
  #print("move")
  pass

def on_click(x,y,button,pressed):
  if (x==Control.posX and y==Control.posY):
    #print("click (",x,",",y,") vs [",Control.posX,",",Control.posY,"]")
    Control.clicks+=1
  else:
    Control.posX=x
    Control.posY=y
    Control.clicks=0
  
  if(Control.clicks>=3):
    Control.ciclo=True
    print("Corriendo programa")

  pass

def hiloListener():
  with mouse.Listener(on_move=on_move, on_click=on_click,on_scroll=on_scroll) as listener:
    listener.join()

def programaPLATA():
  interno=0
  while (True):
    #print("While infinito PLATA")
    while(Control.ciclo):
      if (interno==0 and Control.ciclo):#MONEDA PLATA
        imgPrueba1 = cv2.imread('moneda1.png')
        plantilla_heigth1, plantilla_width1 = imgPrueba1.shape[:2]
        printscreen_pil =  ImageGrab. grab()
        imgAnalizar =   np.array(printscreen_pil.getdata(),dtype='uint8')\
        .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
        height, width = imgAnalizar.shape[0:2]
        startRow = 100
        endRow = height
        startCol= 0
        endCol = width
        imgAnalizar = imgAnalizar[startRow:endRow, startCol:endCol]
        imgAnalizar = cv2.cvtColor(imgAnalizar, cv2.COLOR_BGR2RGB)
        result = cv2.matchTemplate(imgAnalizar, imgPrueba1, cv2.TM_CCOEFF)
        min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)
        (x_max, y_max) = max_location
        #cv2.imshow('imagen PLATA', imgAnalizar)
        cv2.waitKey(0)
        mous.position=((x_max+(plantilla_width1/2)),(100+y_max+(plantilla_heigth1/2)))
        mous.press(mouse.Button.left)
        mous.release(mouse.Button.left)

def programaORO():
  interno=0
  while(True):
    #print("While infinito ORO")
    while(Control.ciclo):
      if (interno==0 and Control.ciclo):#MONEDA ORO
        imgPrueba1 = cv2.imread('moneda2.png')
        plantilla_heigth1, plantilla_width1 = imgPrueba1.shape[:2]
        printscreen_pil =  ImageGrab. grab()
        imgAnalizar =   np.array(printscreen_pil.getdata(),dtype='uint8')\
        .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
        height, width = imgAnalizar.shape[0:2]
        startRow = 100
        endRow = height
        startCol= 0
        endCol = width
        imgAnalizar = imgAnalizar[startRow:endRow, startCol:endCol]
        imgAnalizar = cv2.cvtColor(imgAnalizar, cv2.COLOR_BGR2RGB)
        result = cv2.matchTemplate(imgAnalizar, imgPrueba1, cv2.TM_CCOEFF)
        min_value, max_value, min_location, max_location = cv2.minMaxLoc(result)
        (x_max, y_max) = max_location
        #cv2.imshow('imagen ORO', imgAnalizar)
        cv2.waitKey(0)
        mous.position=((x_max+(plantilla_width1/2)),(100+y_max+(plantilla_heigth1/2)))
        mous.press(mouse.Button.left)
        mous.release(mouse.Button.left)

mous=mouse.Controller()
control = Control()
enclave=True
activaListener=True
kernel = np.ones((5,5),np.uint8)
imgPrueba1 = cv2.imread('moneda1.png')
imgPrueba2 = cv2.imread('moneda2.png')
plantilla_heigth1, plantilla_width1 = imgPrueba1.shape[:2]
plantilla_heigth2, plantilla_width2 = imgPrueba2.shape[:2]
#print("antes de with")

threads = []
for i in range(3):
  if(i==0):
    t=threading.Thread(target=programaORO)
    threads.append(t)
    t.start()
  elif(i==1):
    t=threading.Thread(target=programaPLATA)
    threads.append(t)
    t.start()
  else:
    t=threading.Thread(target=hiloListener)
    threads.append(t)
    t.start()                                                    