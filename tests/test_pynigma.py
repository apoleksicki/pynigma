import unittest

from pynigma.pynigma import Machine, rotor_i, rotor_ii, rotor_iii


class MachineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.machine = Machine([rotor_i(), rotor_ii(), rotor_iii()])

    def test_send_through_rotors_right(self) -> None:
        self.assertEqual("Z", self.machine._send_through_rotors_right("A"))
        self.assertEqual("Y", self.machine._send_through_rotors_right("O"))

    def test_send_through_rotors_left(self) -> None:
        self.assertEqual("R", self.machine._send_through_rotors_left("G"))

        self.assertEqual("O", self.machine._send_through_rotors_left("Y"))

    def test_encode(self) -> None:
        self.assertEqual("B", self.machine.encode("A"))

    def test_encode_zzz(self) -> None:
        self.machine.adjust_rotor(0, "Z")
        self.machine.adjust_rotor(1, "Z")
        self.machine.adjust_rotor(2, "Z")
        self.assertEqual("E", self.machine.encode("A"))

    def test_double_step(self) -> None:
        self.machine.adjust_rotor(0, "A")
        self.machine.adjust_rotor(1, "D")
        self.machine.adjust_rotor(2, "U")
        self.assertEqual("E", self.machine.encode("A"))
        self.print_rotor_positions()
        to_assert = self.machine.encode("P")
        self.print_rotor_positions()
        self.assertEqual("G", to_assert)
        self.assertEqual("V", self.machine.encode("O"))
        self.assertEqual("B", self.machine.rotors[0].get_position())
        self.assertEqual("F", self.machine.rotors[1].get_position())
        self.assertEqual("X", self.machine.rotors[2].get_position())

    def print_rotor_positions(self) -> None:
        print(
            "rotorI: %s, rotorII: %s, rotorIII: %s"
            % (
                self.machine.rotors[0].get_position(),
                self.machine.rotors[1].get_position(),
                self.machine.rotors[2].get_position(),
            )
        )


class TurnoverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rotors = [rotor_i(), rotor_ii(), rotor_iii()]
        self.machine = Machine(self.rotors)

    def test_normal_sequence(self) -> None:
        print("test rotate")
        self.rotors[2].set_position("Z")
        self.assertEqual("U", self.machine.encode("A"))
        self.assertEqual("B", self.machine.encode("A"))


class RotorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rotor = rotor_i()

    def test_encode_left(self) -> None:
        self.assertEqual("U", self.rotor.encode_left("A"))
        self.assertEqual("W", self.rotor.encode_left("B"))

    def test_encode_right(self) -> None:
        self.assertEqual("E", self.rotor.encode_right("A"))
        self.assertEqual("K", self.rotor.encode_right("B"))

    def test_turnover(self) -> None:
        self.assertEqual("U", self.rotor.encode_left("A"))
        self.assertEqual("E", self.rotor.encode_right("A"))

        self.rotor.turnover()
        self.assertEqual("V", self.rotor.encode_left("A"))
        self.assertEqual("J", self.rotor.encode_right("A"))
        self.rotor.turnover()
        self.assertEqual("W", self.rotor.encode_left("A"))
        self.assertEqual("K", self.rotor.encode_right("A"))
