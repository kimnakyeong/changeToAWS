import re
import nltk
from nltk.corpus import names
import random
import pickle

def gender_features(word):
    return {'last_letter': re.sub('[0-9]', '', word)[-1].lower()}
    
print(gender_features('Shrek'))

labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
random.shuffle(labeled_names)

featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
train_set, test_set = featuresets[500:], featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)

with open('data.pickle', 'wb') as f:
    pickle.dump(classifier, f, pickle.HIGHEST_PROTOCOL)

nltk.classify.accuracy(classifier, test_set)

classifier.show_most_informative_features()

pickle.dumps(classifier)

def predict(usernames):
    return [{u: classifier.classify(gender_features(u))} for u in usernames]

input_data = [
    'ned', 
    'etainclub',
    'codingart',
    'codingman',
    'ksc',
    'imrahelk', 
    'newbijohn', 
    'coinfarmer165', 
    'ponzipanda',
    'blockchainstudio',
    'jisoooh0202',
    'jamieinthedark',
    'xinnong',
    'bbooaae',
    'onehand',            
    'osyvv',
    'bluengel',
    'jungjunghoon',
    'duplicate',
    'lucky2',       
]

print(predict(input_data))