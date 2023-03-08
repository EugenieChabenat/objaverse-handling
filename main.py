import objaverse
import random 
import json 
import pandas as pd 
import xlwt
from xlwt import Workbook
import multiprocessing

import argparse
import os 
import warnings
import time 

processes = 1 

# parse arguments 
parser = argparse.ArgumentParser(description='Objaverse Handling')

parser.add_argument('-fe', '--final_excel', default='result_files/test_excel_cat.xls', 
                   type=str, help='name and path of the file where the final excel sheet will be stored')

parser.add_argument('-s', '--subset_categories', default=None, 
                    type=str, help='name of the doc where to find the categories to download from')

parser.add_argument('-d', '--dict_uid', default= None, type=str, 
                    help='name of the file where to store the dictionary of uids')

parser.add_argument('-r', '--removed_uids', default=None, type=str, 
                    help='name of the file where to store the dict with removed uids')

parser.add_argument('-nb', '--nb_objects', default=5, type=int, 
                   help='number of objects to download per category of objects')

parser.add_argument('-nc', '--nb_categories', default=10, type=int, 
                   help='number of categories of objects to download from objaverse')

parser.add_argument('-np', '--nb_processes', default=1, type=int, 
                    help='number of processes to use to download from objaverse')

parser.add_argument('-m', '--multiprocessing', default=False, type=bool, 
                    help='whether to use multiprocessing to download from objaverse or not')

parser.add_argument('--seed', default=None, type=int,
                    help='seed for initializing random processes')
def main(): 
  args = parser.parse_args()
  
  if args.seed is not None: 
    random.seed(args.seed)
   
  if args.multiprocessing: 
    processes = multiprocessing.cpu_count()
  else: 
    processes = args.nb_processes
  
  # load LVIS annotations 
  lvis_annotations = objaverse.load_annotations()
  
  # load categories
  # from file 
  if args.subset_categories is not None: 
    objects_subset = load_categories_from_file(args.subset_categories, args.nb_categories)
   # randomly 
  else: 
    nb_cat = args.nb_categories
    print('Choosing {} categories from LVIS randomly...')
    # TODO 
  
  # get a dict with nb_objects per categories 

  
# --- functions
def load_categories_from_file(file_subset, nb_categories): 
  objects_subset = pd.read_csv(file_subset, delimiter delimiter=';', nrows= nb_categories)
  return objects_subset

  
# default = 'objaverse_subset.csv'
# default = '

# load 
