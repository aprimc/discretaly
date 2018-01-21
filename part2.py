"""
part.py

Build partitions bottom-up.
"""


def get_row(i, w):
    """Get the list of values in row `i` of width `w`. Values are reversed.
    get_row(0, 3)
    [1]
    get_row(1, 3)
    [3, 2]
    get_row(2, 3)
    [5, 4, 3]
    get_row(3, 3)
    [7, 6, 5]
    """

    w = min(i + 1, w)
    return list(range(i*2 + 1, i*2 + 1 - w, -1))


def all_frequencies(w, k):
    for f0 in range(k + 1):
        if w == 1:
            yield [f0]
        else:
            for fs in all_frequencies(w - 1, max(0, k - f0)):
                yield [f0] + fs


def filter_frequencies(fs, ms1, k):
    """Filter frequencies `fs` using maximums `ms` from row above.

    Return maximums for the row or None.
    """
    ms = []
    for j, f in enumerate(fs):
        if j:
            # faster: m = f + max(ms[-1], ms1[j - 1])
            m = ms1[j - 1]
            m0 = ms[-1]
            if m0 > m:
                m = m0
            m += f

            if m > k:
                return None
            ms.append(m)
        else:
            # first element: nothing before or above
            ms.append(f)
    return ms


def row_value(row, fs):
    """
    >>> row_value([3, 2], [1, 1])
    5
    """
    # faster: return sum(n*f for n, f in zip(row, fs))
    s = 0
    for v, f in zip(row, fs):
        s += v * f
    return s


if __name__ == '__main__':
    N = 40  #18 #26
    l = 3
    k = 2  #3
    print('k =', k, ' l =', l)
    w = 2*l + 1
    i = 0
    frequencies = {}
    rows0 = [(0, [])]
    while True:
        rows1 = []
        values1 = get_row(i, w)
        min_next_row = get_row(i + 1, w)[-1]  #
        afs = list(all_frequencies(len(values1), k))
        for value0, ms0 in rows0:
            for fs1 in afs:
                ms = filter_frequencies(fs1, ms0, k)
                if ms is None:
                    continue
                value1 = row_value(values1, fs1) + value0
                if value1 <= N:
                    if value1 > value0:
                        frequencies[value1] = 1 + frequencies.get(value1, 0)
                    if value1 <= N - min_next_row:
                        rows1.append((value1, ms))
        print(values1[-1], frequencies.get(values1[-1], 0))
        if i + 1 >= w:
            print(values1[-2], frequencies.get(values1[-2], 0))
        if max(values1[-2:]) >= N:
            break
        i += 1
        rows0 = rows1

