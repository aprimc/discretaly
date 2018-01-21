
def get_row(i, w):
    return list(range(i*2 + 1, i*2 + 1 - w, -1))


def _all_frequencies(w, m, ks):
    k = min(m, ks[0])
    for f0 in range(k + 1):
        if w == 1:
            yield [f0]
        else:
            for fs in _all_frequencies(w - 1, max(0, k - f0), ks[1:]):
                yield [f0] + fs


def all_frequencies(w, ks):
    return list(_all_frequencies(w, max(ks), ks))


def row_ks(i, w, k0, kn):
    j = i + 1  # convert zero based to one based row index
    n = (w - 1) // 2
    if j <= n:
        ks = [k0] * j + [0] * (w - j)
        #print(ks)
        return ks
    if j <= 2 * n:
        ks = [k0 + kn] * j + [kn] * (w - j)
        #print(ks)
        return ks
    ks = [k0 + kn] * w
    #print(ks)
    return ks


def filter_frequencies(i, fs, ms1_vs1, ks):
    ms1, vs1 = ms1_vs1
    k = max(ks)
    w = len(ks)
    n2 = w - 1
    n = n2 // 2
    ms = []  # maximum frequency
    vs = []  # maximum frequency in the bottom left triangle
    for j, f in enumerate(fs):
        if j:
            m = f + max(ms[-1], ms1[j - 1])

            if m > k:
                return None

            v = 0
            if n <= i < n2 and j > i:
                # we are in the bottom left triangle
                v = f + vs1[j - 1]
                if j - 1 > i:
                    # previous value is also in the bottom left triangle
                    v = max(v, f + vs[-1])

                if v > ks[j]:
                    return None

            ms.append(m)
            vs.append(v)
        else:
            # first element: nothing before or above
            if f > k:
                return None
            ms.append(f)
            vs.append(f)

    return (ms, vs)


def row_value(row, fs):
    # return sum(n*f for n, f in zip(row, fs))
    s = 0
    for v, f in zip(row, fs):
        s += v * f
    return s


if __name__ == '__main__':
    N = 40  #18 #26
    l = 3
    k0, kn = 2, 1
    k = k0 + kn
    print('# ks:', [k0, kn], 'l:', l)
    w = 2*l + 1
    i = 0
    frequencies = {}
    rows0 = [(0, ([0]*w, [0]*w))]
    while True:
        rows1 = []
        values1 = get_row(i, w)
        min_next_row = min(x for x in get_row(i + 1, w) if x > 0)
        rks = row_ks(i, w, k0, kn)
        afs = list(all_frequencies(len(values1), rks))
        for value0, ms0_vs0 in rows0:
            for fs1 in afs:
                ms_vs = filter_frequencies(i, fs1, ms0_vs0, rks)
                if ms_vs is None:
                    continue
                value1 = row_value(values1, fs1) + value0
                if value1 <= N:
                    if value1 > value0:
                        frequencies[value1] = 1 + frequencies.get(value1, 0)
                    if value1 <= N - min_next_row:
                        rows1.append((value1, ms_vs))
        if values1[-1] > 0:
            print(values1[-1], frequencies.get(values1[-1], 0))
            print(values1[-2], frequencies.get(values1[-2], 0))
            if max(values1[-2:]) >= N:
                break
        i += 1
        rows0 = rows1

