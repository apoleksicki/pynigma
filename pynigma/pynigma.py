"""
Created on 15/06/2013

@author: Antek
"""

WIRING_I = (
    "E",
    "K",
    "M",
    "F",
    "L",
    "G",
    "D",
    "Q",
    "V",
    "Z",
    "N",
    "T",
    "O",
    "W",
    "Y",
    "H",
    "X",
    "U",
    "S",
    "P",
    "A",
    "I",
    "B",
    "R",
    "C",
    "J",
)
WIRING_II = (
    "A",
    "J",
    "D",
    "K",
    "S",
    "I",
    "R",
    "U",
    "X",
    "B",
    "L",
    "H",
    "W",
    "T",
    "M",
    "C",
    "Q",
    "G",
    "Z",
    "N",
    "P",
    "Y",
    "F",
    "V",
    "O",
    "E",
)
WIRING_III = (
    "B",
    "D",
    "F",
    "H",
    "J",
    "L",
    "C",
    "P",
    "R",
    "T",
    "X",
    "V",
    "Z",
    "N",
    "Y",
    "E",
    "I",
    "W",
    "G",
    "A",
    "K",
    "M",
    "U",
    "S",
    "Q",
    "O",
)

TURNOVER_POSITION_I = "Q"
TURNOVER_POSITION_II = "E"
TURNOVER_POSITION_III = "V"

REFLECTOR_B = {
    "A": "Y",
    "B": "R",
    "C": "U",
    "D": "H",
    "E": "Q",
    "F": "S",
    "G": "L",
    "H": "D",
    "I": "P",
    "J": "X",
    "K": "N",
    "L": "G",
    "M": "O",
    "N": "K",
    "O": "M",
    "P": "I",
    "Q": "E",
    "R": "B",
    "S": "F",
    "T": "Z",
    "U": "C",
    "V": "W",
    "W": "V",
    "X": "J",
    "Y": "A",
    "Z": "T",
}


class Rotor(object):
    _number_of_characters = 26
    _letter_number_map = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
        "L": 11,
        "M": 12,
        "N": 13,
        "O": 14,
        "P": 15,
        "Q": 16,
        "R": 17,
        "S": 18,
        "T": 19,
        "U": 20,
        "V": 21,
        "W": 22,
        "X": 23,
        "Y": 24,
        "Z": 25,
    }

    _number_letter_map = {
        0: "A",
        1: "B",
        2: "C",
        3: "D",
        4: "E",
        5: "F",
        6: "G",
        7: "H",
        8: "I",
        9: "J",
        10: "K",
        11: "L",
        12: "M",
        13: "N",
        14: "O",
        15: "P",
        16: "Q",
        17: "R",
        18: "S",
        19: "T",
        20: "U",
        21: "V",
        22: "W",
        23: "X",
        24: "Y",
        25: "Z",
    }

    def __init__(self, order, turnoverPosition="A"):
        self._order = list(order)
        self.turnoverPosition = turnoverPosition
        self._position = 0

    def turnover(self):
        self._order.append(self._order.pop(0))
        self._position += 1
        if self._position == Rotor._number_of_characters:
            self._position = 0

    def setPosition(self, position):
        while Rotor._letter_number_map[position] != self._position:
            self.turnover()

    def encodeLeft(self, letter):
        asNumber = Rotor._letter_number_map[letter]
        asLetter = Rotor._number_letter_map[
            self._calculateOffset(asNumber + self._position)
        ]
        return Rotor._number_letter_map.get(self._order.index(asLetter))

    def encodeRight(self, letter):
        mapped = self._order[Rotor._letter_number_map.get(letter)]  # d
        withOffset = Rotor._letter_number_map[mapped] - self._position
        return Rotor._number_letter_map[self._calculateOffset(withOffset)]

    def getPosition(self):
        return Rotor._number_letter_map[self._position]

    def _calculateOffset(self, position):
        if position < 0:
            return Rotor._number_of_characters - abs(position)
        elif position >= Rotor._number_of_characters:
            return position - Rotor._number_of_characters
        else:
            return position


def rotorI():
    return Rotor(WIRING_I, TURNOVER_POSITION_I)


def rotorII():
    return Rotor(WIRING_II, TURNOVER_POSITION_II)


def rotorIII():
    return Rotor(WIRING_III, TURNOVER_POSITION_III)


class Machine(object):
    def __init__(self, rotors, reflector=REFLECTOR_B):
        self.rotors = rotors
        self._reflector = reflector

    def _sendThroughRotorsLeft(self, letter):
        return self._sendThroughRotors(
            letter, self.rotors, lambda rotor, letter: rotor.encodeLeft(letter)
        )

    def _sendThroughRotorsRight(self, letter):
        return self._sendThroughRotors(
            letter, self.rotors[::-1], lambda rotor, letter: rotor.encodeRight(letter)
        )

    def _sendThroughRotors(self, letter, rotors, encodingFunction):
        if len(rotors) == 1:
            return encodingFunction(rotors[0], letter)
        else:
            return self._sendThroughRotors(
                encodingFunction(rotors[0], letter), rotors[1:], encodingFunction
            )

    def _rotate(self):
        if self.rotors[1].getPosition() == self.rotors[1].turnoverPosition:
            self.rotors[0].turnover()
            self.rotors[1].turnover()

        if self.rotors[2].getPosition() == self.rotors[2].turnoverPosition:
            self.rotors[1].turnover()

        self.rotors[2].turnover()

    def encode(self, letter):
        self._rotate()
        encodedRight = self._sendThroughRotorsRight(letter)
        reflected = self._reflector[encodedRight]
        return self._sendThroughRotorsLeft(reflected)

    def adjustRotor(self, rotorNumber, position):
        self.rotors[rotorNumber].setPosition(position)


if __name__ == "__main__":  # pragma: no cover
    machine = Machine([rotorI(), rotorII(), rotorIII()])
    result = ""
    for c in "ANTONIPIOTROLEKSICKI":
        result += machine.encode(c)
    print(result)
