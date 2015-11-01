#!/usr/bin/env python3

# ---------------------------
# projects/collatz/Collatz.py
# Copyright (C) 2015
# Glenn P. Downing
# ---------------------------

CACHE_SIZE = 100
cache = [0] * CACHE_SIZE

# ------------
# collatz_read
# ------------

def collatz_read (s) :
    """
    read two ints
    s a string
    return a list of two ints, representing the beginning and end of a range, [i, j]
    """
    a = s.split()
    return [int(a[0]), int(a[1])]

# --------------------
# collatz_cycle_length
# --------------------

def collatz_cycle_length (num) :
    """
    compute the cycle length
    num the number of interest
    return the cycle length
    """

    assert num > 0

    if num <= 1 :
        return 1
    add_value = 0 # used for recursive addition
    
    if num < CACHE_SIZE and cache[num] > 0 :
        return cache[num]

    if num % 2 == 0 :
        num_copy = num // 2
        add_value = 1 # one cycle
    else :
        num_copy = num + (num // 2) + 1
        add_value = 2 # two cycles, thanks to fancy math

    # recurse to next level
    cycle_length = add_value + collatz_cycle_length(num_copy)

    if num < CACHE_SIZE :
        assert cache[num] == 0 # cache value should be empty before being overwritten
        cache[num] = cycle_length

    assert cycle_length > 0

    return cycle_length


# ------------
# collatz_eval
# ------------

def collatz_eval (i, j) :
    """
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    return the max cycle length of the range [i, j]
    """

    assert i > 0 and j > 0

    max_cycle = 0

    if i > j :
        # switch the values of i and j
        i ^= j
        j ^= i
        i ^= j

    for s in range(i, j + 1) :
        current_cycle = collatz_cycle_length(s)
        if current_cycle > max_cycle :
            max_cycle = current_cycle

    assert max_cycle > 0
    return max_cycle

# -------------
# collatz_print
# -------------

def collatz_print (w, i, j, v) :
    """
    print three ints
    w a writer
    i the beginning of the range, inclusive
    j the end       of the range, inclusive
    v the max cycle length
    """
    w.write(str(i) + " " + str(j) + " " + str(v) + "\n")

# -------------
# collatz_solve
# -------------

def collatz_solve (r, w) :
    """
    r a reader
    w a writer
    """
    for s in r :
        i, j = collatz_read(s)
        v    = collatz_eval(i, j)
        collatz_print(w, i, j, v)
