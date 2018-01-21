#!/usr/bin/env python3

from functools import lru_cache


@lru_cache(maxsize=None)
def mod_part(n, r, m, sm=1):
    if n == 0:
        return [[]]
    L = []
    for i in range(sm, n + 1):
        if i % m not in r:
            continue
        for L1 in mod_part(n - i, r, m, sm):
            if L1 == [] or i >= L1[-1]:
                L.append(L1 + [i])
    return L


def partition(n):
    if n == 0:
        yield []
        return
    for p in partition(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]


if __name__ == '__main__':
    for num in range(1, 27):
        L = []
        for n1 in range(0, num + 1):
            for n2 in range(0, num - n1 + 1):
                for n3 in range(0, num - n1 - n2 + 1):
                    for p1 in mod_part(n1, (1,), 2, 1):
                        for p2 in mod_part(n2, (4, 5, 6), 10, 1):
                            for p3 in mod_part(n3, (2, 8), 10, 1):
                                if sum(p1) + sum(p2) + sum(p3) != num:
                                    continue
                                L.append((p1, p2, p3))
        print('Congruence 3-color partitions of {}: {}'.format(num, len(L)))
        #for i, p in enumerate(sorted(L)):
        #    print(i+1, p)

