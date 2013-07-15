#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sudoku


class TestSudoku(unittest.TestCase):
    """docstring for TestSudoku"""
    def setUp(self):
        self.sudoku = sudoku.Sudoku()
        self.sudoku.load_from_file('s4.txt')
        
    def tearDown(self):
        self.sudoku = None

    def test_find_singles(self):
        self.assertEqual(self.sudoku.find_singles(), [
            {'col': 1, 'value': '4', 'row': 3},
            {'col': 7, 'value': '1', 'row': 3},
            {'col': 4, 'value': '7', 'row': 4},
            {'col': 1, 'value': '8', 'row': 5},
            {'col': 7, 'value': '7', 'row': 5},
            {'col': 2, 'value': '1', 'row': 8},
            {'col': 0, 'value': '1', 'row': 4},
            {'col': 3, 'value': '8', 'row': 4},
            {'col': 8, 'value': '5', 'row': 4},
            {'col': 3, 'value': '2', 'row': 0},
            {'col': 5, 'value': '9', 'row': 4}
        ], 'find wrong singles')

    def test_
if __name__ == '__main__':
    unittest.main()
