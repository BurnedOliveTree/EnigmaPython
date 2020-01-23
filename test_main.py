from main import Initiate
from simple import Enigma, Create
import pytest


class Tests():
    name = "output.txt"  # default_file
    select = "Select/default.txt"  # default_select
    rotors = "Rotors/default.txt"  # default_rotors

    ''' E N I G M A '''
    def test_encrypt_text(self):
        temp_one = ["ABCDE"]
        markM3 = Enigma(*Create.open_config(Tests.rotors, Tests.select))
        with open(Tests.name, "w+") as out_file:
            out_file.write(temp_one[0])
        raw_text = Enigma.open_file(Tests.name)
        Enigma.encrypt_text(markM3, raw_text)
        raw_text = Enigma.open_file(Tests.name)
        Enigma.encrypt_text(markM3, raw_text)
        with open(Tests.name, "r") as file_select:
            temp_two = [line.rstrip() for line in file_select]
        assert temp_one == temp_two

    ''' C R E A T E '''
    def test_split_list(self):
        assert ["A", "B", "C"] == Create.split_list(str, "A B C")
        assert [1, 2, 3] == Create.split_list(int, "1 2 3")

    def test_check_case(self):
        assert ["A", "B", "C"], ["d"] == Create.check_case(["1", "A", "B", "C", "d"])

    def test_raise_select(self):
        with pytest.raises(Exception):
            Create.raise_select("name", [6, 3, 1], 5, 1, 3)
        with pytest.raises(Exception):
            Create.raise_select("name", [1, 2, 3, 4, 5, 2], 5, 1, 3)
        with pytest.raises(Exception):
            Create.raise_select("name", [3, 2, 3], 5, 1, 3)

    def test_raise_rotors(self):
        Initiate.create_select("1 3 5 1 0 0 0")
        rotors_list, deflector, letters_list, uppercase, lowercase, plug_board = Create.open_config("Rotors/ABCdef.txt", "Select/temporary.txt")
        deflector.letters.append("A")
        with pytest.raises(Exception):
            Create.raise_rotors(3, rotors_list, deflector, letters_list)
        del deflector.letters[-1]
        rotors_list[0].length += 1
        with pytest.raises(Exception):
            Create.raise_rotors(3, rotors_list, deflector, letters_list)
        rotors_list[0].length -= 1
        rotors_list[0].alphabet[1] = "A"
        with pytest.raises(Exception):
            Create.raise_rotors(3, rotors_list, deflector, letters_list)
        rotors_list[0].alphabet[1] = "B"
        deflector.letters[0] = "A"
        with pytest.raises(Exception):
            Create.raise_rotors(3, rotors_list, deflector, letters_list)

    def test_raise_plugs(self):
        with pytest.raises(Exception):
            Create.raise_plugs(["ABCE", "TD"], ["ABCDET"])
        with pytest.raises(Exception):
            Create.raise_plugs(["AB", "TD"], ["ABCD"])
        with pytest.raises(Exception):
            Create.raise_plugs(["AB", "CD", "AE"], ["ABCDEF"])

    def test_open_config(self):
        Initiate.create_select("1 3 5 1 0 0 0 AB")
        rotors_list, deflector, letters_list, uppercase, lowercase, plug_board = Create.open_config("Rotors/ABCdef.txt", "Select/temporary.txt")
        assert letters_list == ['A', 'B', 'C', 'd', 'e', 'f']
        assert uppercase == ['A', 'B', 'C']
        assert lowercase == ['d', 'e', 'f']
        assert plug_board["A"] == "B"
        assert plug_board["B"] == "A"

    ''' I N I T I A T E '''
    def test_open_alphabet(self):
        assert ['A', 'B', 'C', 'D'] == Initiate.open_alphabet("Alphabets/ABCD.txt")

    def test_create_rotors(self):
        alphabet = ["A", "B", "C", "D"]
        Initiate.create_rotors("Rotors/temporary.txt", alphabet, 5)
        with open("Rotors/temporary.txt", "r") as file_select:
            temp = [line.rstrip() for line in file_select]
        assert temp[0] == "5 1"
        assert temp[1][0] in alphabet
        assert temp[2][0] in alphabet
        assert temp[3][0] in alphabet
        assert temp[4][0] in alphabet
        assert temp[5][0] in alphabet

    def test_create_select(self):
        Initiate.create_select("1 2 3 1 0 0 0")
        with open("Select/temporary.txt", "r") as file_select:
            temp = [line.rstrip() for line in file_select]
        assert temp[0] == "1 2 3 1"
        assert temp[1] == "0 0 0"


if __name__ == "__main__":
    pass
