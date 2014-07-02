'''
What are the different scoring criterias?
    1. Sentence Lengths.
    2. Comparing against top words external list
    3. If first character is Uppercase or not
    4. Scoring using IDF based on existing corpus'''

import utility
import sentencesplitter
import wordtokenizer
import string
import re
import freqtoeba
import math

# lines = utility.file_generator('kafka.txt')

def topwordcheck(listwords, topwordset):
    ''' Takes in a list of words, and return the number of words that are
    in the topwordset of that language. Returns false if nothing matches.
    '''
    totwords = len(listwords)
    set_listwords = set(listwords)

    noncommonwords = set_listwords - topwordset

    count_uncommonwords = len(noncommonwords)

    count_commonwords = totwords - count_uncommonwords


    return totwords, count_commonwords, count_uncommonwords


def score_length(minlength, maxlength, senlength, equally=True):
    ''' Returns score according to the length, score according to distance
    from the midpoint of extremes.
    OR, 
    Score all sentences in the permitted thresholds equally
    '''
    midpoint = (maxlength-minlength)/2
    if equally:
        if senlength<=max_thresh and senlength >= minlength:
            return 1
        else:
            return (abs(senlength - midpoint))**(-1)
    else:
        #TODO make this better.
        #variable scoring even inside permitted length.
        base = maxlength - midpoint
        return abs(senlength - midpoint)

def score_common_words(uncommon_thresh, countinfo, equally=True ):
    ''' Return score based on number of uncommon words allowed. Countinfo is
    tuple returned by topwordcheck method. If equally is set true, then 
    sentences with uncommon words less than or equal to the threshold are
    scored equally.
    '''
    num_uncommonwords = countinfo[2]
    if equally:
        if num_uncommonwords <=uncommon_thresh:
            return 1
        else:
            return 0
    else:
        #TODO add functionality here for variable scoring
        return 1




def pop_word_set_gen(file):
    '''
    Takes in a file of popular word, with words/line and returns a set of
    words normalized into lower case.
    '''
    pop_word_set = set()
    file_generator = utility.file_generator(file)
    for line in file_generator:
        word = line.strip()
        #Now put it into set
        pop_word_set.add(word.lower())
    return pop_word_set


def if_popular(word, topwordlist):
    ''' Takes in word and checks whether its part of top word list'''
    lword = word.lower()



def punc_strippers(line):
    '''To strip all punctuation and spaces from both sides.
    '''
    unwanted = string.punctuation + ' '
    # We add fullstop to make the sentence normal again
    return line.strip(unwanted)+'.'





def score_firstchar_upper(line):
    '''Return false if first char of line not upper'''
    if line[0].isupper():
        return 1
    else:
        return 0

def iwf(word, fdist):
    '''Takes word and fdist, and returns the word frequency. Return 0 if none'''
    return fdist[word]

def score_iwf(sentence, fdist, totalsent, log=True):
    ''''''
    totscore = 0
    totf = 0
    num_words = len(sentence)
    if log:
        for word in sentence:
            totscore = totscore + math.log10(fdist[word.lower()]/totalsent)
        return totscore
    else:
        if num_words == 0:
            return 0
        for word in sentence:
            freq = fdist[word.lower()]
            if freq == 0:
                pass
            else:
                totf = totf + freq
        if totf != 0:
            return (totf/num_words)**(-1)
        else:
            return totf 

def sentence_picker(min_thresh, max_thresh, uncommon_thresh, lines, newlinechar):
    '''Return list of useful sentences picked out of dump of sentences
    given to it as input.

    Arguements min_thresh and max_thresh are the minimum and maximum
    length of sentences allowed.

    Lines is a list of sentences in unicode.

    newlinechar is the char that documents uses for newlines. Project
    Gutenberg uses '\r\n'
    '''
    sent_dia = []
    picked_sentences = {}

    weight_iwf = 1
    weight_common = 1
    weight_len = 1
    weight_firstchar = 1

    count = 0
    counttot = len(lines)
    count_above_max = 0
    count_below_min = 0
    count_dialogue = 0
    #TODO fdist should be loaded from a pickle, this takes a lot of time
    fdist = freqtoeba.fdist_gen('eng', 'sentences.csv', 'stopword/stop-words_english_1_en.txt')


    #We create the set initially here so that we don't have to create
    # it time and again.
    topwordset = pop_word_set_gen('wikifiction.txt')

    for i in range(0, len(lines)):

        #normalizing wrapped test
        lines[i] = utility.unwrapper(lines[i], newlinechar)




        #tokenizing each sentence into words which are lowercase
        sent_words = wordtokenizer.wordtokenizer('eng', lines[i])

        sentlen = len(sent_words)
        # print lines[i].encode('utf-8')
        # print 'h\n'


        sent_less_stop_words = utility.less_stopwords(sent_words)


        sentlen_less_stop_words = len(sent_less_stop_words)





        #TODO For the time being , later get better score using missing vocab

        score = 0

        score = score + weight_len * score_length(min_thresh, max_thresh, sentlen, equally=True)
        score = score + weight_firstchar * score_firstchar_upper(lines[i])

        countinfo = topwordcheck(sent_less_stop_words, topwordset)

        score = score + weight_common * score_common_words(uncommon_thresh, countinfo, equally=True)

        score = score + weight_iwf * score_iwf(sent_less_stop_words, fdist, counttot, True)
        # print lines[i], score_iwf(sent_less_stop_words, fdist)

        picked_sentences[lines[i]] = score


        if sentlen > max_thresh:
            dialogues = re.findall(r'"(.*?)"', lines[i])
            for dialogue in dialogues:
                score = 0
                dia_words = wordtokenizer.wordtokenizer('eng', dialogue)
                dialen = len(dia_words)
                dia_less_stop_words = utility.less_stopwords(dia_words)
                dialen_less_stop_words = len(dia_less_stop_words)
                countinfo = topwordcheck(dia_less_stop_words, topwordset)

                score = score + weight_len * score_length(min_thresh, max_thresh, dialen, equally=True)
                score = score + weight_firstchar * score_firstchar_upper(dialogue)
                score = score + weight_common * score_common_words(uncommon_thresh, countinfo, equally=True)
                score = score + weight_iwf * score_iwf(dia_less_stop_words, fdist, counttot, True)
                # print dialogue, score_iwf(dia_less_stop_words, fdist)
                picked_sentences[dialogue] = score



    #     if sentlen >= min_thresh and sentlen <= max_thresh:
    #         count = count + 1
    #         # print lines[i]

    #         num_common_words = topwordcheck(sent_less_stop_words, topwordset)[1]
    #         if num_common_words < sentlen_less_stop_words-1:
    #             continue
    #         if not is_firstchar_upper(lines[i]):
    #             continue

    #         picked_sentences[punc_strippers(lines[i])] = score
    #         # print '\n'

    #     if sentlen > max_thresh:
    #         dialogues = re.findall(r'"(.*?)"', lines[i])
    #         # print dialogues
    #         for dialogue in dialogues:
    #             dia_words = wordtokenizer.wordtokenizer('eng', dialogue)
    #             wrdcnt = len(dia_words)
    #             dia_less_stop_words = utility.less_stopwords(dia_words)
    #             dialen_less_stop_words = len(dia_less_stop_words)
    #             score = dialen_less_stop_words
    #             if wrdcnt >= 4:
    #                 # print dialogue.encode('utf-8')

    #                 num_common_words = topwordcheck(dia_less_stop_words, topwordset)[1]
    #                 if num_common_words < dialen_less_stop_words-1:
    #                     continue
    #                 if not is_firstchar_upper(dialogue):
    #                     continue

    #                 sent_dia.append(dialogue)
    #                 picked_sentences[dialogue] = score
                    
    #                 count_dialogue += 1
    #         count_above_max += 1
    #     if sentlen < min_thresh:
    #         count_below_min += 1


    return picked_sentences

# for line in lines:
#     print line
#     print '___'

# print 'Total sentences = ', counttot
# print 'Sentences <> thresholds = ', count
# print 'Sheentences < threshold = ', count_below_min
# print 'Sentences > thresholds = ', count_above_max

# print 'New sentences got from Dialogues are ', count_dialogue


min_thresh = 4
max_thresh = 12
uncommon_thresh = 1
with open('kafka.txt', 'rb') as f:
    text = f.read().decode('utf-8')


lines = sentencesplitter.splitter(text, 'eng')


picked = sentence_picker(min_thresh, max_thresh, uncommon_thresh, lines, '\r\n')



import operator

sorted_picked = sorted(picked.iteritems(), key=operator.itemgetter(1))


for pick in sorted_picked:

    print pick
    
print len(sorted_picked)

# for sent in sent_dia:
#     # print sent.encode('utf-8')
#     print punc_strippers(sent)
#     print '\n'

# k =  lines[80]
# print k
# print k.replace('\r\n', ' ')


