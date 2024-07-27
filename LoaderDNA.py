# ***************************************************************
# File: LoaderDNA.py
# Authors: Krystian Czechowicz, Bartosz Niemiec
# Description: Class to load DNA's and class value from the file 
# ***************************************************************

from DNA import DNA

class LoaderDNA:
    def __init__(self, filename : str) -> None:
        self.__file = filename
        self.__dna_list = []

    def load_DNA(self):
        self.__dna_list = []
        with open(self.__file, "r") as f:
            lines = f.readlines()
            for i in range(int((len(lines))/2)):
                self.__dna_list.append(DNA(lines[2*i+1][:-1], bool(int(lines[2*i][:-1]))))

    def get_DNA_list(self):
        return self.__dna_list

