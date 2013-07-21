'''
Created on 21/07/2013

@author: Antek
'''

import pygtk
pygtk.require('2.0')
import gtk

class PynimgaUI(object):
    
    def close_application(self, widget):
        gtk.main_quit()
    
    def __init__(self):
        self.letterCounter = 0
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(True)  
        window.connect('destroy', self.close_application)
        window.set_title('TextView Widget Basic Example')
        window.set_border_width(0)
        
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        window.add(textview)
        self.textbuffer = textview.get_buffer()
        self.iter = self.textbuffer.get_end_iter()
        
        textview.show()
        window.connect('key_press_event', self._printChar)
        window.show()


    def _printChar(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if len(keyname) == 1:
            self.textbuffer.insert(self.iter, keyname.upper())
            self.letterCounter += 1
            if self.letterCounter == 5:
                self.letterCounter = 0
                self.textbuffer.insert(self.iter, ' ')


        
    
        
if __name__ == '__main__':
    PynimgaUI()
    gtk.main()
