"""
Created on 15/06/2013

@author: Antek
"""

from typing import Callable, ClassVar

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
    NUMBER_OF_CHARACTERS: ClassVar[int] = 26
    LETTER_NUMBER_MAP: ClassVar[dict[str, int]] = {
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

    NUMBER_LETTER_MAP: ClassVar[dict[int, str]] = {
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

    def __init__(self, order: tuple, turnover_position: str = "A") -> None:
        self._order = list(order)
        self.turnover_position = turnover_position
        self._position = 0

    def turnover(self) -> None:
        self._order.append(self._order.pop(0))
        self._position += 1
        if self._position == Rotor.NUMBER_OF_CHARACTERS:
            self._position = 0

    def set_position(self, position: str) -> None:
        while Rotor.LETTER_NUMBER_MAP[position] != self._position:
            self.turnover()

    def encode_left(self, letter: str) -> str:
        as_number = Rotor.LETTER_NUMBER_MAP[letter]
        as_letter = Rotor.NUMBER_LETTER_MAP[
            self._calculate_offset(as_number + self._position)
        ]
        return Rotor.NUMBER_LETTER_MAP[self._order.index(as_letter)]

    def encode_right(self, letter: str) -> str:
        mapped = self._order[Rotor.LETTER_NUMBER_MAP[letter]]  # d
        with_offset = Rotor.LETTER_NUMBER_MAP[mapped] - self._position
        return Rotor.NUMBER_LETTER_MAP[self._calculate_offset(with_offset)]

    def get_position(self) -> str:
        return Rotor.NUMBER_LETTER_MAP[self._position]

    def _calculate_offset(self, position: int) -> int:
        if position < 0:
            return Rotor.NUMBER_OF_CHARACTERS - abs(position)
        elif position >= Rotor.NUMBER_OF_CHARACTERS:
            return position - Rotor.NUMBER_OF_CHARACTERS
        else:
            return position


def rotor_i() -> Rotor:
    return Rotor(WIRING_I, TURNOVER_POSITION_I)


def rotor_ii() -> Rotor:
    return Rotor(WIRING_II, TURNOVER_POSITION_II)


def rotor_iii() -> Rotor:
    return Rotor(WIRING_III, TURNOVER_POSITION_III)


class Machine(object):
    def __init__(
        self, rotors: list[Rotor], reflector: dict[str, str] = REFLECTOR_B
    ) -> None:
        self.rotors = rotors
        self._reflector = reflector

    def _send_through_rotors_left(self, letter: str) -> str:
        return self._send_through_rotors(
            letter, self.rotors, lambda rotor, letter: rotor.encode_left(letter)
        )

    def _send_through_rotors_right(self, letter: str) -> str:
        return self._send_through_rotors(
            letter, self.rotors[::-1], lambda rotor, letter: rotor.encode_right(letter)
        )

    def _send_through_rotors(
        self,
        letter: str,
        rotors: list[Rotor],
        encoding_function: Callable[[Rotor, str], str],
    ) -> str:
        if len(rotors) == 1:
            return encoding_function(rotors[0], letter)
        else:
            return self._send_through_rotors(
                encoding_function(rotors[0], letter), rotors[1:], encoding_function
            )

    def _rotate(self) -> None:
        if self.rotors[1].get_position() == self.rotors[1].turnover_position:
            self.rotors[0].turnover()
            self.rotors[1].turnover()

        if self.rotors[2].get_position() == self.rotors[2].turnover_position:
            self.rotors[1].turnover()

        self.rotors[2].turnover()

    def encode(self, letter: str) -> str:
        self._rotate()
        encoded_right = self._send_through_rotors_right(letter)
        reflected = self._reflector[encoded_right]
        return self._send_through_rotors_left(reflected)

    def adjust_rotor(self, rotor_number: int, position: str) -> None:
        self.rotors[rotor_number].set_position(position)


if __name__ == "__main__":  # pragma: no cover
    machine = Machine([rotor_i(), rotor_ii(), rotor_iii()])
    result = ""
    for c in "ANTONIPIOTROLEKSICKI":
        result += machine.encode(c)
    print(result)
