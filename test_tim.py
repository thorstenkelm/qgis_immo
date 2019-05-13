from builtins import list
from distutils.command.config import config

import nltk
import codecs
import treetaggerwrapper
import pandas as pa

#Testdaten laden
daten = pa.read_excel("C:/Users/Tim\Desktop/Sommersemester 2019/GI Projekt Immobilien/Daten/2019-04-09_123329_MietwohnungenEssen.xlsx")

# Jupyter Notebook
#display(dataframe_wetter)

#Beschreibungsspalte heruasziehen
beschreibung = daten["beschreibung"]

#Tokenization
sentences = nltk.sent_tokenize(str(beschreibung), language="german")

list = []
for sentence in sentences:
    tokenized_text = nltk.word_tokenize(sentence, language="german")
    list.append(tokenized_text)

print(list[0])

#Holen der values aus den Daten
beschreibung_list_values = beschreibung.get_values()

dict = {}
#sortieren und einzelne Wörter in Liste speichern
#for wort in list:
#       sort = sorted(wort.split())
#      list.append(sort)

sorted(list)

nouns = set()
for array in list:
    if(array[1] == "NNP" or array[1] == "NN" or array[1] == "NNPS" or array[1] == "NNS"):
        nouns.add(array[0])
print(nouns)

#Aus wortliste wörter nehmen und in einem Dictionary legen
#Gleizieitg als Value die Häufigkeit des auftretens
for wort in list:
    for i in wort:
        dict[i] = wort.count(i)
print(dict)


#Testwörter
immo_set = {"Alarmanlage", "Altbau", "Alternative Energien", "Anlieger", "Arbeitszimmer", "Architekt", "Asbest", "Aufzug", "Balkon", "Bankbürgschaft", "Barrierefreiheit",
"Baugerüst", "Bauherr", "Bauträger", "Besichtigung", "Blockheizkraftwerk", "Brandhemmende Baustoffe", "Brauchwasser", "Briefkasten", "Carport", "Courtage",
"Dachsanierung", "Dachgeschoss", "Dachschräge", "Dachterrasse", "Dämmung", "Darlehen", "Denkmalschutz", "Doppelhaus-Hälfte", "Doppelverglasung", "Eigenbedarf",
"Eigentümergemeinschaft", "Eigentumswohnung", "Einfamilienhaus", "Einheitliche", "Fassadengestaltung", "Einstiegsfreies Bad", "Emissions-bzw.Abgasnormen",
"Energetische Sanierung", "Energieausweis", "Energiesparmaßnahmen", "Erbpacht", "Erschließungskosten", "Exposé", "Fachwerkhaus", "Fahrradkeller", "Fenster",
"Fertighaus", "Feuerversicherung", "Fußbodenheizung", "Garage", "Gartenbeleuchtung", "Gartennutzung", "Gartenplanung", "Gaube", "Gebäudeversicherung",
"Geothermie", "Gewerbe im Privathaus", "Gewerblich genutzte Immobilien", "Gewerk", "Grundbuchauszug", "Grunderwerbsteuer", "Grundfläche", "Grundschuld",
"Grundschuldlöschung", "Grundsteuer", "Grundstück", "Grundstücksgrenze", "Hausnummer", "Haustiere", "Hausverwaltung", "Heizen mit Holz", "Hobbykeller",
"Hypothek", "Hypothekenbank", "Immobilie", "Immobilie vererben", "Immobilienbewertung", "Immobilienvermarktung", "Innenausbau", "Intelligente Gebäudetechnik",
"Kamin", "Kaminholzlagerung", "Kaution", "Keller", "KernsanierungKinderlärm", "Kündigungsfristen", "Kunst am Bau", "Leuchtreklame", "Loggia", "Lüften", "Makler",
"Maler-und Lackiererarbeiten", "Massivhaus", "Mehrfamilienhaus", "Mieterhöhung", "Mietminderung", "Mietvertrag", "Mülltonnen", "Musterhaus", "Nachmieter",
"Nebenkosten", "Nebenkostenabrechnung", "Neubau", "Niedrigenergiehaus", "Obergeschoss", "Passivhaus", "Provision", "Renovierung", "Rohbau", "Rollstuhlgerechtes Wohnen",
"Schaltplan", "Schimmel", "Schlüsselfertige Übergabe", "Schönheitsreparaturen", "Schornsteinfeger", "Seniorenwohnung", "Statik", "Staatliche Förderung",
"Starkstromanschluss", "Steckdosen", "Teilungserklärung", "Terrasse", "Tiefgarage", "Tilgung", "Treppenhaus", "Trockenbau", "Umzug", "Wäschekeller", "Wegerecht",
"Wintergarten", "Winterräumpflicht", "Wohnfläche", "Wohnungsbaugesellschaften", "Zwangsversteigerung"}

#Testdaten einlesen
textfile = codecs.open("test.txt", "r", "utf-8-sig")
text = textfile.read()
textfile.close()

#Tokenization
sentences = nltk.sent_tokenize(text, language="german")

list = []
for sentence in sentences:
    tokenized_text = nltk.word_tokenize(sentence, language="german")
    list.append(tokenized_text)

#Dasselbe wie sentences_tok = [nltk.tokenize.word_tokenize(sent) for sent in sentences]

#print(list)

#Treetragger verwenden für die Lemmatisierung
tagger = treetaggerwrapper.TreeTagger(TAGLANG='de')

list2 = []
list3 = []
for i in list:
    tags = tagger.tag_text(i, tagonly=True) #don't use the TreeTagger's tokenization!
    list2.append(tags)
    tags2 = treetaggerwrapper.make_tags(tags)
    list3.append(tags2)


s = set()
word = set()
art = set()
lemma = set()
for j in list3:
    for i in j:
        s.add(i)
        word.add(i.word)
        art.add(i.pos)
        lemma.add(i.lemma)

#print(lemma.intersection(immo_set))

#print(immo_set.intersection(settag))

for u in list3:
    for i in u:
        if i.pos == "NN":
            pass
          #print(settag.intersection(immo_set))



