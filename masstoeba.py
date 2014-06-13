import utility
import sentencesplitter
import wordtokenizer
import string
import re
# lines = utility.file_generator('kafka.txt')

with open('kafka.txt', 'rb') as f:
    text = f.read().decode('utf-8')


lines = sentencesplitter.splitter(text, 'eng')


min_thresh = 4
max_thresh = 12
count = 0
counttot = len(lines)
count_above_max = 0
count_below_min = 0
count_dialogue = 0


def punc_strippers(line):
    '''To strip all punctuation and spaces from both sides.
    '''
    unwanted = string.punctuation + ' '

    return line.strip(unwanted)+'.'


sent_dia = []

for i in range(0, len(lines)):
    #normalizing wrapped test
    lines[i] = utility.unwrapper(lines[i], '\r\n')
    sent_words = wordtokenizer.wordtokenizer('eng', lines[i])
    numwords = len(sent_words)
    # print lines[i].encode('utf-8')
    # print '\n'
    if numwords >= min_thresh and numwords <= max_thresh:
        count = count + 1
        # print lines[i]
        # print punc_strippers(lines[i])
        # print '\n'
    if numwords > max_thresh:
        dialogues = re.findall(r'"(.*?)"', lines[i])
        # print dialogues
        for dialogue in dialogues:
            wrdcnt = len(wordtokenizer.wordtokenizer('eng', dialogue))
            if wrdcnt >= 4:
                # print dialogue.encode('utf-8')
                sent_dia.append(dialogue)
                count_dialogue += 1
        count_above_max += 1
    if numwords < min_thresh:
        count_below_min += 1

# for line in lines:
#     print line
#     print '___'

print 'Total sentences = ', counttot
print 'Sentences <> thresholds = ', count
print 'Sheentences < threshold = ', count_below_min
print 'Sentences > thresholds = ', count_above_max

print 'New sentences got from Dialogues are ', count_dialogue

for sent in sent_dia:
    # print sent.encode('utf-8')
    print punc_strippers(sent)
    print '\n'

# k =  lines[80]
# print k
# print k.replace('\r\n', ' ')