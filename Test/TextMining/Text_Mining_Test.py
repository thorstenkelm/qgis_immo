import nltk
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords
from nltk.util import everygrams
import treetaggerwrapper
from collections import Counter


class TextMiner:

    def __init__(self, data, filter, counter):
        self.data = data
        self.filter = self.set_filter(filter)
        self.counter = counter

    def set_filter(self, file):
        # fiter_set fuellen
        filter_set = set()

        for line in file:
            line = line.rstrip("\n")
            line = line.strip()
            filter_set.add(line)
        file.close()
        return filter_set

    @staticmethod
    def strip_punctuation(s):
        """
        entfernt Satzzeichen
        auch Punkte z.B. nach Zahlen
        :param s:
        :return:
        """
        return ''.join(c for c in s if c not in punctuation)

    @staticmethod
    def create_ngrams(input, min_len, max_len):
        """
        Bildet N-gramme
        input ist eine Liste aus Sätzen
        min_len ist die minimale Länge der N-gramme
        max_len ist die maximale Länge der N-gramme
        :param input:
        :param min_len:
        :param max_len:
        :return:
        """
        result = []
        for sent in input:
          sent_split = sent.split()
          result.append(list(everygrams(sent_split, min_len=min_len, max_len=max_len)))
        return result

    @staticmethod
    def remove_stopwords(text, stopwords):
        """

        :param text:
        :param stopwords:
        :return:
        """
        for sent in text:
            for w in sent:
                if w in stopwords:
                    sent.remove(w)


    def prepare_description(self, text):
        """

        :param text:
        :return:
        """
        #Aufteilung in Sätze
        sentences = nltk.sent_tokenize(text, language='german')

        #Satzzeichen löschen
        for i in range(len(sentences)):
         sentences[i] = self.strip_punctuation(sentences[i])

        #Tokenization
        tokenized_text = [nltk.word_tokenize(sent, language='german') for sent in sentences]

        #N-gramme bilden
        ngrams = self.create_ngrams(input=sentences,
                                    min_len=2,
                                    max_len=3)

        #Stoppwörter löschen
        stop_words = set(stopwords.words('german'))
        self.remove_stopwords(tokenized_text, stop_words)

        return tokenized_text, ngrams

    @staticmethod
    def filter_nouns(text):
        """
        Treetagger
        :param text:
        :return:
        """
        tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')
        tags = []
        for sent in text:
            tags += tagger.tag_text(sent, tagonly=True)

        time0 = time.time()
        tags = treetaggerwrapper.make_tags(tags)

        #Nomen filtern
        nouns = set()
        for array in tags:
          if(array[1] == "NNP" or array[1] == "NN" or
               array[1] == "NNPS" or array[1] == "NNS"):
            nouns.add(array[0])
        return nouns

    @staticmethod
    def ngrams_to_set(ngrams):
        """
        die einzelnen str elemente aus den tupeln extrahieren (für jeden Satz)
        dann daraus ein set erstellen
        :param ngrams:
        :return:
        """
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

    def execute(self):
        """

        :return:
        """

        for text in self.data:
            local_counter = Counter()

            tokenized_text, ngrams = self.prepare_description(text)
            nouns = self.filter_nouns(tokenized_text)

            # Schnittmenge aus 'nomen' und 'filter_set' bilden
            result_nouns = nouns.intersection(self.filter)

            for word in result_nouns:
                local_counter[word] += 1

            # N-gramme zu set konvertiern um das verschneiden vorzubereiten
            ngrams_set = self.ngrams_to_set(ngrams)

            # In filter_set nach ngrammen suchen und nur die gefundenen behalten
            result_ngrams = ngrams_set.intersection(self.filter)

            # N-gramme zu local_counter hinzufügen
            for ngram in result_ngrams:
                local_counter[ngram] += 1

            # Diese zur übergreifenden Countliste hinzufügen
            self.counter += local_counter

        # Liste der x häufigsten Wörter/Nomen ausgeben
        return self.counter.most_common(10)


# main script
print("Text Mining gestartet")
counter = Counter()

# import csv
data = pd.read_csv("2019-04-09_123329_MietwohnungenEssen.csv", sep=";", header=0)
descArray = data['beschreibung']

filter_file = open("Filter.txt", "r")

time3 = time.time()
tm = TextMiner(data=descArray,
               filter=filter_file,
               counter=counter)

result = tm.execute()

print(result)

# f = open("result.txt", "a")
# for word in result:
#     f.write(word[0] + ": " + str(word[1]) + "\n")
# f.write("----------------------------")
# f.close()

print("Text Mining beendet")
