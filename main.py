from PIL import Image, ImageGrab
import pytesseract
import cutlet
import os, time
import translators as ts
import translators.server as tss
import wx
import threading

APP_EXIT = 1

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
        self.InitUI()

    def InitUI(self):
        self.SetTransparent(200)

        #MenuBar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')

        img = wx.Image('./assets/exit.png', wx.BITMAP_TYPE_PNG)
        img = img.Scale(16, 16, wx.IMAGE_QUALITY_HIGH)
        qmi.SetBitmap(wx.Bitmap(img))
        
        fileMenu.Append(qmi)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.SetSize((350, 250))
        self.SetTitle('Icons and shortcuts')
        self.Centre()
        #MenuBar

        #Button-OCR
        self.button = wx.Button(self, label="", size=(200,100))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)
        

        self.SetPosition(wx.Point(0,0))
        self.Show()
    
    #OCR FUNCTION
    def on_button_click(self, event):
        size = self.button.Size
        x1,y1 = self.button.GetScreenPosition()
        x2,y2 = x1 + size[0], y1 + size[1]

        #Iniciar traduccion
        t = threading.Thread(target=Translator().start_reading, args=(x1, y1, x2, y2))
        t.daemon = True
        t.start()
    #OCR FUNCTION

    def OnQuit(self, e):
        self.Close()

def main():
    app = wx.App()
    mf = DesktopController(None, title="OCR Translator")
    app.MainLoop()

if __name__ == '__main__':
    main()