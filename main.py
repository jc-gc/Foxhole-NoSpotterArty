import tkinter as tk
import os
import re
import pygubu
import math
from PIL import Image, ImageTk

imglocation = './Images/Maps/'
PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = PROJECT_PATH + './inter.ui'

class Program:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('frame_1')
        builder.connect_callbacks(self)

        self.cmbBox = builder.get_object('cmbBox')
        self.imgCanvas = builder.get_object('imgCanvas')
        self.lblDistance = builder.get_object('lblDistance')
        self.lblAzi = builder.get_object('lblAzi')

        self.imgCanvas.bind('<Button-1>', self.getPos)
        self.imgCanvas.bind('<Button-3>', self.getTarget)
        self.imgCanvas.config(cursor='crosshair')

        self.tiles = dict()

        self.pos, self.target = None, None
        self.tarline = None

        self.getPos = False

    def run(self):
        self.findtiles()

        self.cmbBox['values'] = tuple(self.tiles)

        self.mainwindow.mainloop()

    def findtiles(self):
        for tile in os.listdir(imglocation):
            if tile.startswith('Map'):
                name = tile.replace('Map','')
                name = name.replace('Hex.TGA','').replace('.TGA','')
                name = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', name)
                self.tiles.update([(name,f'{imglocation+tile}')])

    def getPos(self, event):
        x,y = event.x, event.y
        mx = self.pix2m(0,1078.84,0 ,18*128,x)
        my = self.pix2m(0,1078.84,0 ,18*128,y)



        if self.pos is not None:
            self.imgCanvas.delete(self.pos['posdot'])

        posdot = self.imgCanvas.create_oval(x-3,y-3,x+3,y+3, fill='green')
        self.pos = {'x': x,
                    'y': y,
                    'mx': mx,
                    'my': my,
                    'posdot': posdot}

        self.updateVal()

    def getTarget(self, event):
        x, y = event.x, event.y
        mx = self.pix2m(0, 1078.84, 0, 18 * 128, x)
        my = self.pix2m(0, 1078.84, 0, 18 * 128, y)
        
        howieoffset = self.pix2m(0, 18*128, 0, 1078.84, 150)
        mortaroffset = self.pix2m(0, 18 * 128, 0, 1078.84, 65)

        if self.target is not None:
            self.imgCanvas.delete(self.target['tardot'])
            for ring in self.target['rngrings']:
                self.imgCanvas.delete(ring)
        tardot = self.imgCanvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill='red')
        
        
        rngrings = [self.imgCanvas.create_oval(x-howieoffset,y-howieoffset,x+howieoffset,y+howieoffset),
            self.imgCanvas.create_oval(x-mortaroffset,y-mortaroffset,x+mortaroffset,y+mortaroffset)]
        self.target = {'x': x,
                       'y': y,
                       'mx': mx,
                       'my': my,
                       'tardot': tardot,
                       'rngrings': rngrings}

        self.updateVal()

    def updateVal(self):
        if self.tarline is not None:
            self.imgCanvas.delete(self.tarline)
        if self.pos is not None and self.target is not None:
            distance = math.sqrt( math.pow(self.pos['mx'] - self.target['mx'], 2) + math.pow(self.pos['my'] - self.target['my'], 2) )
            azi = math.atan2(self.pos['my'] - self.target['my'], self.pos['mx'] - self.target['mx'])
            self.tarline = self.imgCanvas.create_line(self.pos['x'], self.pos['y'], self.target['x'], self.target['y'], width=2, smooth=1)
            self.lblDistance.config(text=f'Distance: {round(distance,1)}m')
            self.lblAzi.config(text=f'Azi: {round((math.degrees(azi) - 90) % 360)}')


    def loadimg(self):
        self.pos, self.target = None, None
        sel = self.cmbBox.get()
        im = Image.open(self.tiles[sel])
        im = ImageTk.PhotoImage(im)
        self.imgCanvas.delete(tk.ALL)
        self.imgCanvas.create_image(0,0, anchor=tk.NW, image=im)

        ic=0
        for i in range(-4,1054,59):
            ic+=1
            self.imgCanvas.create_line(i,0,i,888, fill='gray')
            self.imgCanvas.create_text(i + 10, 10, text=chr(64+ic))

        xc=0
        for x in range(-2,888,59):
            xc+=1
            self.imgCanvas.create_line(0,x,1024,x, fill='gray')
            self.imgCanvas.create_text(10, x + 35, text=xc)


        self.mainwindow.mainloop()

    def pix2m(self, omin, omax, nmin, nmax, ovalue):
        OldRange = (omax - omin)
        NewRange = (nmax - nmin)
        NewValue = (((ovalue - omin) * NewRange) / OldRange) + nmin
        return NewValue

if __name__ == '__main__':
    program = Program()
    program.run()