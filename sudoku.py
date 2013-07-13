#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Sudoku(object):

    CELLS_IN_BOXES = {
        0: {'rows': {0, 1, 2}, 'cols': {0, 1, 2}},
        1: {'rows': {0, 1, 2}, 'cols': {3, 4, 5}},
        2: {'rows': {0, 1, 2}, 'cols': {6, 7, 8}},
        3: {'rows': {3, 4, 5}, 'cols': {0, 1, 2}},
        4: {'rows': {3, 4, 5}, 'cols': {3, 4, 5}},
        5: {'rows': {3, 4, 5}, 'cols': {6, 7, 8}},
        6: {'rows': {6, 7, 8}, 'cols': {0, 1, 2}},
        7: {'rows': {6, 7, 8}, 'cols': {3, 4, 5}},
        8: {'rows': {6, 7, 8}, 'cols': {6, 7, 8}}
    }

    FULL = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

    def __init__(self):
        self.sudoku = []

    def load_from_file(self, file):
        f = open(file, 'r')

        for row in f:
            self.sudoku.append(row.split())

        f.close()

    def is_all_digit(self):
        for r in self.sudoku:
            for c in r:
                if not c.isdigit():
                    return False
        return True

    def __str__(self):
        s = '+-------+-------+-------+\n'
        i = 0
        for r in self.sudoku:

            s = s + '| {0} {1} {2} | {3} {4} {5} | {6} {7} {8} |\n'.format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8])
            if i == 2 or i == 5:
                s = s + '+-------+-------+-------+\n'

            i += 1
        s = s + '+-------+-------+-------+\n'
        return s.replace('0', '-')

    def check_row(self, i):
        row = set(self.sudoku[i])
        row = self.FULL.difference(row)
        #print(print('Row #{0}: {1}'.format(i, row)))
        return row

    def check_col(self, i):
        col = set()
        for r in self.sudoku:
            col.add(r[i])

        col = self.FULL.difference(col)
        #print(print('Col #{0}: {1}'.format(i, col)))
        return col

    def check_box(self, i):

        box = {self.sudoku[r][c] for r in self.CELLS_IN_BOXES[i]['rows'] for c in self.CELLS_IN_BOXES[i]['cols']}

        # print(box)

        box = self.FULL.difference(box)
        # print('Box #{0}: {1}'.format(i, box))

        return box

    def check_rows(self):
        t = []
        for i in range(len(self.sudoku)):
            t.append(self.check_row(i))
        return t

    def check_cols(self):
        t = []
        for i in range(len(self.sudoku)):
            t.append(self.check_col(i))
        return t

    def check_boxes(self):
        t = []
        for i in range(len(self.sudoku)):
            t.append(self.check_box(i))
        return t

    def check_cell(self, row, col):

        cell = self.sudoku[row][col]
        if cell != '0':
            #print(cell)
            return cell

        row_set = self.check_row(row)
        col_set = self.check_col(col)

        for box in self.CELLS_IN_BOXES.keys():
            if row in self.CELLS_IN_BOXES[box]['rows'] and col in self.CELLS_IN_BOXES[box]['cols']:
                    box_set = self.check_box(box)

        diff = self.FULL.intersection(row_set, col_set, box_set)
        #print('Cell [{0}, {1}] can be in {2}'.format(row, col, diff))
        return diff

    def check_cells(self):
        t = []
        for row in range(len(self.sudoku)):
            for col in range(len(self.sudoku)):
                cell = self.sudoku[row][col]
                if cell == '0':
                    t.append({
                        'row': row,
                        'col': col,
                        'poss_values': self.check_cell(row, col)
                    })
        #print(t)
        return t

    def find_singles(self):
        while True:
            poss_values = self.check_cells()
            if len(poss_values) == 0:
                break

            has_one_poss_value = False
            for cell in poss_values:
                if len(cell['poss_values']) == 1:
                    row = cell['row']
                    col = cell['col']
                    self.sudoku[row][col] = cell['poss_values'].pop()
                    #print(self)
                    has_one_poss_value = True

            if not has_one_poss_value:
                break

        print('Find singles \n')
        print(self)

    def find_hiden_singles_in_rows(self):
        poss_values = self.check_cells()

        if len(poss_values) == 0:
            return

        rows = {}
        for cell in poss_values:
            row = cell['row']
            if row in rows:
                rows[row] += list(cell['poss_values'])
            else:
                rows[row] = list(cell['poss_values'])

        for r in rows:
            for v in rows[r]:
                if rows[r].count(v) == 1:
                    #print('In row {0} = {1}'.format(r, v))

                    for cell in poss_values:
                        if cell['row'] == r and v in cell['poss_values']:
                            self.sudoku[r][cell['col']] = v
                            #print(self)
        print('Hiden singles in row')
        print(self)

    def find_hiden_singles_in_cols(self):
        poss_values = self.check_cells()

        if len(poss_values) == 0:
            return

        cols = {}
        for cell in poss_values:
            col = cell['col']
            if col in cols:
                cols[col] += list(cell['poss_values'])
            else:
                cols[col] = list(cell['poss_values'])

        for c in cols:
            for v in cols[c]:
                if cols[c].count(v) == 1:
                    #print('In col {0} = {1}'.format(c, v))

                    for cell in poss_values:
                        if cell['col'] == c and v in cell['poss_values']:
                            self.sudoku[cell['row']][c] = v
                            #print(self)
        print('Hiden singles in col')
        print(self)

    def find_hiden_singles_in_boxes(self):
        pass

    def solve(self):
        i = 0
        while i < 5:

            poss_values_before = self.check_cells()
            self.find_singles()
            self.find_hiden_singles_in_rows()
            self.find_hiden_singles_in_cols()
            self.find_hiden_singles_in_boxes()

            poss_values_after = self.check_cells()

            if len(poss_values_after) == 0:
                break
            if poss_values_before == poss_values_after:
                print("There aren't changes")
                break

            i += 1

        if len(self.check_cells()) == 0:
            print('Sudoku is done')
        else:
            print('I can\'t solve this sudoku :(')

if __name__ == '__main__':
    sudoku = Sudoku()
    sudoku.load_from_file('s4.txt')
    print(sudoku)
    #sudoku.check_rows()
    #sudoku.check_col(0)
    #sudoku.check_cols()
    #sudoku.check_box(0)
    # sudoku.check_boxes()
    #sudoku.check_cell(0, 1)
    #sudoku.check_cells()
    sudoku.solve()
