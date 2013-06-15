'''
Created on 15/06/2013

@author: Antek
'''
import unittest


I = ('E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', \
     'H', 'X', 'U', 'S', 'P', 'A', 'I', 'B', 'R', 'C', 'J')

class Rotor(object):
    _letter_map = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7, 'I':8,\
                   'J':9, 'K':10, 'L':11, 'M':12, 'N':13, 'O':14, 'P':15, 'Q':16,\
                   'R':17, 'S':18, 'T':19, 'U':20, 'V':21, 'W':22, 'X':23, 'Y':24, 'Z':25}
    
    def __init__(self, order):
        self._order = order
        
    def turnover(self):
        self._order.append(self._order.pop(0))
    
    def _encode(self, letter):
        self._order[Rotor._letter_map.get(letter)]
    
class RotorTest(unittest.TestCase):
    def testEncode(self):
        pass