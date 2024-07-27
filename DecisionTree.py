# *********************************************************************
# File: DecisionTree.py
# Authors: Krystian Czechowicz, Bartosz Czechowicz
# Description: Class DecisionTree contains methods to build tree and
#              predict value of class for given DNA seqence.
#              Enum class are used to choose algorythm configuration
# *********************************************************************

from enum import Enum
from Node import Node, Divide
import math

class SplitCriteria(Enum):
    GINI = 0
    ENTROPY = 1

class StopCriteria(Enum):
    BASIC_STOP = 0
    LOOSE_STOP = 1
    BASIC_DEPTH_STOP = 2
    LOOSE_DEPTH_STOP = 3

class Alternative(Enum):
    EXCLUDE = 0
    INCLUDE = 1

class DecisionTree:


    def __init__(self,  trainData : list,
                 split_criteria : SplitCriteria = SplitCriteria.ENTROPY,
                 stop_criteria : StopCriteria = StopCriteria.BASIC_STOP,
                 alternative : Alternative = Alternative.EXCLUDE ,
                 depth = None, domination_percent = 1.0, excamples_percent_to_stop = 0.0) -> None:
        self.__split_criteria = split_criteria
        self.__stop_criteria = stop_criteria
        self.__alternative = alternative
        self.__trainData = trainData
        self.__maxDepth = depth
        self.__rootNode = Node()
        
        self.__DOMINATION_PERCENT = domination_percent
        self.__EXAMPLES_PERCENT_TO_STOP = excamples_percent_to_stop

    # used to start building decision tree
    def build_tree(self):
        self.__build_tree(self.__rootNode, self.__trainData)
    
    # used to predict class for given DNA sequence
    def predict(self, seq : list):
         bbb = self.__predict(seq, self.__rootNode)
         return bbb
    
    # private method to check appropriate stop criteria
    def __check_for_stop(self, currentNode : Node,
                       currentData : list,
                       parentData : list,
                       currentDepth : int) -> bool:
        if self.__stop_criteria == StopCriteria.BASIC_STOP.value:
            return self.__basic_stop(currentNode, currentData, parentData, currentDepth, False)
        elif self.__stop_criteria == StopCriteria.BASIC_DEPTH_STOP.value:
            return self.__basic_stop(currentNode, currentData, parentData, currentDepth, True)
        elif self.__stop_criteria == StopCriteria.LOOSE_STOP.value:
            return self.__loose_stop(currentNode, currentData, parentData, currentDepth, False)
        elif self.__stop_criteria == StopCriteria.LOOSE_DEPTH_STOP.value:
            return self.__loose_stop(currentNode, currentData, parentData, currentDepth, True)
        else:
            raise "Wrong stop criteria chosen"
        
    # private method to get entropy on given data
    def __get_entropy(self, data):
        if len(data) != 0:
            sum = 0
            for d in data:
                if d.isCut == 1:
                    sum +=1
            
            fraction = sum/len(data)
            if(fraction == 0 or fraction == 1):
                return 0
            return (-1)*(fraction*math.log2(fraction) + (1 - fraction)*math.log2(1 - fraction))
        else:
            return 0     

    # private method to get gini index on given data
    def __get_gini_index(self, data):
        if len(data) != 0:
            fraction = sum(data)/len(data)
            return (1- (fraction**2 + (1-fraction)**2))
        else:
            return 0

    # private method to split sets using best entrophy/gini index
    def __get_split(self, currentTrainData, split_criteria, alternative):
        best_entropy = 2
        best_gini = 2
        best_split_option = None
        best_atr_idx = None
        num_of_children = None
        for atr_idx in range(len(currentTrainData[0])):
            if alternative == Alternative.INCLUDE.value:
                for split in list(Divide)[8:]:
                    entropy = 0
                    gini = 0
                    num_of_children_local = 0
                    if split == Divide.C_G_A_T:
                        for i in range(4):
                            modified_data = self.__modify_train_data(split, atr_idx, i, currentTrainData)
                            if split_criteria == SplitCriteria.GINI.value:
                                gini += (len(modified_data)/len(currentTrainData))*self.__get_gini_index(modified_data)
                            else:
                                entropy += (len(modified_data)/len(currentTrainData))*self.__get_entropy(modified_data)
                        num_of_children_local = 4
                    elif (split == Divide.CG_A_T or split == Divide.CA_G_T or 
                        split == Divide.CT_G_A or split == Divide.GA_C_T or 
                        split == Divide.GT_C_A or split == Divide.AT_C_G):
                        for i in range(3):
                            modified_data = self.__modify_train_data(split, atr_idx, i, currentTrainData)
                            if split_criteria == SplitCriteria.GINI.value:
                                gini += (len(modified_data)/len(currentTrainData))*self.__get_gini_index(modified_data)
                            else:
                                entropy += (len(modified_data)/len(currentTrainData))*self.__get_entropy(modified_data)
                        num_of_children_local = 3
                    elif (split == Divide.CG_AT or Divide.CA_GT or 
                        Divide.CT_GA):
                        for i in range(2):
                            modified_data = self.__modify_train_data(split, atr_idx, i, currentTrainData)
                            if split_criteria == SplitCriteria.GINI.value:
                                gini += (len(modified_data)/len(currentTrainData))*self.__get_gini_index(modified_data)
                            else:
                                entropy += (len(modified_data)/len(currentTrainData))*self.__get_entropy(modified_data)
                        num_of_children_local = 2
                    else:
                        for i in range(2):
                            modified_data = self.__modify_train_data(split, atr_idx, i, currentTrainData)
                            if split_criteria == SplitCriteria.GINI.value:
                                gini += (len(modified_data)/len(currentTrainData))*self.__get_gini_index(modified_data)
                            else:
                                entropy += (len(modified_data)/len(currentTrainData))*self.__get_entropy(modified_data)
                        num_of_children_local = 2
                    if split_criteria == SplitCriteria.GINI.value:
                        if gini < best_gini:
                            best_gini = gini
                            best_split_option = split
                            best_atr_idx = atr_idx
                            num_of_children = num_of_children_local
                    else:
                        if entropy < best_entropy:
                            best_entropy = entropy
                            best_split_option = split
                            best_atr_idx = atr_idx
                            num_of_children = num_of_children_local
            else:
                entropy = 0
                gini = 0
                num_of_children_local = 0
                split = Divide.C_G_A_T
                for i in range(4):
                    modified_data = self.__modify_train_data(split, atr_idx, i, currentTrainData)
                    if split_criteria == SplitCriteria.GINI.value:
                        gini += (len(modified_data)/len(currentTrainData))*self.__get_gini_index(modified_data)
                    else:
                        entropy += (len(modified_data)/len(currentTrainData))*self.__get_entropy(modified_data)
                num_of_children_local = 4
                if split_criteria == SplitCriteria.GINI.value:
                    if gini < best_gini:
                            best_gini = gini
                            best_split_option = split
                            best_atr_idx = atr_idx
                            num_of_children = num_of_children_local
                else:
                    if entropy < best_entropy:
                            best_entropy = entropy
                            best_split_option = split
                            best_atr_idx = atr_idx
                            num_of_children = num_of_children_local

        return best_split_option, best_atr_idx, num_of_children


    

    # private method to generate modified data that met given condition
    def __modify_train_data(self,
                        splitOption : Divide,
                        atrIndex : int,
                        index : int,
                        trainData : list) -> list:
        
        modifiedData = []

        if splitOption == Divide.C_G_A_T:
            if index == 0:
                modifiedData = self.__split_data(['C'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['G'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['A'], atrIndex, trainData)
            else:
                modifiedData = self.__split_data(['T'], atrIndex, trainData)
        
        elif splitOption == Divide.CG_A_T:
            if index == 0:
                modifiedData = self.__split_data(['C', 'G'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['A'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['T'], atrIndex, trainData)

        elif splitOption == Divide.CA_G_T:
            if index == 0:
                modifiedData = self.__split_data(['C', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['G'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['T'], atrIndex, trainData)

        elif splitOption == Divide.CT_G_A:
            if index == 0:
                modifiedData = self.__split_data(['C', 'T'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['G'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['A'], atrIndex, trainData)

        elif splitOption == Divide.GA_C_T:
            if index == 0:
                modifiedData = self.__split_data(['G', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['C'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['T'], atrIndex, trainData)
        
        elif splitOption == Divide.GT_C_A:
            if index == 0:
                modifiedData = self.__split_data(['G', 'T'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['C'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['A'], atrIndex, trainData)

        elif splitOption == Divide.AT_C_G:
            if index == 0:
                modifiedData = self.__split_data(['A', 'T'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['C'], atrIndex, trainData)
            elif index == 2:
                modifiedData = self.__split_data(['G'], atrIndex, trainData)

        elif splitOption == Divide.CG_AT:
            if index == 0:
                modifiedData = self.__split_data(['C', 'G'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['A', 'T'], atrIndex, trainData)
            
        elif splitOption == Divide.CA_GT:
            if index == 0:
                modifiedData = self.__split_data(['C', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['G', 'T'], atrIndex, trainData)

        elif splitOption == Divide.CT_GA: 
            if index == 0:
                modifiedData = self.__split_data(['C', 'T'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['A', 'G'], atrIndex, trainData)

        elif splitOption == Divide.CGA_T: 
            if index == 0:
                modifiedData = self.__split_data(['C', 'G', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['T'], atrIndex, trainData)

        elif splitOption == Divide.CGT_A: 
            if index == 0:
                modifiedData = self.__split_data(['C', 'G', 'T'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['A'], atrIndex, trainData)

        elif splitOption == Divide.CAT_G: 
            if index == 0:
                modifiedData = self.__split_data(['C', 'T', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['G'], atrIndex, trainData)

        elif splitOption == Divide.ATG_C: 
            if index == 0:
                modifiedData = self.__split_data(['G', 'T', 'A'], atrIndex, trainData)
            elif index == 1:
                modifiedData = self.__split_data(['C'], atrIndex, trainData)

        
        return modifiedData
    
    # private method to update nodes (condition to set, child list)
    def __update_node_params(self, currentNode, best_split, best_atr_idx, num_of_children):
        currentNode.setCondition(best_atr_idx, best_split)
        children_list = []
        for i in range(num_of_children):
            children_list.append(Node(currentNode))
        currentNode.setChildren(children_list)



    # private method to build tree (recurency)
    def __build_tree(self, currentNode : Node,
                     currentTrainData : list,
                     parentTrainData : list = None,
                     currentDepth : int = 0):
        
        if self.__check_for_stop(currentNode, currentTrainData, parentTrainData, currentDepth):
            return 0
        best_split, best_atr_idx, num_of_children = self.__get_split(currentTrainData, self.__split_criteria, self.__alternative)
        self.__update_node_params(currentNode, best_split, best_atr_idx, num_of_children)
        for split_num, node in enumerate(currentNode.getChildren()):
            childTrainData = self.__modify_train_data(currentNode.splitOption, currentNode.atributeIndex
                                                    , split_num, currentTrainData)

            for dna in childTrainData:
                dna.sequence.pop(currentNode.atributeIndex)
            self.__build_tree(node, childTrainData, currentTrainData, currentDepth+1)
                

    # check basic stop criteria with possibility to include depth
    def __basic_stop(self, currentNode : Node,
                     trainingData : list,
                     parentData : list,
                     currentDepth : int,
                     additional : bool = False) -> bool:
        
        # check if subset is empty
        if len(trainingData) == 0:
            if sum(parentData) >= len(parentData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True
        
       # check if there are atribute
        if len(trainingData[0].sequence) == 0:
            if sum(parentData) >= len(parentData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True 
        
        # check if all data has same class
        if sum(trainingData)==len(trainingData) or sum(trainingData) == 0: 
            currentNode.setLeafValue(trainingData[0].isCut)
            return True
        
        # check if there are exist possible division
        dna_to_check = trainingData[0]
        all_the_same = True
        for dna in trainingData[8:]:
            for index, nucleodite in enumerate(dna_to_check.sequence):
                if nucleodite != dna[index]:
                    all_the_same = False
                
        if all_the_same:
            if sum(trainingData) >= len(trainingData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True
        


        # check depth is additional is required
        if additional:
            if currentDepth >= self.__maxDepth:
                if sum(trainingData) >= len(trainingData) / 2:
                    currentNode.setLeafValue(True)
                else:
                    currentNode.setLeafValue(False)
                return True
            
        return False


    # check loose stop criteria with possibility to include depth
    def __loose_stop(self, currentNode : Node,
                     trainingData : list,
                     parentData : list,
                     currentDepth : int,
                     additional : bool = False) -> bool:
        
        # to few examples
        if len(trainingData) <= self.__EXAMPLES_PERCENT_TO_STOP*len(self.__trainData):
            if sum(parentData) >= len(parentData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True 
        
        # check if there are atribute
        if len(trainingData[0].sequence) == 0:
            if sum(parentData) >= len(parentData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True 

        # check domination of one class
        if sum(trainingData) <= (1-self.__DOMINATION_PERCENT)*len(trainingData):
            currentNode.setLeafValue(False)
            return True
        elif sum(trainingData) >= self.__DOMINATION_PERCENT*len(trainingData):
            currentNode.setLeafValue(True)
            return True
        
        # check if there are exist possible division
        dna_to_check = trainingData[0]
        all_the_same = True
        for dna in trainingData[1:]:
            for index, nucleodite in enumerate(dna_to_check.sequence):
                if nucleodite != dna[index]:
                    all_the_same = False
                
        if all_the_same:
            if sum(trainingData) >= len(trainingData) / 2:
                currentNode.setLeafValue(True)
            else:
                currentNode.setLeafValue(False)
            return True
        
        # check depth is additional is required
        if additional:
            if currentDepth >= self.__maxDepth:
                if sum(trainingData) >= len(trainingData) / 2:
                    currentNode.setLeafValue(True)
                else:
                    currentNode.setLeafValue(False)
                return True

        return False
    

    # used in modifying set to return subset that meet given condition
    def __split_data(self, conditionSet : list,
                  index : int,
                  data : list) -> list:
        
        data_to_ret = []
        for dna in data:
            if(dna[index] in conditionSet):
                data_to_ret.append(dna.copy())

        return data_to_ret
    

    # private method used in prediction (recurency)
    def __predict(self, seq : list, node : Node):
        if node.isLeaf():
            bbb = node.getLeafValue()
            return bbb
        nucleotide = seq[node.atributeIndex]
        if node.splitOption == Divide.C_G_A_T:
            if nucleotide == 'C':
                child = node.getChildren()[0]
            elif nucleotide == 'G':
                child = node.getChildren()[1]
            elif nucleotide == 'A':
                child = node.getChildren()[2]
            else:
                child = node.getChildren()[3]
        
        elif node.splitOption == Divide.CG_A_T:
            if nucleotide == 'C' or nucleotide == 'G':
                child = node.getChildren()[0]
            elif nucleotide == 'A':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]

        elif node.splitOption == Divide.CA_G_T:
            if nucleotide == 'C' or nucleotide == 'A':
                child = node.getChildren()[0]
            elif nucleotide == 'G':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]

        elif node.splitOption == Divide.CT_G_A:
            if nucleotide == 'C' or nucleotide == 'T':
                child = node.getChildren()[0]
            elif nucleotide == 'G':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]

        elif node.splitOption == Divide.GA_C_T:
            if nucleotide == 'G' or nucleotide == 'A':
                child = node.getChildren()[0]
            elif nucleotide == 'G':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]
        
        elif node.splitOption == Divide.GT_C_A:
            if nucleotide == 'G' or nucleotide == 'T':
                child = node.getChildren()[0]
            elif nucleotide == 'C':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]

        elif node.splitOption == Divide.AT_C_G:
            if nucleotide == 'A' or nucleotide == 'T':
                child = node.getChildren()[0]
            elif nucleotide == 'C':
                child = node.getChildren()[1]
            else:
                child = node.getChildren()[2]

        elif node.splitOption == Divide.CG_AT:
            if nucleotide == 'C' or nucleotide == 'G':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]
            
        elif node.splitOption == Divide.CA_GT:
            if nucleotide == 'C' or nucleotide == 'A':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        elif node.splitOption == Divide.CT_GA: 
            if nucleotide == 'C' or nucleotide == 'T':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        elif node.splitOption == Divide.CGA_T: 
            if nucleotide == 'C' or nucleotide == 'G' or nucleotide == 'A':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        elif node.splitOption == Divide.CGT_A: 
            if nucleotide == 'C' or nucleotide == 'G' or nucleotide == 'T':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        elif node.splitOption == Divide.CAT_G: 
            if nucleotide == 'C' or nucleotide == 'T' or nucleotide == 'A':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        elif node.splitOption == Divide.ATG_C: 
            if nucleotide == 'T' or nucleotide == 'G' or nucleotide == 'A':
                child = node.getChildren()[0]
            else:
                child = node.getChildren()[1]

        return self.__predict(seq, child)



