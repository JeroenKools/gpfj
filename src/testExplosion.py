"""
KABOOM! Comic book-like explosions in Tkinter

Jeroen Kools, 2013
"""

import Tkinter as Tk
import math 
import random
import colorsys

def star(x,y,innerRadius,outerRadius,th0=0,arms=5,noise=0):
    coords = []
    noise = max(0,noise)
    N = lambda x=0: random.randint(-noise,noise)
        
    for i in range(arms):
        th1 = 2.*math.pi*i/arms + th0
        th2 = 2.*math.pi*(i+.5)/arms + th0
                 
        coords += [x+math.sin(th1)*innerRadius+N(),
                   y+math.cos(th1)*innerRadius+N(),
                   x+math.sin(th2)*outerRadius+N(),
                   y+math.cos(th2)*outerRadius+N()]
    return coords

def explosion(canvas, x,y,stars,h=90,w=150, arms=9, noise=30):
    colors = gradient(0,1./6,1,.8,stars)
    for i in range(stars):        
        th0 = math.pi*random.random()
        coords = star(x,y,int(h*.9**i),int(w*.9**i),th0, arms, int(noise*.7**i))
        canvas.create_polygon(coords,outline=None,fill=colors[i])

def gradient(startHue, endHue, startSaturation, endSaturation, steps):
    hstepsize = (endHue-startHue)/(steps-1)
    sstepsize = (float(endSaturation)-startSaturation)/(steps-1)
    hue = [startHue+i*hstepsize for i in range(steps+1)]
    saturation = [startSaturation+i*sstepsize for i in range(steps+1)]
    colors = [colorsys.hsv_to_rgb(h, s, 1) for (h,s) in zip(hue,saturation)] 
    colors = ["#%02x%02x%02x" % (int(255*c[0]),int(255*c[1]),int(255*c[2])) for c in colors]
    return colors 

class KABOOM:
    def __init__(self, root):
        self.root = root
        self.canvas = Tk.Canvas(root,width=500,height=500)
        self.canvas.grid(columnspan=3) 
        Tk.Button(root, text="KABOOM!", command=self.boom).grid(row=1, column=0)
        Tk.Button(root, text="Kaboom!", command=lambda: self.kaboom(250,250)).grid(row=1, column=1)
        Tk.Button(root, text="Clear!", command = lambda: self.canvas.delete(Tk.ALL)).grid(row=1, column=2)
        self.canvas.bind("<Button-1>", self.onclick)
        
    def boom(self):
        self.canvas.delete(Tk.ALL)
        for i in range(random.randint(4,9)):
            explosion(self.canvas, 
                random.randint(0,500),
                random.randint(0,500),  # location
                random.randint(3,6),    # stars/colors
                random.randint(60,80),  # inner radius
                random.randint(100,140),# outer radius
                random.randint(5,11),   # arms
                random.randint(10,40))  # noise
            
    def onclick(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.kaboom(x, y)
            
    def kaboom(self, x, y):
        """Small explosion, available on click"""
        colors = gradient(0,1./7,1,1,5)
        basename = random.randint(0,1000000)
        th0 = math.pi*random.random()
        
        for i in range(5):
            coords = star(x, y, 15-2*i, 30-i*2, th0, 7, 6-i)
            name = "star%i_part%i" % (basename, i)
            self.canvas.create_polygon(coords, outline=None,fill=colors[i], state = Tk.HIDDEN, tags = name)    

        self.reveal(basename, 4)

    def reveal(self, basename, i): 
        if i>=0:
            self.canvas.itemconfig("star%i_part%i" % (basename, i), state=Tk.NORMAL)
            self.root.after(40, lambda: self.reveal(basename, i-1))
        else:
            self.hide(basename, i)
            
    def hide(self, basename, i):
        if i<5:
            self.canvas.delete("star%i_part%i" % (basename, i))
            self.root.after(60, lambda: self.hide(basename, i+1))

if __name__ == "__main__":
    root = Tk.Tk()
    root.title("KABOOM! Explosions!")
    b = KABOOM(root)
    root.mainloop()
