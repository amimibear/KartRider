import time
import pyscreenshot as ImageGrab

id0 = int(open(f'img/img/_.txt', 'r').read())+1

for id in range(id0,1000000):
    print(id)
    # im = ImageGrab.grab(bbox=(400, 130, 1340, 1160))  # X1,Y1,X2,Y2
    # im = ImageGrab.grab(bbox=(-1240, 150, -700, 755))  # X1,Y1,X2,Y2 iphone
    # im = ImageGrab.grab(bbox=(-1200, 30, -610, 870))  # X1,Y1,X2,Y2 ipad
    im = ImageGrab.grab(bbox=(270, 30, 880, 870))  # X1,Y1,X2,Y2 ipad
    time.sleep(5)
    im.save(f"img/img/{id}.png")
    open('img/img/_.txt', 'w').write(str(id))