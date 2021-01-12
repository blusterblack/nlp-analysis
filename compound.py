import re
from nltk import ngrams
from nltk import WordNetLemmatizer


def sortF(x):
    return int(x.split('\t')[0][2:])

# output a tmp.out: a file consist of sentence order and compound


def findCompound(model_number):
    lemmatizer = WordNetLemmatizer()
    with open('data.all.word') as vocabFile:
        vocab = vocabFile.read()
    with open(f"model{model_number}.out", "r") as inputFile, open('tmp.out', 'w') as fout:
        data = inputFile.readlines()
        fil_data = sorted(
            filter(lambda x: x[0] == 'S', data), key=sortF)

        for row in fil_data:
            num, sent = row.split('\t')
            for n in range(2, 5):
                for ngram in ngrams(sent.split(), n):
                    lemmatizedNgram = map(
                        lambda x: lemmatizer.lemmatize(x), ngram)
                    normalizedWord = '_'.join(lemmatizedNgram).lower()
                    if not re.search(r'[\!\?\,\.]', normalizedWord):
                        regex = rf'\b{normalizedWord}\b'
                        if re.search(regex, vocab):
                            print(num[2:]+" "+'_'.join(ngram)+'\n')
                            fout.write(num[2:]+" "+'_'.join(ngram)+'\n')


def filter_examples(model_number):
    with open('tmp.out') as compoundFile, open(f"model{model_number}.out", "r") as inputFile:
        data = inputFile.readlines()
        compoundData = compoundFile.readlines()
        compoundDict = {}
        for i in compoundData:
            k, v = i.split()
            v = v.replace('_', ' ')
            if k in compoundDict:
                compoundDict[k] += [v]
            else:
                compoundDict[k] = [v]
        print(compoundDict.items())

        def filter_func(x):
            num = x.split('\t')[0][2:]
            return x[0] in ['S', 'H', 'T'] and num in compoundDict.keys()

        fil_data = sorted(
            filter(filter_func, data), key=sortF)

        for id, i in enumerate(fil_data):
            if (i[0] == 'S'):
                num = i.split('\t')[0][2:]
                for j in compoundDict[num]:
                    fil_data[id] = re.sub(
                        re.escape(j), j.upper(), fil_data[id],
                        flags=re.IGNORECASE)
            elif (i[0] == 'H'):
                fil_data[id] = fil_data[id].split(
                    '\t')[0]+'\t'+fil_data[id].split('\t')[2]

        with open(f"model{model_number}.compound", "w") as fout:
            fout.writelines(fil_data)


# findCompound(48)
filter_examples(48)
