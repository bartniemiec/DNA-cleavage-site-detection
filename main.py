# ************************************************************
# File: main.py
# Authors: Krystian Czechowicz, Bartosz Niemiec
# Description: main file of program to perform data loading,
#              building decision tree using cross validation
#              and calculate performance
# ***********************************************************

import DecisionTree
import LoaderDNA
import argparse

def main(filename, split, stop, alternative, depth, dominationPercent, examplesPercent):

    # Loading data from file
    loader = LoaderDNA.LoaderDNA(filename)
    loader.load_DNA()
    data = loader.get_DNA_list()

    # Split data on equal 5 grups for cross-validation
    true_data = []
    false_data = []
    for dna in data:
        if dna.isCut:
            true_data.append(dna)
        else:
            false_data.append(dna)

    group_1 = true_data[:int(len(true_data)/5)] + false_data[:int(len(false_data)/5)]
    group_2 = true_data[int(len(true_data)/5):int(2*len(true_data)/5)] + false_data[int(len(false_data)/5):int(2*len(false_data)/5)]
    group_3 = true_data[int(2*len(true_data)/5):int(3*len(true_data)/5)] + false_data[int(2*len(false_data)/5):int(3*len(false_data)/5)]
    group_4 = true_data[int(3*len(true_data)/5): int(4*len(true_data)/5)] + false_data[int(3*len(false_data)/5): int(4*len(false_data)/5)]
    group_5 = true_data[int(4*len(true_data)/5): int(len(true_data))] + false_data[int(4*len(false_data)/5): int(len(false_data))]

    groups = [group_1,group_2,group_3,group_4, group_5]

    # build tree 5 times - cross validation
    best_accuracy = 0
    best_tp = 0; best_tn = 0; best_fp = 0; best_fn = 0
    
    for i in range(5):
        validation_set = groups[i%5]       
        training_set = groups[(i+1)%5] + groups[(i+2)%5] + groups[(i+3)%5] + groups[(i+4)%5]        
        dt = DecisionTree.DecisionTree(training_set, split,stop, alternative, depth, dominationPercent, examplesPercent)
        dt.build_tree()
        score = 0
        tp = 0
        tn = 0
        fp = 0
        fn = 0
        for data in validation_set:
            prediction = dt.predict(data.sequence)
            real = data.isCut
            if real == 1 and prediction == 1:
                tp+=1
                score+=1
            elif real == 0 and prediction == 0:
                tn+=1
                score+=1
            elif real == 0 and prediction == 1:
                fp+=1
            elif real == 1 and prediction == 0:
                fn+=1
        accuracy = score/len(validation_set)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_training_set = training_set
            best_tp = tp
            best_tn = tn
            best_fp = fp
            best_fn = fn
            best_dt = dt


    # calculate performance score using best resulted values

    recall = best_tp/(best_tp+best_fn)
    specificity = best_tn/(best_tn+best_fp)
    speciality = best_tp/(best_tp+best_fp)
    f2 = (2*specificity*recall)/(recall+specificity)
    f1 = (2*speciality*recall)/(recall+speciality)

    print("============= VALIDATING DATA ==============")
    print(f'Accuracy: {best_accuracy}')
    print(f'True positive: {best_tp}')
    print(f'True negative: {best_tn}')
    print(f'False positive: {best_fp}')
    print(f'False negative: {best_fn}')
    print(f'Recall: {recall}')
    print(f'Specificity: {specificity}')
    print(f'Speciality: {speciality}')
    print(f'F1 Score: {f1}')

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    score = 0
    for data in best_training_set:
        prediction = best_dt.predict(data.sequence)
        real = data.isCut
        if real == 1 and prediction == 1:
            tp+=1
            score+=1
        elif real == 0 and prediction == 0:
            tn+=1
            score+=1
        elif real == 0 and prediction == 1:
            fp+=1
        elif real == 1 and prediction == 0:
            fn+=1
    accuracy = score/len(best_training_set)

    recall = tp/(tp+fn)
    specificity = tn/(tn+fp)
    speciality = tp/(tp+fp)
    f1 = (2*speciality*recall)/(recall+speciality)
    f2 = (2*specificity*recall)/(recall+specificity)

    print("============= TRAINING DATA ==============")
    print(f'Accuracy: {accuracy}')
    print(f'True positive: {tp}')
    print(f'True negative: {tn}')
    print(f'False positive: {fp}')
    print(f'False negative: {fn}')
    print(f'Recall: {recall}')
    print(f'Specificity: {specificity}')
    print(f'Speciality: {speciality}')
    print(f'F1 Score: {f1}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset")
    parser.add_argument("split")
    parser.add_argument("stop")
    parser.add_argument("alternative")
    parser.add_argument("depth", nargs="?", const = 0, type=int)
    parser.add_argument("dominationPercent", nargs="?", const = 1.0, type=float)
    parser.add_argument("examplesPercent", nargs="?", const = 0.0, type=float)
    args = parser.parse_args()

    dataset = args.dataset

    split = int(args.split)
    print("Chosen split criteria: " + str(DecisionTree.SplitCriteria(split).name))

    stop = int(args.stop)
    print("Chosen stop criteria: " + str(DecisionTree.StopCriteria(stop).name))
    
    alternative = int(args.alternative)
    print("Alternative option: " + str(DecisionTree.Alternative(alternative).name))

    depth = args.depth
    if depth != None and (stop == 2 or stop == 3):
        print("Depth: " + str(depth))

    dominationPercent = args.dominationPercent
    if dominationPercent != None and (stop == 1 or stop == 3):
        print("Domination percent to stop: " + str(dominationPercent))

    examplesPercent = args.examplesPercent
    if examplesPercent != None and (stop == 1 or stop == 3):
        print("Examples percent to stop: " + str(examplesPercent))

    main(dataset, split, stop, alternative, depth, dominationPercent, examplesPercent)