import tkinter as tk
from PIL import ImageGrab
import os
import json
import subprocess
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint Application")
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen',True)
        self.root.bind("<Control-n>",self.reset)
        self.root.bind("<Control-s>",self.save)
        self.root.bind("<Control-w>",self.setMode)
        self.root.bind("<Control-o>",self.openFolder)
        self.root.bind("<Control-a>",self.setTransparency)
        self.root.bind("<Escape>",self.exit)
        self.last_x = None
        self.last_y = None
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="black",highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.PATH = ''
        self.imageCount = 1
        self.mode = 'WRITE'
        self.transparency = False
        self.loadConfig()
        self.setImageCount()
    def setTransparency(self,event):
        if self.transparency == False:
            self.root.attributes('-alpha',0.5)
        else:
            self.root.attributes("-alpha",1.0)
        self.transparency = not self.transparency
    def openFolder(self,event):
        subprocess.Popen(r"explorer " + f'{self.PATH}')
    def setMode(self,event):
        if self.mode == 'WRITE':
            self.mode = 'ERASE'
        else:
            self.mode = 'WRITE'
    def setImageCount(self):
        for x in os.listdir(self.PATH):
            if x[:5] == 'image':
                self.imageCount += 1
    def loadConfig(self):
        with open("config.json",'r') as f:
            self.PATH = json.loads(f.read())['savePath']
    def reset(self,event):
        self.canvas.delete("all")
    def exit(self,event):
        self.root.destroy()
    def save(self,event):
        image = ImageGrab.grab(bbox=(0,0,1920,1080))
        image.save(self.PATH + '/' + f'image{self.imageCount}.png')
        self.imageCount += 1
    def start_draw(self, event):
        # Anchor the starting coordinate upon clicking
        self.last_x = event.x
        self.last_y = event.y
    def draw(self, event):
        # Draw a continuous path by connecting the last point to the current point
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y, 
                width=3 if self.mode == 'WRITE' else 40, fill='white' if self.mode == 'WRITE' else 'black', capstyle=tk.ROUND, smooth=True
            )
        # Update the position tracking to the current point
        self.last_x = event.x
        self.last_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
#python -m PyInstaller --onefile --noconsole a.py