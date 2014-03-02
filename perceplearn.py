#! /usr/bin/env python

import sys

# class to store information used in the model
class Classification:
    def __init__(self, name):
        self.name = name
        self.weights = dict()

def train():
    
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)


    classes = [] # list of possible classes

    print "Beginning training..."
    with open(training_filename) as f:
        for line in f:
            class_and_text = line.split(' ', 1) # split the first word (the class identifier) from the rest of the text
            classname = class_and_text[0]
            text = class_and_text[1]
            print classname

            # search for the class in the list of possible classes
            class_index = -1
            for c in classes:
                if classname == c.name:
                    class_index = classes.index(c)

            # class doesn't exist yet and we should add a new one
            if class_index == -1:
                new_class = Classification(classname)
                classes.append(new_class)
                class_index = classes.index(new_class) # get the index of the class so we add the features to the correct index

            # classify 
            score_by_class = []
            for class_index,class_type in enumerate(classes):
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
            if classes[classified_index].name != classname:
                print "Incorrectly classified as ", classes[classified_index].name
                for class_index, class_type in enumerate(classes):
                    for word in text.split(' '):
                        word = word.rstrip('\n') # strip out newlines, which aren't handled well by the model
                        if (word == "") or (word == " "):
                            continue
                        
                        if word in classes[class_index].weights:
                            if class_type.name == classname:
                                classes[class_index].weights[word] += 1 
                            else:
                                classes[class_index].weights[word] -= 1
                                    
                        # add new word to weight vector
                        else:
                            if class_type.name == classname:
                                classes[class_index].weights[word] = 1 
                            else:
                                classes[class_index].weights[word] = -1
 


    # Generate the classification model
    model_file = open(model_filename, 'w')
    model_file.write("{0} number_of_classes\n".format(len(classes)))

    for class_type in classes:
        model_file.write("{0} {1}\n".format(class_type.name, len(class_type.weights)))
    
    for class_type in classes:
        for word in class_type.weights:
            model_file.write("{0} {1}\n".format(word, class_type.weights[word]))




train()
