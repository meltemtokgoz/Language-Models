import math
import random


def dataset(path):
    with open(path) as f:
        lines = [line.strip()[2:] for line in f]
    return lines


def Ngram(n, data):
    ngram_model = {}
    for s in data:
        s = s.split()
        if n == 3:
            s.insert(0, "<s>")
        s.insert(0, "<s>")
        s.append("</s>")
        for i in range(len(s) - n + 1):
            pair = ' '.join(s[i:i + n])
            if ngram_model.__contains__(pair):
                ngram_model[pair] += 1
            else:
                ngram_model[pair] = 1
    return ngram_model


def next(word, gram, n):
    upto = 0
    total = 0
    if n == 1:
        total = sum(v for k, v in gram.items())
        random_number = random.uniform(0, total)
        for c, w in gram.items():
            if upto + w > random_number and c != '<s>':
                return c
            upto += w
    elif n == 2:
        for c, w in gram.items():
            c = c.split()
            if c[0] == word:
                total += w
        random_number = random.uniform(0, total)
        for c, w in gram.items():
            c = c.split()
            if c[0] == word and upto + w > random_number and c != '<s>':
                return c[1]
            upto += w
    else:
        w = word.split(" ")
        for c, v in gram.items():
            key = c.split(" ")
            if key[0] == w[0] and key[1] == w[1]:
                total += v
        random_number = random.uniform(0, total)
        for c, v in gram.items():
            key = c.split(" ")
            if key[0] == w[0] and key[1] == w[1] and upto + v > random_number and c != '<s>':
                return key[1]+" "+key[2]
            upto += v


def generate(length, count, n, gram):
    sentences = []
    for c in range(count):
        generated_sentence = ""
        if n == 1 or n == 2:
            word = '<s>'
            for i in range(length):
                if i == 0:
                    find_word = next(word, gram, n)
                else:
                    new_word = next(find_word, gram, n)
                    find_word = new_word
                if find_word == '</s>':
                    break
                else:
                    if i == length-1:
                        generated_sentence += find_word
                    else:
                        generated_sentence += find_word+" "
        else:
            word = "<s> <s>"
            for i in range(length):
                if i == 0:
                    find_word = next(word, gram, n)
                else:
                    new_word = next(find_word, gram, n)
                    find_word = new_word
                find = find_word.split(" ")
                if find[1] == '</s>':
                    break
                else:
                    if i == length-1:
                        generated_sentence += find[1]
                    else:
                        generated_sentence += find[1]+" "
        sentences.append(generated_sentence)
    return sentences


def prob(sentence, n, unigram, bigram, trigram, sen_count):
    word = sentence.split(" ")
    result = 1
    # for uni-gram
    if n == 1:
        total = sum(v for k, v in unigram.items())
        for i in range(len(word)):
            if word[i] in unigram.keys():
                word_value = unigram[word[i]]
            else:
                return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            word_prob = word_value / total
            result *= word_prob
        return result
    # for bi-gram
    elif n == 2:
        for i in range(len(word)):
            if i == 0:
                val = "<s>"+" "+word[i]
                if val in bigram.keys():
                    word_prob = bigram[val] / unigram["<s>"]
                else:
                    return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            elif i != (len(word)-1):
                val = word[i-1]+" "+word[i]
                val2 = word[i-1]
                if val in bigram.keys() and val2 in unigram.keys():
                    word_prob = bigram[val] / unigram[val2]
                else:
                    return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            result *= word_prob
        return result
    # for tri-gram
    else:
        for i in range(len(word)-1):
            if i == 0:
                val = "<s>" + " " + "<s>" + " " + word[i]
                if val in trigram.keys():
                    word_value = trigram[val]
                    word_prob = word_value / sen_count
                else:
                    return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            elif i == 1:
                val = "<s>" + " " + word[i - 1] + " " + word[i]
                val2 = "<s>"+" "+word[i - 1]
                if val in trigram.keys() and val2 in bigram.keys():
                    word_prob = trigram[val] / bigram[val2]
                else:
                    return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            else:
                val = word[i - 1] + " " + word[i] + " " + word[i + 1]
                val2 = word[i - 1]+" "+word[i]
                if val in trigram.keys() and val2 in bigram.keys():
                    word_prob = trigram[val] / bigram[val2]
                else:
                    return sprob(sentence, n, unigram, bigram, trigram, sen_count)
            result *= word_prob
        return result


def sprob(sentence, n, unigram, bigram, trigram, sen_count):
    word = sentence.split(" ")
    result = 1
    # for uni-gram
    if n == 1:
        V = len(unigram.keys())
        total = sum(v for k, v in unigram.items())
        for i in range(len(word)):
            if word[i] in unigram.keys():
                word_value = unigram[word[i]]
            else:
                word_value = 0
            word_prob = (word_value +1) / (total+V)
            result *= word_prob
        return result
    # for bi-gram
    elif n == 2:
        V = len(bigram.keys())
        for i in range(len(word)):
            if i == 0:
                val = "<s>"+" "+word[i]
                if val in bigram.keys():
                    word_value = bigram[val]
                else:
                    word_value = 0
                word_prob = (word_value + 1) / (unigram["<s>"]+V)
            elif i != (len(word)-1):
                val = word[i-1]+" "+word[i]
                val2 = word[i-1]
                if val in bigram.keys():
                    word_value = bigram[val]
                else:
                    word_value = 0
                if val2 in unigram.keys():
                    N = unigram[val2]
                else:
                    N = 0
                word_prob = (word_value + 1) / (N+V)
            result *= word_prob
        return result
    # for tri-gram
    else:
        V = len(trigram.keys())
        for i in range(len(word)-1):
            if i == 0:
                val = "<s>" + " " + "<s>" + " " + word[i]
                if val in trigram.keys():
                    word_value = trigram[val]
                else:
                    word_value = 0
                word_prob = (word_value + 1) / (sen_count + V)
            elif i == 1:
                val = "<s>" + " " + word[i - 1] + " " + word[i]
                val2 = "<s>"+" "+word[i - 1]
                if val in trigram.keys():
                    word_value = trigram[val]
                else:
                    word_value = 0
                if val2 in bigram.keys():
                    N = bigram[val2]
                else:
                    N = 0
                word_prob = (word_value + 1) / (N+V)
            else:
                val = word[i - 1] + " " + word[i] + " " + word[i + 1]
                val2 = word[i - 1]+" "+word[i]
                if val in trigram.keys():
                    word_value = trigram[val]
                else:
                    word_value = 0
                if val2 in bigram.keys():
                    N = bigram[val2]
                else:
                    N = 0
                word_prob = (word_value + 1) / (N+V)
            result *= word_prob
        return result


def ppl(sentence, probability):
    N = len(sentence)
    if N > 0:
        perp = math.pow(probability, (1/-N))
        return perp
    else:
        return "perplexity does not exist"


def main():
    folderPath = "assignment1-dataset.txt"
    data = dataset(folderPath)

    unigram = Ngram(1, data)
    bigram = Ngram(2, data)
    trigram = Ngram(3, data)

    sen_count = len(data)
    # changes values
    count = 1
    length = 15
    n = 2
    gram = bigram

    sentences = generate(length, count, n, gram);
    print(sentences)

    for s in range(count):
        print("Sentence-", s+1, ": ", sentences[s])
        for i in range(1, 4):
            # prob(sentence, n, unigram, bigram, trigram, sen_count):
            prob_value = prob(sentences[s], i, unigram, bigram, trigram, sen_count)
            print(i, "-gram probability : ", prob_value)

            perplexity = ppl(sentences[s], prob_value)
            print(i, "-gram Perplexity : ",  perplexity)


if __name__ == '__main__':
    main()
