'''
Created on 15/06/2013

@author: Antek
'''
import unittest


I_WIRING = ('E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', \
     'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J')
II_WIRING = ('A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', \
      'C', 'Q', 'G', 'Z', 'N', 'P', 'Y', 'F', 'V', 'O', 'E')
III_WIRING = ('B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', \
       'E', 'I', 'W', 'G', 'A', 'K', 'M', 'U', 'S', 'Q', 'O')

I_TURNOVER_POSITION = 'Q'
II_TURNOVER_POSITION = 'E'
III_TURNOVER_POSITION = 'V'

REFLECTOR_B =   {'A':'Y', 'B':'R', 'C':'U', 'D':'H', 'E':'Q', 'F':'S', 'G':'L', 'H':'D', \
                 'I':'P', 'J':'X', 'K':'N', 'L':'G', 'M':'O', 'N':'K', 'O':'M', 'P':'I', \
                 'Q':'E', 'R':'B', 'S':'F', 'T':'Z', 'U':'C', 'V':'W', 'W':'V', 'X':'J', \
                 'Y':'A', 'Z':'T'}


class Rotor(object):
    _letter_number_map = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8, \
                   'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16, \
                   'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}
    
    _number_letter_map = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', \
                   9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 16:'Q', \
                   17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}
    
    def __init__(self, order, turnoverPosition = 'A'):
        self._order = list(order)
        self.turnoverPosition = turnoverPosition
        
    def turnover(self):
        self._order.append(self._order.pop(0))
    
    def encodeRight(self, letter):
        return self._order[Rotor._letter_number_map.get(letter)]
    
    def encodeLeft(self, letter):
        return Rotor._number_letter_map.get(self._order.index(letter))
    
I = Rotor(I_WIRING, I_TURNOVER_POSITION)
II = Rotor(II_WIRING, II_TURNOVER_POSITION)
III = Rotor(III_WIRING, III_TURNOVER_POSITION)

class Machine(object):
    def __init__(self, rotors, reflector = REFLECTOR_B):
        self.rotors = rotors
        self._reflector = reflector
    
    def _sendThroughRotorsRight(self, letter):
        return self._sendThroughRotors(letter, self.rotors[::-1], \
                                        lambda rotor, letter: rotor.encodeRight(letter))
            
    def _sendThroughRotorsLeft(self, letter):
        return self._sendThroughRotors(letter, self.rotors, \
                                        lambda rotor, letter: rotor.encodeLeft(letter))
        
            
    def _sendThroughRotors(self, letter, rotors, encodingFunction):
        
        print '%c -> %c' % (letter, encodingFunction(rotors[0], letter))
                            
        if len(rotors) == 1:
            print ''
            return encodingFunction(rotors[0], letter)
        else:
            return self._sendThroughRotors(encodingFunction(rotors[0], letter), rotors[1:], encodingFunction)

    
    def encode(self, letter):
        encodedRight = self._sendThroughRotorsRight(letter)
        reflected = self._reflector[encodedRight]
        return self._sendThroughRotorsLeft(reflected)
    
        
 
 
class MacineTest(unittest.TestCase):
    
    def setUp(self):
        self.machine = Machine([III, II, I])
        
    def test_sendThroughRotorsRight(self):
        self.assertEqual('G', self.machine._sendThroughRotorsRight('A'))
        self.assertEqual('Y', self.machine._sendThroughRotorsRight('O'))
    
    def test_sendThroughRotorsLeft(self):
        self.assertEqual('A', self.machine._sendThroughRotorsLeft('G'))
        self.assertEqual('O', self.machine._sendThroughRotorsLeft('Y'))
        
    def testEncode(self):
        self.assertEqual('N', self.machine.encode('A'))
        
    
class RotorTest(unittest.TestCase):
             
    def setUp(self):
        self.rotor = I
     
    def testEncodeLeft(self):
        self.assertEqual('U', self.rotor.encodeLeft('A'))
        self.assertEqual('W', self.rotor.encodeLeft('B'))
     
    def testEncodeRight(self):
        self.assertEqual('E', self.rotor.encodeRight('A'))
        self.assertEqual('K', self.rotor.encodeRight('B'))
     
    def testTurnover(self):
        self.assertEqual('U', self.rotor.encodeLeft('A'))
        self.assertEqual('E', self.rotor.encodeRight('A'))
        
        self.rotor.turnover()
        self.assertEqual('T', self.rotor.encodeLeft('A'))
        self.assertEqual('K', self.rotor.encodeRight('A'))
        self.rotor.turnover()
        self.assertEqual('S', self.rotor.encodeLeft('A'))
        self.assertEqual('M', self.rotor.encodeRight('A'))
        
