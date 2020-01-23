class Enigma:
    punctuation = [" ", ",", ".", ":", ";", "'", '"', "!", "?"]

    def __init__(self, rotors_list, deflector, letters_list, uppercase, lowercase, plug_board):
        self.rotors = rotors_list
        self.deflector = deflector
        self.rotors_no = len(rotors_list)
        self.letters_list = letters_list
        self.letters_no = len(letters_list)
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.name = Enigma.get_name(self.rotors_no)
        self.plugs = plug_board

    @staticmethod
    def get_name(n):
        '''names the Enigma object'''
        name = "M3"
        if n != 3:
            name += " based"
        return name

    def add_shifts(self):
        '''moves the latter Rotors if required'''
        temp = True
        for i in range(self.rotors_no-1):
            if temp:
                temp = Rotor.add_shift(self.rotors[i])
        if self.rotors[self.rotors_no-1].shift_add == self.letters_no:
            self.rotors[self.rotors_no-1].shift_add = 0

    def encrypt_sign(self, sign):
        '''encrypts one given sign - the main functionality of this program'''
        if sign in list(self.plugs.keys()):
            sign = self.plugs[sign]
        for i in range(self.rotors_no):
            sign = Rotor.encrypt_sign(self.rotors[i], sign)
        sign = Deflector.encrypt_sign(self.deflector, sign)
        for i in range(self.rotors_no-1, -1, -1):
            sign = Rotor.decrypt_sign(self.rotors[i], sign)
        if sign in list(self.plugs.keys()):
            sign = self.plugs[sign]
        Enigma.add_shifts(self)
        return sign

    def encrypt_key(self, sign, encrypted_text, raw_text=""):
        '''encrypts a single sign if conditions are met'''
        unknown = False
        # converts unsupported lowercases to an uppercase
        if sign.islower() and sign not in self.lowercase:
            sign = chr(ord(sign)-32)
        if sign.isupper() and sign not in self.uppercase:
            sign = chr(ord(sign)+32)
        if sign in self.letters_list:
            raw_text += sign
            sign = Enigma.encrypt_sign(self, sign)
            encrypted_text += sign
            # n is just an integer used to format encrypted_text
            temp = len(encrypted_text.replace(' ', '').replace('\n', ''))
            if temp % 80 == 0:
                encrypted_text += "\n"
            elif temp % 5 == 0:
                encrypted_text += " "
        elif sign in Enigma.punctuation:
            raw_text += sign
        # returns True if the sign is not on a Rotor nor in punctuation
        else:
            unknown = True
        return encrypted_text, unknown, raw_text

    def encrypt_text(self, raw_text):
        '''encrypts a given file_name using a given Enigma object'''
        cypher, if_unknown = '', 0
        for sign in range(len(raw_text)):
            current_sign = raw_text[sign]
            cypher, unknown, _ = Enigma.encrypt_key(self, current_sign, cypher)
            if unknown:
                if_unknown = True
        return cypher, if_unknown

    @staticmethod
    def open_file(file_name):
        '''makes a one string from the whole given file'''
        with open(file_name, "r") as file:
            raw_file = [line.rstrip() for line in file]
        return ''.join(raw_file)

    @staticmethod
    def create_file(text, path=''):
        '''makes a file "output.txt" from the given text'''
        with open(path+"output.txt", "w+") as out_file:
            out_file.write(text)

    def __str__(self):
        return f"This {self.name} Enigma emulation uses {', '.join([self.rotors[i].name for i in range(self.rotors_no)])} rotors and the {self.deflector.name} deflector"


class Rotor:
    def __init__(self, name, letters_list, shift_beginning):
        self.name = name
        self.letters = letters_list
        self.alphabet = letters_list.copy()
        self.alphabet.sort()
        self.length = len(self.alphabet)
        self.shift_beg = shift_beginning % self.length
        self.shift_add = 0

    def encrypt_sign(self, sign):
        '''encrypts one given sign - the main functionality of this program'''
        for j in range(self.length):
            if sign == self.alphabet[j]:
                return self.letters[(j+self.get_shift()) % self.length]

    def decrypt_sign(self, sign):
        '''decrypts one given sign - the main functionality of this program'''
        for j in range(self.length):
            if sign == self.letters[j]:
                return self.alphabet[(j-self.get_shift()) % self.length]

    def get_shift(self):
        '''returns a combined shift valeu'''
        return self.shift_add + self.shift_beg

    def add_shift(self):
        '''moves this Rotor by one and returns true if the next Rotor should move'''
        self.shift_add += 1
        if self.shift_add == self.length:
            self.shift_add = 0
            return True
        return False

    @staticmethod
    def get_name(n, file_rotors):
        '''names the Rotor object'''
        if file_rotors == "Rotors/default.txt":
            rotor_names = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
            name = rotor_names[n-1]
        else:
            name = f"{n}"
            n %= 10
            if n == 1:
                name += "st"
            elif n == 2:
                name += "nd"
            elif n == 3:
                name += "rd"
            else:
                name += "th"
        return name

    def __str__(self):
        return f"This {self.name} rotor ({' '.join(self.letters)}) is being shifted by {Rotor.get_shift(self)}"


class Deflector(Rotor):
    def __init__(self, name, letters_list):
        self.name = name
        self.letters = letters_list
        self.alphabet = letters_list.copy()
        self.alphabet.sort()
        self.length = len(self.alphabet)

    def encrypt_sign(self, sign):
        '''encrypts one given sign - the main functionality of this program'''
        for i in range(self.length):
            if sign == self.alphabet[i]:
                return self.letters[i]

    @staticmethod
    def get_name(n, file_rotors):
        '''names the Deflector object'''
        name = Rotor.get_name(n, file_rotors)
        if file_rotors == "Rotors/default.txt":
            deflector_names = ['UKW B', 'UKW C']
            name = deflector_names[n-1]
        return name

    def __str__(self):
        return f"This is a {self.name} deflector ({' '.join(self.letters)})"


class Create():
    def split_list(a_type, a_list):
        '''splits a string into a list of signs of given type'''
        return list(map(a_type, a_list.split()))

    def check_case(letters):
        '''returns two lists of the uppercase and the lowercase letters used on the rotors'''
        used_uppercase, used_lowercase = [], []
        for i in range(len(letters)):
            if letters[i].isupper():
                used_uppercase.append(letters[i])
            elif letters[i].islower():
                used_lowercase.append(letters[i])
        return used_uppercase, used_lowercase

    def check_plugs(plug_list):
        plug_amount = len(plug_list)
        plug_board = {}
        while plug_amount > 0:
            plug_board.update({plug_list[0][0]: plug_list[0][1]})
            plug_board.update({plug_list[0][1]: plug_list[0][0]})
            del plug_list[0]
            plug_amount -= 1
        return plug_board

    def raise_select(file, rotors_select, rotors_amount, deflectors_amount, desired_amount):
        '''raises all the Exceptions that can occur in rotors config file'''
        if rotors_amount < desired_amount:
            raise Exception(f"There are less rotors in {file} ({rotors_amount}) than the requested amount ({desired_amount})")
        if max(rotors_select) > rotors_amount:
            raise Exception(f"The requested number of rotor ({max(rotors_select)}) is higher than the given amount of them ({rotors_amount})")
        if rotors_select[desired_amount] > deflectors_amount:
            raise Exception(f"The requested number of deflector ({rotors_select[desired_amount]}) is higher than the given amount of them ({deflectors_amount})")

    def raise_rotors(rotors_amount, rotors_list, deflector, letters_list):
        '''raises all the Exceptions that can occur in select config file'''
        if len(deflector.letters) % 2 != 0:
            raise Exception(f"The number of signs in the deflector {deflector.name} ({len(deflector.letters)}) is not even")
        for i in range(rotors_amount):
            if deflector.length != rotors_list[i].length:
                raise Exception(f"The amount of signs in Rotor {rotors_list[i].name} ({len(rotors_list[i].letters)}) does not match the number of signs in the deflector {deflector.name} ({len(deflector.letters)})")
            for j in range(rotors_list[i].length):
                if rotors_list[i].alphabet[j] != letters_list[j]:
                    raise Exception(f"On the {rotors_list[i].name} rotor, the sign {rotors_list[i].alphabet[j]} should appear once, but it does not (or there is a similar issue with possibly different sign in the {rotors_list[0].name} rotor)")
        for i in range(len(letters_list)):
            for j in range(len(letters_list)):
                if deflector.letters[i] == letters_list[j]:
                    if deflector.letters[j] != letters_list[i]:
                        raise Exception(f"The {deflector.name} deflector is not properly created (it should swap two signs with eachother)")

    def raise_plugs(plug_list, alphabet):
        '''raises all the Exceptions that can occur in select config file for plugs'''
        added = []
        for i in range(len(plug_list)):
            if len(plug_list[i]) != 2:
                raise Exception(f"There should be 2 adjacent sign in {plug_list[i]} instead of {len(plug_list[i])}")
            if plug_list[i][0] not in alphabet:
                raise Exception(f"There sign {plug_list[i][0]} from {plug_list[i]} is not included in your rotors")
            if plug_list[i][1] not in alphabet:
                raise Exception(f"There sign {plug_list[i][1]} from {plug_list[i]} is not included in your rotors")
            if plug_list[i][0] in added:
                raise Exception(f"The sign {plug_list[i][0]} is present multiple times on your plugboard")
            if plug_list[i][1] in added:
                raise Exception(f"The sign {plug_list[i][1]} is present multiple times on your plugboard")
            added.append(plug_list[i][0])
            added.append(plug_list[i][1])

    def open_config(file_rotors, file_select):
        '''transforms configuration files into variables readable by Enigma class'''
        with open(file_select, "r") as file:
            select = [Create.split_list(str, line.rstrip()) for line in file]
        for i in range(len(select[0])):
            select[0][i] = int(select[0][i])
        for i in range(len(select[1])):
            select[1][i] = int(select[1][i])
        with open(file_rotors, "r") as file:
            rotors = [line.rstrip() for line in file]
        amount_list = Create.split_list(int, rotors[0])
        amount_list.append(len(select[0]) - 1)
        # amount_list = rotors, deflectors, desired_of_rotors
        Create.raise_select(file_rotors, select[0], *amount_list)
        rotors_list = [Rotor(
            Rotor.get_name(select[0][i], file_rotors), Create.split_list(
                str, rotors[select[0][i]]), select[1][i]) for i in range(amount_list[2])]
        deflector = Deflector(
            Deflector.get_name(select[0][amount_list[2]], file_rotors), Create.split_list(
                str, rotors[amount_list[0]+select[0][amount_list[2]]]))
        letters_list = rotors_list[0].letters.copy()
        letters_list.sort()
        if len(select) > 2:
            Create.raise_plugs(select[2], letters_list)
            plug_board = Create.check_plugs(select[2])
        else:
            plug_board = {}
        uppercase, lowercase = Create.check_case(letters_list)
        Create.raise_rotors(amount_list[2], rotors_list, deflector, letters_list)
        return rotors_list, deflector, letters_list, uppercase, lowercase, plug_board


def main():
    '''the main function of the program launching the Enigma without libraries or inputs,
    encrypting the text in output.txt using default settings'''
    markM3 = Enigma(*Create.open_config("Rotors/default.txt", "Select/default.txt"))
    raw_text = Enigma.open_file("output.txt")
    encrypted_text, _ = Enigma.encrypt_text(markM3, raw_text)
    Enigma.create_file(encrypted_text)


if __name__ == "__main__":
    main()
