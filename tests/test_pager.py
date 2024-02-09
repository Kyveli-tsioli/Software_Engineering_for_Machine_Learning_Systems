"""Testing the pager module."""

import unittest
import pandas as pd

class TestPager(unittest.TestCase):
    """Testing the pager."""
    def test_pager_res(self):
        # read in aki
        col_names = ['mrn', 'date']
        true_paged = pd.read_csv('../data/aki.csv', header=None, delimiter=',', names=col_names)
        client_paged = pd.read_csv('../data/preds.csv', header=None, delimiter=',', names=col_names)
        df = pd.merge(true_paged, client_paged, on=col_names, how='outer', indicator=True)
        tp = (df['_merge'] == 'both').sum()
        fn = (df['_merge'] == 'left_only').sum() # FN: in true but not paged
        fp = (df['_merge'] == 'right_only').sum() # FP: not in true but was paged
        print("True positive:", tp)
        print("False negative:", fn)
        print("False positive:", fp)
        score = calc_score(tp, fn, fp, 3)
        assert score > 0.8
        print(score)
        return

def calc_score(tp ,fn, fp, b):
    return ((1 + b**2) * tp) / ((1 + b**2)*tp + (b**2)*fn + fp)
        

if __name__ == "__main__":
    unittest.main()
