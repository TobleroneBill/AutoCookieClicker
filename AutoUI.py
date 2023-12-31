import pyautogui
from PIL import Image
import keyboard
import cv2
import numpy as np

GoldCookie = cv2.imread('GoldCookie.png',cv2.IMREAD_UNCHANGED)

IMAGES = [
    Image.open('LookImgs\CursorBuy.PNG'),
    Image.open('LookImgs\GrandmaBuy.PNG'),
    Image.open('LookImgs\FarmBuy.PNG'),
    Image.open('LookImgs\MineBuy.PNG'),
    Image.open('LookImgs\FactoryBuy.PNG'),
    Image.open('LookImgs\BankBuy.PNG'),
    Image.open('LookImgs\TempleBuy.PNG'),
    Image.open('LookImgs\WizardBuy.PNG'),
]


threshold = 0.8     # Confidence

def PressUpgrade():
    print('finding upgrade')
    for image in IMAGES:
        pos = pyautogui.locateOnScreen(image,grayscale=True,confidence=threshold)
        if pos is not None:
            pyautogui.moveTo(pos)
            pyautogui.leftClick()

def MoveDown():
    pos = pyautogui.position()
    #20 possible buildings
    for i in range(2):
        print('-------------------------------------------------------')
        mousePos = list(pos)
        print(pos)
        print(mousePos)

        for i in range(11): 
            mousePos[1] += 95
            pyautogui.moveTo(mousePos)
            pyautogui.click()
            print(f'NewPos: {mousePos}')
        pyautogui.scroll(100)

# Test Area
# haystackImg = pyautogui.screenshot()
# result = cv2.matchTemplate(haystackImg,GoldCookie,cv2.TM_CCOEFF_NORMED)
# cv2.imshow('Res',result)
# cv2.waitKey()