import unittest

from pynigma.pynigma import rotorI, rotorII, rotorIII, Machine


class MachineTest(unittest.TestCase):
    def setUp(self):
        self.machine = Machine([rotorI(), rotorII(), rotorIII()])

    def test_sendThroughRotorsRight(self):
        self.assertEqual("Z", self.machine._sendThroughRotorsRight("A"))
        self.assertEqual("Y", self.machine._sendThroughRotorsRight("O"))

    def test_sendThroughRotorsLeft(self):
        self.assertEqual("R", self.machine._sendThroughRotorsLeft("G"))

        self.assertEqual("O", self.machine._sendThroughRotorsLeft("Y"))

    def testEncode(self):
        self.assertEqual("B", self.machine.encode("A"))

    def testEncodeZZZ(self):
        self.machine.adjustRotor(0, "Z")
        self.machine.adjustRotor(1, "Z")
        self.machine.adjustRotor(2, "Z")
        self.assertEqual("E", self.machine.encode("A"))

    def testDoubleStep(self):
        self.machine.adjustRotor(0, "A")
        self.machine.adjustRotor(1, "D")
        self.machine.adjustRotor(2, "U")
        self.assertEqual("E", self.machine.encode("A"))
        self.printRotorPositions()
        toAssert = self.machine.encode("P")
        self.printRotorPositions()
        self.assertEqual("G", toAssert)
        self.assertEqual("V", self.machine.encode("O"))
        self.assertEqual("B", self.machine.rotors[0].getPosition())
        self.assertEqual("F", self.machine.rotors[1].getPosition())
        self.assertEqual("X", self.machine.rotors[2].getPosition())

    def printRotorPositions(self):
        print(
            "rotorI: %s, rotorII: %s, rotorIII: %s"
            % (
                self.machine.rotors[0].getPosition(),
                self.machine.rotors[1].getPosition(),
                self.machine.rotors[2].getPosition(),
            )
        )


class TurnoverTest(unittest.TestCase):
    def setUp(self):
        self.rotors = [rotorI(), rotorII(), rotorIII()]
        self.machine = Machine(self.rotors)

    def testNormalSequence(self):
        print("test rotate")
        self.rotors[2].setPosition("Z")
        self.assertEqual("U", self.machine.encode("A"))
        self.assertEqual("B", self.machine.encode("A"))


class RotorTest(unittest.TestCase):
    def setUp(self):
        self.rotor = rotorI()

    def testEncodeLeft(self):
        self.assertEqual("U", self.rotor.encodeLeft("A"))
        self.assertEqual("W", self.rotor.encodeLeft("B"))

    def testEncodeRight(self):
        self.assertEqual("E", self.rotor.encodeRight("A"))
        self.assertEqual("K", self.rotor.encodeRight("B"))

    def testTurnover(self):
        self.assertEqual("U", self.rotor.encodeLeft("A"))
        self.assertEqual("E", self.rotor.encodeRight("A"))

        self.rotor.turnover()
        self.assertEqual("V", self.rotor.encodeLeft("A"))
        self.assertEqual("J", self.rotor.encodeRight("A"))
        self.rotor.turnover()
        self.assertEqual("W", self.rotor.encodeLeft("A"))
        self.assertEqual("K", self.rotor.encodeRight("A"))
