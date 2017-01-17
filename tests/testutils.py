# -*- coding: utf-8 -*-
import os
import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_index_equal
import ast

ROOT_FOLDER_PATH = os.path.abspath("../")
SRC_FOLDER_PATH = ROOT_FOLDER_PATH + "/pysocialwatcher/"


def get_abs_file_path_in_src_folder(file_name):
    return SRC_FOLDER_PATH + file_name

def assert_data_frame_almost_equal(left, right):
    assert_frame_equal(left, right,
                           check_dtype=False,
                           check_index_type=True,
                           check_column_type=True,
                           check_frame_type=True,
                           check_less_precise=False,
                           check_names=True,
                           by_blocks=False,
                           check_exact=False)
    assert_index_equal(left.index, right.index,
                           exact=True,
                           check_names=True)