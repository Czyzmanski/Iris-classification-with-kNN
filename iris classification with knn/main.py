def prepare_data(f):
    data = [row.strip().split(',') for row in f]
    for row in data:
        for i in range(len(row) - 1):
            row[i] = float(row[i])
    return data


def get_vect_dist(v1, v2):
    d = 0
    for i in range(len(v1) - 1):
        d += (v1[i] - v2[i]) ** 2
    return d


def get_all_dist(training, v):
    dist = []
    for t in training:
        d = get_vect_dist(t, v)
        dist.append((d, t[-1]))
    return dist


def sort(tab):
    for i in range(len(tab) - 1):
        k = i
        for j in range(i + 1, len(tab)):
            if tab[j][0] < tab[k][0]:
                k = j
        tab[i], tab[k] = tab[k], tab[i]


def classify(training, v, k):
    d2 = get_all_dist(training, v)
    sort(d2)
    poll = {}

    for i in range(k):
        dec_atrr = d2[i][1]
        if dec_atrr in poll:
            poll[dec_atrr] += 1
        else:
            poll[dec_atrr] = 1

    vmax = 0
    kmax = None
    for k, v in poll.items():
        if v > vmax:
            vmax = v
            kmax = k

    return kmax


def prompt_k():
    k = int(input('Please input number of neighbours:\n').strip())
    if k > len(training):
        k = len(training)
    return k


def prompt_v():
    v = input('Please input your testing vector, separating \
              atrributes by white spaces:\n').strip().split()
    for i in range(len(v) - 1):
        v[i] = float(v[i])
    return v


with open('test.txt') as ftest, open('train.txt') as ftrain, open('res.txt', 'w') as fres:
    testing = prepare_data(ftest)
    training = prepare_data(ftrain)
    training_len = len(training)

    print(('k   accuracy    error_rate  good_decisions   bad_decisions'))

    for k in range(1, training_len + 1):
        errors = 0
        for v in testing:
            if v[-1] != classify(training, v, k):
                errors += 1
        print(('{}  {:.4f}  {:.4f}  {}  {}'.format(k, (training_len - errors) / training_len, errors
                                                   / training_len, training_len - errors, errors)))

    k = prompt_k()
    v = prompt_v()
    print('\ndecision: {}'.format(classify(training, v, k)))

