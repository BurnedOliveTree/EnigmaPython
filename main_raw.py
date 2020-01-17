import os
import sys
from simple import Enigma, Create
from main import Initiate

sys.tracebacklimit = 0


class InitiateRaw():
    def select_name(standard, path):
        # general function to let user type in the names of the config files
        input_name = input()
        if input_name == '':
            input_name = standard
        if_file = False
        if "." in input_name:
            input_name = path + input_name
            if_file = True
        return input_name, if_file

    def choose_rotors():
        # lets user create or choose variables to create a rotor config file
        InitiateRaw.clean_choose("Alphabets", "alphabet", "the alphabet")
        file_name, temp = InitiateRaw.select_name("", "Alphabets/")
        file_name, alphabet = Initiate.create_alphabet(file_name, temp)
        os.system('cls' if os.name == 'nt' else 'clear')
        rotors = input("Please enter the desired number of rotors to create:\n\n")
        Initiate.create_rotors(file_name, alphabet, rotors)
        return file_name

    def clean_choose(path, info1, info2):
        # a method cleanly showing all the required information in a "choose" methods to a user
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please enter the name of a file", end='')
        print(f"{' in ' if len(path) > 0 else ''}{path} containing "+info2+"\n")
        if len(info1) > 0:
            print("you can also create your own "+info1+" from here")
        print("(leave blank for the default file name and do not forget the extension)\n")
        if len(path) > 0:
            print(f"Avaible {path}: {', '.join(os.popen(f'ls {path}').read().split())}\n")

    def choose_config():
        # get file_name for Enigma configuration file from user
        InitiateRaw.clean_choose("Rotors", "file from chosen alphabet", "rotors and deflectors")
        file_rotors, temp = InitiateRaw.select_name("default.txt", "Rotors/")
        if not temp:
            file_rotors = InitiateRaw.choose_rotors()
        InitiateRaw.clean_choose("Select", "select file", "information about the chosen rotors")
        file_select, temp = InitiateRaw.select_name("default.txt", "Select/")
        if not temp:
            file_select = Initiate.create_select(file_select)
        return file_rotors, file_select

    def choose_file():
        # get file_name for Enigma configuration file from user
        InitiateRaw.clean_choose("", "", "text to decrypt")
        file_name, _ = InitiateRaw.select_name("standard", "")
        return file_name

    def encrypt_input(markM3):
        # initiates Enigma object from given file_config and runs the simulation
        cypher = ''
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Enigma.__str__(markM3)+'\n')
        raw_text = input("input from keyboard:\n")
        unknown = False
        for i in range(len(raw_text)):
            cypher, unknown, _ = Enigma.encrypt_key(markM3, raw_text[i], cypher)
        return cypher, unknown

    def create_file_info(encrypted_text, unknown):
        # informs about succesful creation of file in create_file
        os.system('cls' if os.name == 'nt' else 'clear')
        print("File containing encrypted text succesfully created")
        if unknown:
            print("\nYour file contained signs, that were neither on the rotor", end='')
            print(" nor a punctuation and since has been omitted")
        print("\nSaved text:\n"+encrypted_text)

    def main():
        # launches all the necessary smaller functions
        # initiates Enigma object from given file_names
        markM3 = Enigma(*Create.open_config(*InitiateRaw.choose_config()))
        file_name = InitiateRaw.choose_file()
        if file_name == "standard":
            encrypted_text, unknown = InitiateRaw.encrypt_input(markM3)
        else:
            encrypted_text, unknown = Enigma.encrypt_file(markM3, file_name)
        Enigma.create_file(encrypted_text)
        InitiateRaw.create_file_info(encrypted_text, unknown)


if __name__ == "__main__":
    InitiateRaw.main()
