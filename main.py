from PIL import Image, ImageGrab
import pytesseract
import cutlet
import os, time
import translators as ts
import translators.server as tss
import wx
import threading

class Translator():
    def get_lines(self, x1, y1, x2, y2):
        bbox = (x1, y1, x2, y2)
        im = ImageGrab.grab(bbox)

        text_raw = pytesseract.image_to_string(im, lang='jpn', config="--psm 11")
        text = text_raw.replace('/', '!')

        text = "\n".join([linea.rstrip() for linea in text.splitlines() if linea.strip()])
        lines = text.splitlines()
        
        return lines

    def start_reading(self, x1, y1, x2, y2):
        katsu = cutlet.Cutlet()
        katsu.use_foreign_spelling = False

        lines = []

        while True:
            new_lines = self.get_lines(x1, y1, x2, y2)

            if lines != new_lines:
                os.system('cls')
                lines = new_lines
                for line in lines:
                    print('🗨️   ' + line)
                    print('👀   ' + katsu.romaji(line))
                    print("---------------------------------")
                
            time.sleep(0.1)

class DesktopController(wx.Frame):
    def __init__(self, parent, title):
        super(DesktopController, self).__init__(parent, title=title)
        self.SetTransparent(200)
        self.button = wx.Button(self, label="Start", size=(200,100))
        
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)

        self.SetPosition(wx.Point(0,0))
        self.Show()
    
    def on_button_click(self, event):
        size = self.button.Size
        x1,y1 = self.button.GetScreenPosition()
        x2,y2 = x1 + size[0], y1 + size[1]

        #Iniciar traduccion
        t = threading.Thread(target=Translator().start_reading, args=(x1, y1, x2, y2))
        t.daemon = True
        t.start()

if __name__ == '__main__':
    app = wx.App()
    mf = DesktopController(None, title="Selecciona un area")
    app.MainLoop()