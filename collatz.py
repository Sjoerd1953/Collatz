# -*- coding: utf-8 -*-
"""
This module contains functions and methods that are related
to the Collatz conjecture.

===========================================================
Created on Sun Sep 29 2019
@author: Sjoerd van Staveren (sjoerd@van-staveren.net)
Version : 1.0 - Sep 29 2019
          1.1 - Oct 10 2019
          1.2 - Oct 27 2021

Version history:
    1.0 Initial version
    1.1 Names of functions in line with official terminology
        Reduced sequence added
    1.2 Added colgen(n) (Collatz sequence generator)
        Added redcolgen(n) (Collatz reduced sequence generator)
        C(n), T(n) and tst(n) are now using the generators
===========================================================
"""
def isPo2(n: int) -> bool:
    """
    Supporting function for CtoPo2()
    """
    while n % 2 == 0:
        n = n // 2

    if n == 1:
        return True
    else:
        return False

def colgen(n: int):
    """
    This function returns a generator for the Collatz sequence down to 1
    Use it as follows:

        import collatz as c
        sequence = c.colgen(10)
        print(list(sequence))

        result: [10, 5, 16, 8, 4, 2, 1]
        """
    yield n
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = n * 3 + 1
        yield n

def redcolgen(n: int):
    """
    This function returns a generator for the reduced Collatz sequence down to 1
    The sequence is reduced by dividing the even number that is the
    result of the 3n+1 step by 2 in the same step.

    Use it as follows:

        import collatz as c
        sequence = c.redcolgen(10)
        print(list(sequence))

        result: [10, 5, 8, 4, 2, 1]
        """
    yield n
    while n > 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = (n * 3 + 1) // 2
        yield n

def C(n: int) -> list:
    """
    This function returns the complete Collatz sequence down to 1
    of a given number n as a list.
    """

    return list(colgen(n))

def T(n: int) -> list:
    """
    This function returns the reduced Collatz sequence down to 1
    of a given number n as a list.
    """

    return list(redcolgen(n))

def tst(n: int) -> int:
    """
    Tst stands for total stopping time.
    This function returns the number of steps that it
    takes to reach 1.
    """

    return len(list(colgen(n)))

def st(n: int) -> int:
    """
    St stands for stopping time.
    This function returns the number of steps that it
    takes to reach a number that is smaller than the
    starting number for the first time.

    For every even starting number the st obviously is 1.
    """
    if n%2 == 0:
        return 1

    k = 0
    n_start = n

    while not (n == 1):
        k = k + 1
        if n % 2 == 0:
            n = n // 2
            if n < n_start:
                break
        else:
            n = (3 * n + 1) // 2
            k = k + 1

    return k


def residue(n: int) -> float:
    """
    For any positive integer N let E(N) and O(N) denote
    the number of elements from S0 to SD(N)-1 which are
    even or odd, respectively. Obviously O(N) + E(N) = D(N).
    Now due to the construction of the sequence we may write
    2^E(N) = 3^O(N) * N * Res(N) where Res(N) is a factor
    equal to the product of (1 + 1 / ( 3 * Si ) ) taken over
    the odd elements Si for 0 ≤ i < D(N).
    Res(N) is called the Residue of N.
    
    This function returns the Residue of a given number n
    as a float
    """
    n_start = n
    e = 0
    o = 0

    while not (n == 1):
        if n % 2 == 0:
            n = n // 2
            e = e + 1
        else:
            n = (3 * n + 1) // 2
            o = o + 1
            e = e + 1

    res_n = 2 ** e / (3 ** o * n_start)

    return float(res_n)


def completeness(n: int) -> float:
    """
    for all integers N > 1 the Completeness of N,
    C(N), is defined by C(N) = O(N) / E(N).
    
    This function returns the Completeness of a
    given number n as a float.
    """
    e = 0
    o = 0

    while not (n == 1):
        if n % 2 == 0:
            n = n // 2
            e = e + 1
        else:
            n = (3 * n + 1) // 2
            o = o + 1
            e = e + 1

    completeness = o / e

    return float(completeness)


def CtoPo2(n: int) -> list:
    """
    This function returns the Collatz sequence down to
    the first power of 2 of a given number n as a list.
    """
    seq_list = []

    while not isPo2(n):
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1

        seq_list.append(n)

    return seq_list


def uptree(n: int) -> list:
    """
    This function returns the next step in the Collatz
    sequence of a given number n from the bottom-up
    point of view as a list. This list contains either one
    or two numbers
    """
    m = []
    m.append(n * 2)
    if n % 6 == 4:
        m.append((n - 1) // 3)

    return m


class Tree:
    def __init__(self, root: int, steps: int):
        """
        This class creates a tree object with a starting
        number (root) and the height of the tree (steps).
        """
        self.root = root
        self.steps = steps

    def tree(self):
        """
        This function returns the numbers in the tree,
        starting at the given root and going a given number
        of steps up the Collatz tree, as a sorted list and
        the individual branches as a list of lists.
        
        Use it as follows:
            import collatz as c
            mytree = c.Tree(5,6)
            a, b = mytree.tree()
            
            print(a) # prints a sorted list of the numbers in the tree
            print(b) # prints the branches
        """
        root = self.root
        steps = self.steps
        tree = [root]
        branches = [[root]]

        for step in range(1, steps + 1):
            nextbranch = []
            for numbers in branches[-1]:
                newnumbers = uptree(numbers)
                nextbranch.extend(newnumbers)

            tree.extend(nextbranch)
            branches.append(nextbranch)

        return sorted(tree), branches