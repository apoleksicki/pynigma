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
        self.updaters = []
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_resizable(True)  
        window.connect('destroy', self.close_application)
        window.set_title('Pynigma')
        window.set_border_width(0)
        window.set_size_request(200, 200)
        
        textviewRotorI = self._textselfView_and_updater_for_rotor(self.rI)
        textviewRotorII = self._textselfView_and_updater_for_rotor(self.rII)
        textviewRotorIII = self._textselfView_and_updater_for_rotor(self.rIII)
        
        
        
        outputBox, self.textbufferOutput = self._createTextview('Output')
        inputBox, self.textbufferInput = self._createTextview('Input')
        
        rotorbox = gtk.HBox(False, 0)
        label = gtk.Label('Rotors: ')
        rotorbox.pack_start(label, fill = True, expand = True)
        label.show()
        
        rotorbox.pack_start(textviewRotorI, fill = False, expand = False)
        rotorbox.pack_start(textviewRotorII, fill = False, expand = False)
        rotorbox.pack_start(textviewRotorIII, fill = False, expand = False)
        
        box = gtk.VBox(False, 0)
        box.pack_start(rotorbox, fill = False, expand = False)
        
        box.pack_start(outputBox, expand = False)
        box.pack_start(inputBox, expand = False)
        
        textviewRotorI.show()
        textviewRotorII.show()
        textviewRotorIII.show()
        
        
        rotorbox.show()
        window.add(box)
        box.show()
        self.iterOutput = self.textbufferOutput.get_end_iter()
        self.iterInput = self.textbufferInput.get_end_iter()
        
        window.connect('key_press_event', self._printChar)
        window.show()


    def _textselfView_and_updater_for_rotor(self, rotor):
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_border_width(5)
        textbuffer = textview.get_buffer()
        updater = lambda: textbuffer.set_text(rotor.getPosition())
        updater.__call__()
        self.updaters.append(updater)
        return textview
        
    def _printChar(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if len(keyname) == 1:
            self.textbufferOutput.insert(self.iterOutput, self.machine.encode(keyname.upper()))
            self.textbufferInput.insert(self.iterInput,  keyname.upper())
            self.letterCounter += 1
            [updater.__call__() for updater in self.updaters ]
            
            if self.letterCounter == 5:
                self.letterCounter = 0
                self.textbufferOutput.insert(self.iterOutput, ' ')
                self.textbufferInput.insert(self.iterInput, ' ')
    
    def _createTextview(self, labelText):
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        label = gtk.Label(labelText)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(textview)
        sw.show()
        label.show()
        textview.show()
        box = gtk.VBox(False, 0)
        box.add(label)
        box.add(sw)
        box.show()
        return (box, textview.get_buffer())


        


        
    
        
if __name__ == '__main__':
    PynimgaUI()
    gtk.main()
