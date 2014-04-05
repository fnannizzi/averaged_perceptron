#! /usr/bin/env python

import sys

# class to store weight vectors for each iteration
class Iteration:
    def __init__(self, index):
        self.index = index
        self.classes = []

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.weights = dict()

def train():
    
    if len(sys.argv) > 3:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
        num_iterations = int(sys.argv[3])
    else:
        print "Not enough arguments: need a training filename, a model filename, and a number of iterations. Quitting..."
        sys.exit(0)


    iterations = [] # list of weight vectors calculated in each iteration

    print "Beginning training..."
    for iteration in range(0,num_iterations):
        this_iteration = Iteration(iteration)
        print iteration
        if iteration > 0:
            this_iteration.classes = iterations[iteration - 1].classes
        
        with open(training_filename) as f:
            for line in f:
                class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
                classname = class_and_text[0]
                text = class_and_text[1]

                # search for the class in the list of possible classes
                class_index = -1
                for c in this_iteration.classes:
                    if classname == c.name:
                        class_index = this_iteration.classes.index(c)

                # class doesn't exist yet and we should add a new one
                if class_index == -1:
                    new_class = Classification(classname)
                    this_iteration.classes.append(new_class)
                    class_index = this_iteration.classes.index(new_class) # get the index of the class so we add the features to the correct index

                # classify 
                score_by_class = []
                for class_index,class_type in enumerate(this_iteration.classes):
                    score = 0
                    for word in text.split(' '):
                        word = word.rstrip('\n') # strip out newlines, which aren't handled well by the model
                        if (word == "") or (word == " "):
                            continue

                        if word in class_type.weights:
                            score += class_type.weights[word]

                    score_by_class.append(score)

                classified = max(score_by_class)
                classified_index = score_by_class.index(classified)
                    
                # check and update
                if this_iteration.classes[classified_index].name != classname:
                    #print "Incorrectly classified as ", this_iteration.classes[classified_index].name
                    for class_index, class_type in enumerate(this_iteration.classes):
                        for word in text.split(' '):
                            word = word.rstrip('\n') # strip out newlines, which aren't handled well by the model
                            if (word == "") or (word == " "):
                                continue
                            
                            if word in this_iteration.classes[class_index].weights:
                                if class_type.name == classname:
                                    this_iteration.classes[class_index].weights[word] += 1
                                else:
                                    this_iteration.classes[class_index].weights[word] -= 1
                                        
                            # add new word to weight vector
                            else:
                                if class_type.name == classname:
                                    this_iteration.classes[class_index].weights[word] = 1
                                else:
                                    this_iteration.classes[class_index].weights[word] = -1
 
 
        iterations.append(this_iteration)


    # Average the weights
    averaged_weights = iterations[0]
    for index in range(1, num_iterations):
        for class_type in iterations[index].classes:
            class_index = iterations[index].classes.index(class_type)
            for word in class_type.weights:
                print class_type.weights[word]
                averaged_weights.classes[class_index].weights[word] += class_type.weights[word]

    for class_type in averaged_weights.classes:
        for word in class_type.weights:
            class_type.weights[word] = (class_type.weights[word]/num_iterations)


    # Generate the classification model
    model_file = open(model_filename, 'w')
    model_file.write("{0} number_of_classes\n".format(len(averaged_weights.classes)))

    for class_type in averaged_weights.classes:
        model_file.write("{0} {1}\n".format(class_type.name, len(class_type.weights)))
    
    for class_type in averaged_weights.classes:
        for word in class_type.weights:
            model_file.write("{0} {1}\n".format(word, class_type.weights[word]))




train()
