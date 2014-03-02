#! /usr/bin/env python

import sys

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.weights = dict()
        self.size_weight_vector = 0
    
def classify():
    
    if len(sys.argv) > 1:
        model_filename = sys.argv[1]

    else:
        print "Not enough arguments: need a model filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes

    # loading model
    with open(model_filename) as f:        
        # read the number of classes
        line = f.readline()
        tokens = line.split(' ')
        num_classes = int(tokens[0])
                
        for x in range(0, num_classes):
            # read the class names and store the class info
            line = f.readline()
            tokens = line.split(' ')
            new_class = Classification(tokens[0])
            new_class.size_weight_vector = int(tokens[1])
            classes.append(new_class)
        
        for class_type in classes:
            for word_in_model in range(0, class_type.size_weight_vector):
                line = f.readline()
                tokens = line.split(' ')
                class_type.weights[tokens[0]] = int(tokens[1])

    # begin classification
    print "Model file loaded. Classification beginning. Enter 'quit' to exit."
    
    while(True):
        input = raw_input("Please enter some text: ")
        if input.lower() == "quit":
            print "Quitting..."
            break

        else:
            score_by_class = []
            for class_index,class_type in enumerate(classes):
                score = 0
                for word in input.split(' '):
                    word = word.rstrip('\n') # strip out newlines, which aren't handled well by the model
                    if (word == "") or (word == " "):
                        continue
                    
                    if word in class_type.weights:
                        score += class_type.weights[word]
                    else:
                        class_type.weights[word] = 0
                    
                        for index,c in enumerate(classes):
                            if index == class_index:
                                continue
                            c.weights[word] = 0

                score_by_class.append(score)

            classified = max(score_by_class)
            classified_index = score_by_class.index(classified)
            print "Classified as ", classes[classified_index].name


classify()