# *********************************************************************
# File: Node.py
# Authors: Krystian Czechowicz, Bartosz Czechowicz
# Description: Class Node represent either leaf or test node in decision
#              tree. It can be set as root node. It can has children only
#              if node is not leaf. Additional enum class represents
#              dividing option (condition) in given node 
# *********************************************************************

from enum import Enum

class Divide(Enum):
    NULL = 0
    C_G_A_T = 1
    CG_A_T = 2
    CA_G_T = 3
    CT_G_A = 4
    GA_C_T = 5
    GT_C_A = 6
    AT_C_G = 7
    CG_AT = 8
    CA_GT = 9
    CT_GA = 10
    CGA_T = 11
    CGT_A = 12
    CAT_G = 13
    ATG_C = 14
    


class Node:

    def __init__(self, parentNode = None, childNodes = None, leafValue = None) -> None:
        if parentNode is None:
            self.__isRoot = True
        else:
            self.__parentNode = parentNode
        
        if childNodes is None and leafValue is not None:
            self.__isLeaf = True
            self.__leafValue = leafValue
        elif childNodes is not None and leafValue is None:
            self.__isLeaf = False
            self.__childNodes = childNodes
        elif childNodes is None and leafValue is None:
            self.__isLeaf = False
            self.__childNodes = None
        else:
            raise "Node cannot have both children and be leaf"
        
        self.splitOption = Divide.NULL
        self.atributeIndex = None

    def setCondition(self, atributeIndex : int, wayToDivide : Divide):
        self.splitOption = wayToDivide
        self.atributeIndex = atributeIndex

    def getCondition(self):
        return (self.splitOption, self.atributeIndex)

        
    def setLeafValue(self, value):
        if self.__childNodes is not None:
            raise "Leaf cannot have children"
        self.__leafValue = value
        self.__isLeaf = True

    def setChildren(self, childrenList : list):
        self.__childNodes = childrenList
        self.__isLeaf = False
        self.__leafValue = None

    def getParent(self):
        if self.__parentNode is None:
            raise "Root does not have parent"
        return self.__parentNode

    def getChildren(self):
        if self.__isLeaf:
            raise "Leaf do not has children"
        return self.__childNodes

    def getLeafValue(self):
        if not self.__isLeaf:
            raise "Node is not a leaf"
        return self.__leafValue

    def isLeaf(self) -> bool:
        return self.__isLeaf

    def isRoot(self) -> bool:
        return self.__isRoot
