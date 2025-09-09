from PIL import Image, ImageGrab
import pytesseract
import cutlet
import os, time
import wx
import threading

APP_EXIT = 1

class Translator():
    def __init__(self, callback=None):
        self.stop_translating = False
        self.callback = callback

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

        while not self.stop_translating:
            new_lines = self.get_lines(x1, y1, x2, y2)

            if lines != new_lines:
                lines = new_lines
                
                # Build the display text
                display_text = ""
                for line in lines:
                    display_text += '🗨️   ' + line + '\n'
                    display_text += '👀   ' + katsu.romaji(line) + '\n'
                    display_text += "---------------------------------\n"
                
                # Update GUI through callback
                if self.callback:
                    wx.CallAfter(self.callback, display_text)
                
                # Also print to console (optional)
                os.system('cls' if os.name == 'nt' else 'clear')
                for line in lines:
                    print('🗨️   ' + line)
                    print('👀   ' + katsu.romaji(line))
                    print("---------------------------------")

            time.sleep(1)

    def stop(self):
        self.stop_translating = True


class DesktopController(wx.Frame):
    def __init__(self, parent, title):
        super(DesktopController, self).__init__(parent, title=title)
        self.translator = None
        self.ocr_thread = None
        self.running = False
        self.init_ui()

    def init_ui(self):
        # Set window transparency (0-255, where 255 is fully opaque)
        self.SetTransparent(200)
        
        # Create main panel
        panel = wx.Panel(self)
        
        # Create horizontal sizer for side-by-side layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Create OCR button with descriptive label
        self.button = wx.Button(panel, label="")
        self.Bind(wx.EVT_BUTTON, self.on_button_click, self.button)
        
        # Create message text box (multiline, read-only)
        self.message_box = wx.TextCtrl(panel, 
                                    style=wx.TE_MULTILINE | wx.TE_READONLY,
                                    value="")
        
        # Add button to left side - takes up available space
        sizer.Add(self.button, 1, wx.EXPAND)
        
        # Add message box to right side - takes up available space  
        sizer.Add(self.message_box, 1, wx.EXPAND)
        
        # Set sizer for panel
        panel.SetSizer(sizer)
        
        # Fit the frame to its contents
        sizer.Fit(self)
        
        # Center the window on screen instead of positioning at (0,0)
        self.Center()
        
        # Optional: Set minimum size
        self.SetMinSize(self.GetSize())
        
        # Refresh layout
        self.Layout()
        
        icon = wx.Icon("./assets/favicon.ico", wx.BITMAP_TYPE_ICO) 
        self.SetIcon(icon)
        
        # Show the window
        self.Show()

    def update_message_box(self, text):
        # Callback function to update the message box with OCR results
        self.message_box.SetValue(text)
        # Scroll to the end to show the latest text
        self.message_box.SetInsertionPointEnd()

    def on_button_click(self, event):
        if not self.running:
            # --- Start OCR ---
            size = self.button.Size
            x1, y1 = self.button.GetScreenPosition()
            x2, y2 = x1 + size[0], y1 + size[1]

            self.translator = Translator(callback=self.update_message_box)
            self.ocr_thread = threading.Thread(
                target=self.translator.start_reading, args=(x1, y1, x2, y2)
            )
            self.ocr_thread.daemon = True
            self.ocr_thread.start()

            self.running = True
        else:
            # --- Stop OCR ---
            if self.translator:
                self.translator.stop()
            self.running = False


    def OnQuit(self, e):
        if self.translator:
            self.translator.stop()
        self.Close()


def main():
    app = wx.App()
    mf = DesktopController(None, title="OCR Translator")
    app.MainLoop()


if __name__ == '__main__':
    main()