import nltk
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords
from nltk.util import everygrams
import treetaggerwrapper
from collections import Counter

#entfernt Satzzeichen
#auch Punkte z.B. nach Zahlen
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

#Bildet N-gramme
#input ist eine Liste aus Sätzen
#min_len ist die minimale Länge der N-gramme
#max_len ist die maximale Länge der N-gramme
def create_ngrams(input, min_len, max_len):
    result = []
    for sent in input:
      sent_split = sent.split()
      result.append(list(everygrams(sent_split, min_len=min_len, max_len=max_len)))
    return result

def remove_stopwords(text, stopwords):
    for sent in text:
        for w in sent:
            if w in stopwords:
                sent.remove(w)

def prepare_description(text):
    #Aufteilung in Sätze
    sentences = nltk.sent_tokenize(text, language='german')

    #Satzzeichen löschen
    for i in range(len(sentences)):
     sentences[i] = strip_punctuation(sentences[i])

    #Tokenization
    tokenized_text = [nltk.word_tokenize(sent, language='german') for sent in sentences]

    #N-gramme bilden
    ngrams = create_ngrams(sentences, 2, 3)

    #Stopwörter löschen
    stop_words = set(stopwords.words('german'))
    remove_stopwords(tokenized_text, stop_words)
    return zip(tokenized_text, ngrams)

def filter_nouns(text, local_counter):
    #Treetagger
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
    tags = []
    for sent in text:
        tags += tagger.tag_text(sent, tagonly=True)
    tags = treetaggerwrapper.make_tags(tags)

    #Nomen filtern
    nouns = set()
    for array in tags:
      if(array[1] == "NNP" or array[1] == "NN" or
           array[1] == "NNPS" or array[1] == "NNS"):
        nouns.add(array[0])
    return nouns

#die einzelnen str elemente aus den tupeln extrahieren (für jeden Satz)
#dann daraus ein set erstellen
def ngrams_to_set(ngrams):
    result = set()
    for sentence in ngrams:
        for tuple in sentence:
            s = ""
            for i in range(len(tuple)):
                if(i == len(tuple)-1):
                    s += tuple[i]
                else:
                    s += tuple[i] + " "
            result.add(s)
    return result

######### main script #############
print("Text Mining gestartet")
counter = Counter()

#import csv
data = pd.read_csv("2019-04-09_123329_MietwohnungenEssen.csv", sep=";", header=0)
descrArray = data['beschreibung']

#fiter_set fuellen
filter_set = set()
file = open("Filter.txt", "r")
for line in file:
    line = line.rstrip("\n")
    words = line.split(",")
    #letztes element entfernen falls leer
    if(words[-1] == ""):
        words.remove(words[-1])
    #zu filter_set hinzufuegen
    for word in words:
        word = word.strip()
        filter_set.add(word)
file.close()

for text in descrArray:
    local_counter = Counter()

    tokenized_text, ngrams = zip(*prepare_description(text))
    nouns = filter_nouns(tokenized_text, local_counter)

    #Schnittmenge aus 'nomen' und 'filter_set' bilden
    result_nouns = nouns.intersection(filter_set)

    for word in result_nouns:
        local_counter[word] += 1

    #N-gramme zu set konvertiern um das verschneiden vorzubereiten
    ngrams_set = ngrams_to_set(ngrams)

    #In filter_set nach ngrammen suchen und nur die gefundenen behalten
    result_ngrams = ngrams_set.intersection(filter_set)

    #N-gramme zu local_counter hinzufügen
    for ngram in result_ngrams:
       local_counter[ngram] += 1

    #Diese zur übergreifenden Countliste hinzufügen
    counter += local_counter

# Liste der x häufigsten Wörter/Nomen ausgeben
result = counter.most_common(10)
f = open("result.txt", "a")
for word in result:
    f.write(word[0] + ": " + str(word[1]) + "\n")
f.write("----------------------------")
f.close()

print("Text Mining beendet")
