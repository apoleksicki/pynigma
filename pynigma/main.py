'''
Created on 21/07/2013

@author: Antek
'''

import pygtk
pygtk.require('2.0')
import gtk
from pynigma import Machine, rotorI, rotorII, rotorIII

class PynimgaUI(object):
    
    def close_application(self, widget):
        gtk.main_quit()
    
    def __init__(self):
        self.letterCounter = 0
        self.rI = rotorI()
        self.rII = rotorII()
        self.rIII = rotorIII()
        self.machine = Machine([self.rI, self.rII, self.rIII])
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(True)  
        window.connect('destroy', self.close_application)
        window.set_title('Pynigma')
        window.set_border_width(0)
        window.set_size_request(200, 200)
        
        textviewRotorI, self.rotorI_updater = self._textselfView_and_updater_for_rotor(self.rI)
        textviewRotorII, self.rotorII_updater = self._textselfView_and_updater_for_rotor(self.rII)
        textviewRotorIII, self.rotorIII_updater = self._textselfView_and_updater_for_rotor(self.rIII)
        
        textviewEncoded = gtk.TextView()
        textviewEncoded.set_editable(False)
        textviewEncoded.set_cursor_visible(False)
        
        textviewPlain = gtk.TextView()
        textviewPlain.set_editable(False)
        textviewPlain.set_cursor_visible(False)
        
        labelEncoded = gtk.Label('Encoded')
        labelPlain = gtk.Label('Plain')
        
        
        rotorbox = gtk.HBox(True, 0)
        label = gtk.Label('fooooooooooooooooooooo')
        rotorbox.pack_start(label, fill = True, expand = True)
        label.show()
        
        rotorbox.pack_start(textviewRotorI, fill = False, expand = False)
        rotorbox.pack_start(textviewRotorII, fill = False, expand = False)
        rotorbox.pack_start(textviewRotorIII, fill = False, expand = False)
        
        box = gtk.VBox(False, 0)
        box.pack_start(rotorbox, fill = False, expand = False)
        
        encodedBox = gtk.HBox(False, 0)
        box.pack_start(labelEncoded)
        box.pack_start(textviewEncoded)
        box.pack_start(labelPlain)
        box.pack_start(textviewPlain)
        
        textviewRotorI.show()
        textviewRotorII.show()
        textviewRotorIII.show()
        
        
        rotorbox.show()
        labelEncoded.show()
        textviewEncoded.show()
        labelPlain.show()
        textviewPlain.show()
        window.add(box)
        box.show()
        self.textbufferRotor1 = textviewRotorI.get_buffer()
        self.textbufferEncoded = textviewEncoded.get_buffer()
        self.textbufferPlain= textviewPlain.get_buffer()
        self.iterEncoded = self.textbufferEncoded.get_end_iter()
        self.iterPlain = self.textbufferPlain.get_end_iter()
        
        window.connect('key_press_event', self._printChar)
        window.show()


    def _textselfView_and_updater_for_rotor(self, rotor):
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_border_color('red')
        textbuffer = textview.get_buffer()
        updater = lambda: textbuffer.set_text(rotor.getPosition())
        updater.__call__()
        return (textview, updater)


    def _printChar(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if len(keyname) == 1:
            self.textbufferEncoded.insert(self.iterEncoded, self.machine.encode(keyname.upper()))
            self.textbufferPlain.insert(self.iterPlain,  keyname.upper())
            self.letterCounter += 1
            self.rotorI_updater.__call__()
            self.rotorII_updater.__call__()
            self.rotorIII_updater.__call__()
            
            if self.letterCounter == 5:
                self.letterCounter = 0
                self.textbufferEncoded.insert(self.iterEncoded, ' ')
                self.textbufferPlain.insert(self.iterPlain, ' ')


        
    
        
if __name__ == '__main__':
    PynimgaUI()
    gtk.main()
