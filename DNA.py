# *****************************************************************
# File: DNA.py
# Authors: Krystian Czechowicz, Bartosz Niemiec
# Description: DNA class contains methods, that allows to operate
#              on it as on list, but also contains additional
#              attrubute (class value of example - isCut)
# *****************************************************************


class DNA:
    def __init__(self, sequence : str, isCut : bool) -> None:
        self.isCut = isCut
        self.sequence=[i for a,i in enumerate(sequence) ] 
        self.__index=0
    
    def __getitem__(self, index : int) -> str:
        if(index>=len(self.sequence)):
            raise Exception
        else:
            return self.sequence[index]
        
    def __setitem__(self, index: int, nucletide : str) -> None:
        if(index < len(self.sequence)):
            self.sequence[index] = nucletide
        elif(index == len(self.sequence)):
            self.sequence.append(nucletide)
        else:
            raise "Index is out of range" 
    
    def __len__(self):
        return len(self.sequence)
    
    def append(self, nucletide : str) -> None:
        self.sequence.append(nucletide)

    def pop(self) -> None:
        self.sequence.pop()
    
    def __eq__(self, other) -> bool:
        return self.sequence == other.sequence
    
    def __str__(self) -> str:
        return str(self.sequence)
    
    def __add__(self, other):
        return int(self) + int(other)
    
    def __int__(self):
        return int(self.isCut)
    
    def __radd__(self, other):
        return int(self) + int(other)

    def __iter__(self):
        self.__index = 0

    def __next__(self):
        if self.__index < len(self.sequence):
            result = self.sequence[self.__index]
            self.__index += 1
            return result
        else:
            raise StopIteration

    def copy(self):
        d = DNA(self.sequence, self.isCut)
        return d