 # coding: utf-8
import wordtokenizer
import csv

def csv_generator(filename, delim):
    with open(filename,'rb') as f:
        rows = csv.reader(f, delimiter=delim)
        for row in rows:
            yield row

def translation_lookup(word):
    '''For now looks up translation from hin to english from the en_hi file from wiktionary'''
    csvgen = csv_generator('en_hi.csv','\t')
    for row in csvgen:
        print word, ' checking against ', row[1].decode('utf-8') 
        if word == row[1].decode('utf-8'):
            return row[0].decode('utf-8')
    return False



def sentencesimilarity(lang1,sentence1, lang2,sentence2):
    '''Lang1 will be converted to lang2 and then similarity between the newly translated sentece and lang2 willbe calculated
       We try to keep lang2 as english

    '''
    print 'First sentence bag got is : '
    sentence1_words = wordtokenizer.wordtokenizer(lang1,sentence1.lower())
    print sentence1_words

    print 'Second sentence bag got is : '
    sentence2_words = wordtokenizer.wordtokenizer(lang2,sentence2.lower())
    print sentence2_words

    # return '1'
    translated_sentence = []
    for word in sentence1_words:
        translated_word = translation_lookup(word)
        print translated_word
        if translated_word:
            translated_sentence.extend(translated_word.split())

    print 'Translated bag for sentence1 is : '
    print translated_sentence

    #Now we have translated sentence in bag of words format. We need to check how many of these words exist in sentence2
    same_word_count = 0
    for word in translated_sentence:
        if word in sentence2_words:
            print word
            same_word_count = same_word_count + 1

    return same_word_count


w = 'गुरु'.decode('utf-8')

print translation_lookup(w)

testsen1 = 'how much girl life'.decode('utf-8')
testsen2 = 'कितना लड़की जी'.decode('utf-8')

print testsen1.encode('utf-8')
print testsen2.encode('utf-8')

print sentencesimilarity('hin',testsen2,'eng',testsen1)