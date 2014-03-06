#! /usr/bin/env python

import sys

# class to store information used in the model
class POSClassification:
    def __init__(self, name):
        self.name = name
        self.words = dict()
        self.suffixes = dict()
        self.pre_pre_tags = dict()
        self.pre_tags = dict()

# class to store data while classifying
class Features:
    def __init__(self, tag, word):
        self.tag = tag
        self.word = word
        self.suffix = word[-2:]

    def setTags(self, pre_tag, pre_pre_tag):
        self.pre_tag = pre_tag
        self.pre_pre_tag = pre_pre_tag


def checkString(word):
    word = word.rstrip('\n') # strip out newlines, which aren't handled well by the model
    if (word == "") or (word == " "):
        return True
    else:
        return False


def locateIndex(tag, pos_list):
    pos_index = -1
    for index,pos in enumerate(pos_list):
        if  tag == pos.name:
            pos_index = index

    # pos tag class doesn't exist yet and we should add a new one
    if pos_index == -1:
        new_class = POSClassification(tag)
        pos_list.append(new_class)
        pos_index = pos_list.index(new_class) # get the index of the class so we add the features to the correct index

    return pos_index


def train():
    
    if len(sys.argv) > 2:
        training_filename = sys.argv[1]
        model_filename = sys.argv[2]
    else:
        print "Not enough arguments: need a training filename and a model filename. Quitting..."
        sys.exit(0)

    pos_list = [] # list of possible part of speech tags
    correct = 0
    print "Beginning training..."
    with open(training_filename) as f:
        for line in f:
            features_list = [] # list of preceding word/tag pairs
            words_and_tags = line.split(' ') # split the line into word and tag pairs
            
            # iterate through the word and tag pairs
            for feature_index,pair in enumerate(words_and_tags):
                #print feature_index, " ", pair
                pair_arr = pair.split('/')
                if checkString(pair_arr[0]) or checkString(pair_arr[1]):
                    continue
                
                features = Features(pair_arr[1], pair_arr[0])
                # initialize features
                if feature_index > 1:
                    features.setTags(features_list[feature_index - 1].tag, features_list[feature_index - 2].tag)
                elif feature_index > 0:
                    features.setTags(features_list[feature_index - 1].tag, "no_tag_present")
                else:
                    features.setTags("no_tag_present", "no_tag_present")

                features_list.append(features)

                # search for the pos tag in the list of possible tags
                pos_index = locateIndex(features.tag, pos_list)

                # classify
                score_by_class = []
                for index,pos in enumerate(pos_list):
                    score = 0    
                    score += pos.words.get(features.word, 0)
                    score += pos.pre_tags.get(features.pre_tag, 0)
                    score += pos.pre_pre_tags.get(features.pre_pre_tag, 0)
                    score += pos.suffixes.get(features.suffix, 0)

                    score_by_class.append(score)
                    #print "score for ", pos.name, " is ", score

                classified = max(score_by_class)
                classified_index = score_by_class.index(classified)
                #print "Classified as ", pos_list[classified_index].name
               
                correct += 1
                # check and update
                if pos_list[classified_index].name != features.tag:
                    #print "Incorrectly classified as ", pos_list[classified_index].name
                    correct -= 1
                    print correct

                    for pos in pos_list:
                        # score using word
                        if features.word in pos.words:
                            if pos.name == features.tag:
                                pos.words[features.word] += 1 
                            else:
                                pos.words[features.word] -= 1 
                                    
                        # add new word to weight vector
                        else:
                            if pos.name == features.tag:
                                pos.words[features.word] = 1 
                            else:
                                pos.words[features.word] = -1
                                
                        # score using pre_tag
                        if features.pre_tag in pos.pre_tags: 
                            if pos.name == features.tag:
                                pos.pre_tags[features.pre_tag] += 1 
                            else:
                                pos.pre_tags[features.pre_tag] -= 1 
                                    
                        # add new pre_tag to weight vector
                        else:
                            if pos.name == features.tag:
                                pos.pre_tags[features.pre_tag] = 1 
                            else:
                                pos.pre_tags[features.pre_tag] = -1
                        
                        # score using pre_pre_tag
                        if features.pre_pre_tag in pos.pre_pre_tags:
                            if pos.name == features.tag:
                                pos.pre_pre_tags[features.pre_pre_tag] += 1 
                            else:
                                pos.pre_pre_tags[features.pre_pre_tag] -= 1 
                                    
                        # add new pre_pre_tag to weight vector
                        else:
                            if pos.name == features.tag:
                                pos.pre_pre_tags[features.pre_pre_tag] = 1 
                            else:
                                pos.pre_pre_tags[features.pre_pre_tag] = -1

                        # score using suffix
                        if features.suffix in pos.suffixes:
                            if pos.name == features.tag:
                                pos.suffixes[features.suffix] += 1 
                            else:
                                pos.suffixes[features.suffix] -= 1 
                                    
                        # add new suffix to weight vector
                        else:
                            if pos.name == features.tag:
                                pos.suffixes[features.suffix] = 1 
                            else:
                                pos.suffixes[features.suffix] = -1


    # Generate the classification model
    model_file = open(model_filename, 'w')
    model_file.write("{0} number_of_classes\n".format(len(pos_list)))

    for pos in pos_list:
        model_file.write("{0} {1} {2} {3}\n".format(pos.name, len(pos.words), len(pos.pre_tags), len(pos.pre_pre_tags)))
    
    for pos in pos_list:

        for word in pos.words:
            model_file.write("{0} {1}\n".format(word, pos.words[word]))
       
        for pre_tag in pos.pre_tags:
            model_file.write("{0} {1}\n".format(pre_tag, pos.pre_tags[pre_tag]))
        
        for pre_pre_tag in pos.pre_pre_tags:
            model_file.write("{0} {1}\n".format(pre_pre_tag, pos.pre_pre_tags[pre_pre_tag]))
        for suffix in pos.suffixes:
            model_file.write("{0} {1}\n".format(suffix, pos.suffixes[suffix]))


train()
