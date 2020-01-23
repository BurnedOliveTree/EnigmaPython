import curses
from random import sample
from os import popen
import sys
from simple import Enigma, Create

sys.tracebacklimit = 0


class Initiate():
    def select_name(stdscr, y, standard, path):
        '''general function to let user type in the names of the config files'''
        input_key, input_name = 'A', ''
        while input_key != '\n':
            input_key = stdscr.getkey()
            if input_key == '\x7f':
                input_name = input_name[:-1]
                a = len(input_name)
                stdscr.addstr(y, a, chr(32))
            else:
                input_name += input_key
            stdscr.addstr(y, 0, input_name)
        if input_name == '\n':
            input_name = standard
        else:
            input_name = input_name[:-1]
        stdscr.addstr(y, 0, " " * (curses.COLS-1))
        if_file = False
        if "." in input_name:
            input_name = path + input_name
            if_file = True
        return input_name, if_file

    def open_alphabet(file_name):
        '''transforms a file containg alphabet into a list'''
        with open(file_name, "r") as file:
            temp_list = [line.rstrip() for line in file]
            alphabet = []
            for i in range(len(temp_list)):
                alphabet += Create.split_list(str, temp_list[i])
            alphabet.sort()
        return alphabet

    def create_alphabet(file_name, temp):
        '''creates an alphabet from a file or a user given one'''
        if temp:
            alphabet = Initiate.open_alphabet(file_name)
            file_name = file_name[10:]
        else:
            alphabet = file_name.split()
            alphabet.sort()
            file_name = "temporary.txt"
        if len(alphabet) % 2 != 0:
            raise Exception(f"The number of signs in the file ({len(alphabet)}) is odd")
        return "Rotors/" + file_name, alphabet

    def create_rotors(file_name, alphabet, rotors):
        '''creates a rotor config file from variables created in choose_rotors'''
        rotors = int(rotors)
        with open(file_name, "w+") as out_file:
            out_file.write(str(rotors)+" 1\n")
            n = len(alphabet)
            for i in range(rotors):
                out_file.write(' '.join(sample(alphabet, n))+"\n")
            out_file.write(' '.join(alphabet[::-1]))

    def choose_rotors(stdscr):
        '''lets user create or choose variables to create a rotor config file'''
        Initiate.clean_choose(stdscr, "Alphabets", "alphabet", "the alphabet")
        file_name, temp = Initiate.select_name(stdscr, 1, "", "Alphabets/")
        file_name, alphabet = Initiate.create_alphabet(file_name, temp)
        stdscr.addstr(5, 0, " " * (curses.COLS-1))
        stdscr.addstr(0, 0, "Please enter the desired number of rotors to create\n")
        rotors, _ = Initiate.select_name(stdscr, 1, "5", "")
        Initiate.create_rotors(file_name, alphabet, rotors)
        return file_name

    def create_select(select):
        '''creates a select config file from user input'''
        select, plugs = select.split(), []
        while not select[-1].isnumeric():
            plugs.append(select[-1])
            del select[-1]
        rotors = (len(select) - 1) // 2
        with open("Select/temporary.txt", "w+") as out_file:
            for i in range(rotors):
                out_file.write(select[i]+" ")
            out_file.write(select[rotors]+"\n")
            for i in range(rotors):
                out_file.write(select[i+rotors+1]+" ")
            out_file.write("\n")
            for i in range(len(plugs)):
                out_file.write(plugs[i]+" ")
        return "Select/temporary.txt"

    def clean_choose(stdscr, path, info1, info2):
        '''a method cleanly showing all the required information in a "choose" methods to a user'''
        stdscr.clear()
        stdscr.addstr(3, 0, "Press 'Enter' to confirm current typed-in text as a name of the file")
        stdscr.addstr(4, 0, "(leave blank for the default file name and do not forget the extension)")
        if len(info1) > 0:
            stdscr.addstr(5, 0, "you can also create your own "+info1+" from here")
        if len(path) > 0:
            stdscr.addstr(7, 0, f"Avaible {path}: {', '.join(popen(f'ls {path}').read().split())}")
        stdscr.addstr(0, 0, "Please enter the name of a file")
        stdscr.addstr(0, 31, f"{' in ' if len(path) > 0 else ''}{path} containing "+info2+"\n")

    def choose_config(stdscr):
        '''get file_name for Enigma configuration file from user'''
        Initiate.clean_choose(stdscr, "Rotors", "file from chosen alphabet", "rotors and deflectors")
        file_rotors, temp = Initiate.select_name(stdscr, 1, "default.txt", "Rotors/")
        if not temp:
            file_rotors = Initiate.choose_rotors(stdscr)
        Initiate.clean_choose(stdscr, "Select", "select file", "information about the chosen rotors")
        file_select, temp = Initiate.select_name(stdscr, 1, "default.txt", "Select/")
        if not temp:
            file_select = Initiate.create_select(file_select)
        return file_rotors, file_select

    def choose_file(stdscr):
        '''get file_name for Enigma configuration file from user'''
        Initiate.clean_choose(stdscr, "", "", "text to decrypt")
        file_name, _ = Initiate.select_name(stdscr, 1, "standard", "")
        return file_name

    def encrypt_input(stdscr, markM3):
        '''initiates Enigma object from given file_config and runs the simulation'''
        input_key, raw_text, cypher = 'A', '', ''
        stdscr.clear()
        # stdscr.addstr(curses.LINES-1, 0, f"Window size: ({curses.COLS};{curses.LINES})")
        while ord(input_key) != 27:
            stdscr.addstr(0, 0, Enigma.__str__(markM3))
            stdscr.addstr(1, 0, "Press Esc to finish")
            stdscr.addstr(6, 0, "encypted text")
            stdscr.addstr(7, 0, cypher)
            stdscr.addstr(3, 0, "input from keyboard:")
            stdscr.addstr(4, 0, raw_text)
            input_key = stdscr.getkey()
            cypher, unknown, raw_text = Enigma.encrypt_key(markM3, input_key, cypher, raw_text)
            if unknown:
                curses.beep()
                stdscr.addstr(9, 0, "this sign is not included in your selected rotors")
            else:
                stdscr.clear()
        return cypher

    def create_file_info(stdscr, encrypted_text, unknown):
        '''informs about succesful creation of file in create_file'''
        input_key = 'A'
        while ord(input_key) != 27:
            stdscr.clear()
            stdscr.addstr(0, 0, "File containing encrypted text succesfully created")
            stdscr.addstr(1, 0, "Press Esc to exit")
            if unknown:
                stdscr.addstr(3, 0, "Your file contained signs, that were neither on the rotor")
                stdscr.addstr(3, 58, "nor a punctuation and since has been omitted")
            stdscr.addstr(5, 0, "Saved text:\n"+encrypted_text)
            input_key = stdscr.getkey()

    def wrapped_functions(stdscr):
        '''the actual main function of the program - launches all the necessary smaller functions'''
        # initiates Enigma object from given file_names
        markM3 = Enigma(*Create.open_config(*Initiate.choose_config(stdscr)))
        file_name = Initiate.choose_file(stdscr)
        if file_name == "standard":
            encrypted_text, unknown = Initiate.encrypt_input(stdscr, markM3), False
        else:
            raw_text = Enigma.open_file(file_name)
            encrypted_text, unknown = Enigma.encrypt_text(markM3, raw_text)
        Enigma.create_file(encrypted_text)
        Initiate.create_file_info(stdscr, encrypted_text, unknown)


def main():
    '''initiating curses window and all required functions for it'''
    stdscr = curses.initscr()   # initiate screen
    curses.noecho()   # display keys only when needed
    curses.cbreak()   # keys react without needing Enter
    stdscr.keypad(True)   # direction keys work as they should

    curses.wrapper(Initiate.wrapped_functions)

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    main()
