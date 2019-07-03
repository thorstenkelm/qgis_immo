import nltk
import pandas as pd
from string import punctuation
from nltk.corpus import stopwords
from nltk.util import everygrams
import treetaggerwrapper
from collections import Counter


class TextMiner:

    def __init__(self, data, filter, counter, most_common_length):
        self.data = data
        self.filter = self.set_filter(filter)
        self.counter = counter
        self.most_common_length = most_common_length

    def set_filter(self, file):
        # create filter_set
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
        delete punctuation
        :param s:
        :return:
        """
        return ''.join(c for c in s if c not in punctuation)

    @staticmethod
    def create_ngrams(input, min_len, max_len):
        """
        create N-grams
        min_len is the minimum length of the N-grams
        max_len is the maximum length of the N-grams
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
        # divide in sentences
        sentences = nltk.sent_tokenize(text, language='german')

        # delete punctuation
        for i in range(len(sentences)):
         sentences[i] = self.strip_punctuation(sentences[i])

        # to lowercase
        for i in range(len(sentences)):
          sentences[i] = sentences[i].lower()

        # tokenizing
        tokenized_text = [nltk.word_tokenize(sent, language='german') for sent in sentences]

        # create N-grams
        ngrams = self.create_ngrams(input=sentences,
                                    min_len=2,
                                    max_len=3)

        # delete stopwords
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
        tags = treetaggerwrapper.make_tags(tags)

        # filter nouns
        nouns = set()
        for array in tags:
          if(array[1] == "NNP" or array[1] == "NN" or
               array[1] == "NNPS" or array[1] == "NNS"):
            nouns.add(array[0])
        return nouns

    @staticmethod
    def ngrams_to_set(ngrams):
        """
        :param ngrams:
        :return:
        """
        result = set()
        for sentence in ngrams:
            for tuple in sentence:
                s = ""
                for i in range(len(tuple)):
                    if i == len(tuple)-1:
                        s += tuple[i]
                    else:
                        s += tuple[i] + " "
                result.add(s)
        return result

    @staticmethod
    def get_result(self):
        """
        :return: result
        returns a dict of x most common words
        """
        result = self.counter.most_common(self.most_common_length)
        return dict(result)

    @property
    def execute(self):
        """
        :return:
        """

        for text in self.data:

            tokenized_text, ngrams = self.prepare_description(text)
            nouns = self.filter_nouns(tokenized_text)

            # intersect 'nouns' and 'filter'
            result_nouns = nouns.intersection(self.filter)

            for word in result_nouns:
                self.counter[word] += 1

            # convert N-grams to set
            ngrams_set = self.ngrams_to_set(ngrams)

            # intersect 'ngrams_set' and 'filter'
            result_ngrams = ngrams_set.intersection(self.filter)

            # add N-grams to counter
            for ngram in result_ngrams:
                self.counter[ngram] += 1

        return self.get_result(self)


# main script
counter = Counter()

# import csv
data = pd.read_csv("2019-04-09_123329_Mietwohnungen.csv", sep=";", header=0)
descArray = data['beschreibung']

filter_file = open("Filter.txt", "r")
# length of the list of most common words
most_common_length = 10

tm = TextMiner(data=descArray,
               filter=filter_file,
               counter=counter,
               most_common_length=most_common_length)

result = tm.execute
print(type(result))
print(result)