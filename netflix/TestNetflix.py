#!/usr/bin/env python3

# -------------------------------
# projects/netflix/TestNetflix.py
# Copyright (C) 2015
# Glenn P. Downing
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io       import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_eval,  \
                    netflix_print, netflix_solve, \
                    netflix_rmse, netflix_rmse_from_dictionary

import math

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase) :

    # ----
    # read
    # ----

    def test_read_1 (self) :
        input_string = StringIO("1:\n"\
            "30878\n"\
            "26\n"\
            "10:\n"\
            "23\n"\
            "54\n"\
            "20:\n"\
            "30\n"\
            "26\n"\
            "54\n")
        dictionary = {1 : (30878, 26), 10 : (23, 54), 20 : (30, 26, 54)}
        self.assertEqual(dictionary, netflix_read(input_string))

    def test_read_2 (self) :
        input_string = StringIO("1:\n3\n275\n2:\n2\n454")
        dictionary = {1 : (3,275), 2 : (2, 454)}
        self.assertEqual(dictionary, netflix_read(input_string))

    def test_read_3 (self) :
        input_string = StringIO("")
        dictionary = {}
        self.assertEqual(dictionary, netflix_read(input_string))

    # ----
    # eval
    # ----

    def test_eval_1 (self) :
        input_dictionary  = {1 : (30878, 2647871, 1283744)}
        output_dictionary = netflix_eval(input_dictionary)
        self.assertEqual({1 : (3.6503057739484501, 3.3045105104107062, 3.6865857791323067)}, output_dictionary)

    def test_eval_2 (self) :
        input_dictionary  = {1 : (30878, 2647871, 1283744), 10 : (1952305, 1531863)}
        output_dictionary = netflix_eval(input_dictionary)
        self.assertEqual({1 : (3.6503057739484501, 3.3045105104107062, 3.6865857791323067), 10: (3.3265579801724381, 3.172787956336625)}, output_dictionary)

    def test_eval_3 (self) :
        input_dictionary  = {}
        output_dictionary = netflix_eval(input_dictionary)
        self.assertEqual({}, output_dictionary)

    # -----
    # print
    # -----

    def test_print_1 (self) :
        output_stream = StringIO()
        output_dictionary = {1 : (1, 2, 3)}
        rmse_value = 1
        netflix_print(output_stream, output_dictionary, rmse_value)
        self.assertEqual("1:\n1.0\n2.0\n3.0\nRMSE: 1.00\n", output_stream.getvalue())

    def test_print_2 (self) :
        output_stream = StringIO()
        output_dictionary = {1 : (1, 2, 3), 2 : (1, 2, 3)}
        rmse_value = 1
        netflix_print(output_stream, output_dictionary, rmse_value)
        self.assertEqual("1:\n1.0\n2.0\n3.0\n2:\n1.0\n2.0\n3.0\nRMSE: 1.00\n", output_stream.getvalue())

    def test_print_3 (self) :
        output_stream = StringIO()
        output_dictionary = {}
        rmse_value = 1
        netflix_print(output_stream, output_dictionary, rmse_value)
        self.assertEqual("RMSE: 1.00\n", output_stream.getvalue())

    # -----
    # solve
    # -----

    def test_solve_1 (self) :
        input_string = StringIO("1:\n30878\n2647871\n10:\n1952305\n1531863\n")
        output_string = StringIO()
        netflix_solve(input_string, output_string)
        self.assertEqual("1:\n3.7\n3.3\n10:\n3.3\n3.2\nRMSE: 0.00\n", output_string.getvalue())

    def test_solve_2 (self) :
        input_string = StringIO()
        output_string = StringIO()
        netflix_solve(input_string, output_string)
        self.assertEqual("RMSE: 0.00\n", output_string.getvalue())

    def test_solve_3 (self) :
        input_string = StringIO("10:\n1952305\n1:\n30878\n")
        output_string = StringIO()
        netflix_solve(input_string, output_string)
        self.assertEqual("1:\n3.7\n10:\n3.3\nRMSE: 0.00\n", output_string.getvalue())

    # ----
    # rmse
    # ----

    def test_rmse0 (self) :
        self.assertEqual(netflix_rmse((2, 3, 4), (2, 3, 4)), 0)

    def test_rmse1 (self) :
        self.assertEqual(netflix_rmse((2, 3, 4), (3, 2, 5)), 1)

    def test_rmse2 (self) :
        self.assertEqual(netflix_rmse((2, 3, 4), (4, 1, 6)), 2)

    def test_rmse16 (self) :
        self.assertEqual(netflix_rmse((2, 3, 4), (4, 3, 2)), 1.632993161855452)

    # --------------------
    # rmse_from_dictionary
    # --------------------

    def test_rmse_from_dictionary_1 (self) :
        list1 = {1 : (2, 3, 4)}
        list2 = {1 : (2, 3, 4)}
        self.assertEqual(0, netflix_rmse_from_dictionary(list1, list2))

    def test_rmse_from_dictionary_2 (self) :
        list1 = {1 : (2, 3, 4), 2 : (2, 3, 4)}
        list2 = {1 : (2, 3, 4), 2 : (2, 3, 4)}
        self.assertEqual(0, netflix_rmse_from_dictionary(list1, list2))

    def test_rmse_from_dictionary_3 (self) :
        list1 = {}
        list2 = {}
        self.assertEqual(0, netflix_rmse_from_dictionary(list1, list2))

# ----
# main
# ----

if __name__ == "__main__" :
    main()

"""
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
Name          Stmts   Miss Branch BrMiss  Cover   Missing
---------------------------------------------------------
Netflix          18      0      6      0   100%
TestNetflix      33      1      2      1    94%   79
---------------------------------------------------------
TOTAL            51      1      8      1    97%
"""
