import subprocess
import re
import matplotlib.pyplot as plt


def sortF(x):
    return int(x.split('\t')[0][2:])


def slen(x):
    return len(x.split(' '))


def length_analysis(model_number):
    with open(f"model{model_number}.out", "r") as file1:
        data = file1.readlines()
        fil_data = sorted(
            filter(lambda x: x[0] in ['S', 'T', 'H'], data), key=sortF)
        sep_data = list(map(lambda x: "".join(
            list(x.split('\t')[2 if x[0] == 'H' else 1])), fil_data))
        data = [[], [], []]  # S T H

        for i in range(len(fil_data)):
            data[i % 3] += [sep_data[i]]

        a = sorted(zip(data[0], data[1], data[2]), key=lambda x: slen(x[0]))
        result = []
        for i in range(slen(a[-1][0])//10+1):
            data = list(filter(lambda x: slen(x[0]) < (
                i+1)*10 and slen(x[0]) >= (i)*10, a))
            T = [i[1] for i in data]
            H = [i[2] for i in data]

            if len(data) > 10:
                with open('T.out', 'w') as f1, open('H.out', 'w') as f2:
                    f1.writelines(T)
                    f2.writelines(H)
                tmp = subprocess.check_output(
                    "fairseq-score --sys ./H.out --ref ./T.out", shell=True)
                tmp = re.findall(
                    r'(?<=BLEU4 = )\d.*(?= \()', tmp.decode('utf-8'))[0]
                tmp = re.split('/|, ', tmp)
                tmp = list(map(lambda x: float(x), tmp))+[len(data), i]
                result += [tmp]
    return result


def chart(result, model_number):
    X = [i[6] for i in result]
    X = list(map(lambda x: f'{x*10}-{(x+1)*10}', X))
    Y = [i[0] for i in result]
    plt.plot(X, Y, label="Our model", marker='o')
    plt.ylabel("Bleu Score")
    plt.xlabel("Sentence length")
    plt.legend()
    plt.savefig(f"model{model_number}.LA.png")
    print(X)


def main(model_number):
    result = length_analysis(model_number)
    chart(result, model_number)


main(48)
