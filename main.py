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

from save_worksheet import save_to_worksheet

processes = 1 

# parse arguments 
parser = argparse.ArgumentParser(description='Objaverse Handling')

parser.add_argument('-fe', '--final_excel', default='result_files/test_excel_cat.xls', 
                   type=str, help='name and path of the file where the final excel sheet will be stored')

parser.add_argument('-s', '--subset_categories', default='objaverse_subset.csv', 
                    type=str, help='name of the doc where to find the categories to download from')

parser.add_argument('-d', '--dict_uid', default= 'result_files/dict_uids.txt', type=str, 
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

parser.add_argument('-f', '--first', default=False, type=bool, 
                    help='first time loading the lvis annotations or not')
def main(): 
  
  print('in main')
  args = parser.parse_args()
  
  if args.seed is not None: 
    print('Setting random seed..')
    random.seed(args.seed)
   
  if args.multiprocessing: 
    processes = multiprocessing.cpu_count()
  else: 
    processes = args.nb_processes
  print('Using {} processes for downloading'.format(processes))
  
  # load LVIS annotations 
  """if args.first == True: 
    print('Loading LVIS annotations from objaverse..')
    lvis_annotations = objaverse.load_annotations()
    save_dict_as_txt('lvis_annotations.txt', lvis_annotations)
  else: 
    print('Loading LVIS annotations from file..')
    lvis_annotations = get_dict_from_txt('lvis_annotations.txt')"""
      
  
  # load categories
  # from file 
  objects_subset = []
  if args.subset_categories is not None: 
    print('Loading categories from file')
    objects_subset = load_categories_from_file(args.subset_categories, args.nb_categories)
   # randomly 
  else: 
    print('Choosing {} categories from LVIS randomly...')
    nb_cat = args.nb_categories
    objects_subset = []
    # TODO 
  
  print('objects_subset: \n', objects_subset) 
  
  #objects_subset = load_categories_from_file('objaverse_subset.csv', args.nb_categories)
  # get a dict with nb_objects per categories 
  print('Constructing a dictionary with UIDs')
  dict_uids = get_dict_uids(lvis_annotations, objects_subset, args.nb_objects)
  
  print('dict_uids: \n', dict_uids)
  
  # save dict
  save_dict_as_txt(args.dict_uid, dict_uids)
  
  # download objects
  download_objects(dict_uids)
  
  
# --- functions
def load_categories_from_file(file_subset, nb_categories): 
  objects_subset = pd.read_csv(file_subset, delimiter=';', nrows= nb_categories)
  return objects_subset

def get_dict_uids(lvis_annotations, objects_subset, nb_objects):
  dict_uids = {}
  for index, row in objects_subset.iterrows(): 
    if nb_objects > row[1]: 
      dict_uids[row[0]] = lvis_annotations[row[0]][:int(row[1])]
    else: 
      print(dict_uids[row[0]])
      print(lvis_annotations[row[0]])
      dict_uids[row[0]] = lvis_annotations[row[0]][:nb_objects]
  return dict_uids

def save_dict_as_txt(file_path, dict_uids): 
  with open(file_path, 'w') as fp: 
    json.dump(dict_uids, fp)
  print('Dictionary saved to txt sucessfully')
  return None 

def get_dict_from_txt(file_path): 
  with open(file_path, 'r') as fp: 
    load_dict = json.load(fp)
  return load_dict

def download_objects(dict_uids): 
  for objects_cat, uids_ in dict_uids.items(): 
    objects = objaverse.load_objects(
        uids=uids_,
        download_processes=processes
    )
    print('Objects downloaded successfully') 
    return None 

if __name__ == '__main__':
    main()

