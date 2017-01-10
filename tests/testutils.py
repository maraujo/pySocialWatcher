# -*- coding: utf-8 -*-
import os
ROOT_FOLDER_PATH = os.path.abspath("../")
SRC_FOLDER_PATH = ROOT_FOLDER_PATH + "/pyfacebookmarketingcrawler/"

def get_abs_file_path_in_src(file_name):
    return SRC_FOLDER_PATH + file_name