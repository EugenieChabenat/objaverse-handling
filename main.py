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
from modif_objects import *
from methods import * 

processes = 1 

# parse arguments 
parser = argparse.ArgumentParser(description='Objaverse Handling')

# -- files 
"""parser.add_argument('-fe', '--final_excel', default='result_files/test_excel_cat.xls', 
                   type=str, help='name and path of the file where the final excel sheet will be stored')"""

parser.add_argument('-s', '--subset_categories', default='objaverse_subset.csv', 
                    type=str, help='name of the doc where to find the categories to download from')

parser.add_argument('-d', '--dict_uid', default= 'result_files/dict_uids.txt', type=str, 
                    help='name of the file where to store the dictionary of uids')

parser.add_argument('-r', '--file_removed_uids', default=None, type=str, 
                    help='name of the file where to store the dict with removed uids')

parser.add_argument('-mf', '--modified_file', default=None, type=str, 
                    help='name of the file with uids that has been modified')

# -- numbers needed 
parser.add_argument('-nb', '--nb_objects', default=5, type=int, 
                   help='number of objects to download per category of objects')

parser.add_argument('-nc', '--nb_categories', default=10, type=int, 
                   help='number of categories of objects to download from objaverse')

parser.add_argument('-np', '--nb_processes', default=1, type=int, 
                    help='number of processes to use to download from objaverse')

# -- boolean needed 
parser.add_argument('-m', '--multiprocessing', default=False, type=bool, 
                    help='whether to use multiprocessing to download from objaverse or not')

parser.add_argument('--seed', default=None, type=int,
                    help='seed for initializing random processes')

parser.add_argument('-f', '--first', default=False, type=bool, 
                    help='first time loading the lvis annotations or not')

"""parser.add_argument('-mo', '--modifications', default=False, type=bool, 
                    help='reloading after modifying the uids')"""

parser.add_argument('-sw', '--save_worksheet', default=True, type=bool, 
                    help='save the paths to the downloaded objects in a excel worksheet')

parser.add_argument('-nw', '--name_worksheet', default='result_files/final_worksheet.xls', type=str, 
                    help='name and path of the excel worksheet')

# -- options: first, modification and redownloading 
parser.add_argument('-one', '--first_download', default=False, type=bool, 
                    help='name and path of the excel worksheet')

parser.add_argument('-it', '--iterations', default=False, type=bool, 
                    help='name and path of the excel worksheet')

def main(): 
  
  print('in main')
  args = parser.parse_args()
  
  # -- needed everytime (first or iteration) 
  if args.seed is not None: 
    print('Setting random seed..')
    random.seed(args.seed)
   
  if args.multiprocessing: 
    processes = multiprocessing.cpu_count()
  else: 
    processes = args.nb_processes
  print('Using {} processes for downloading'.format(processes))
  
  # load LVIS annotations 
  if args.first == True: 
    print('Loading LVIS annotations from objaverse..')
    lvis_annotations = objaverse.load_lvis_annotations()
    #save_dict_as_txt('lvis_annotations.txt', lvis_annotations)
  else: 
    print('Loading LVIS annotations from file..')
    lvis_annotations = get_dict_from_txt('lvis_annotations.txt')
  
  
  # ----- FIRST TIME = LOAD CATEGORIES 
  if args.first_download: 
    print('FIRST DOWNLOAD')
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
      
    print('Constructing a dictionary with UIDs')
    dict_uids = get_dict_uids(lvis_annotations, objects_subset, args.nb_objects)

    # save dict
    save_dict_as_txt(args.dict_uid, dict_uids)
    
    
    # download objects
    if args.save_worksheet: 
      print('Downloading objects and saving the paths to folder in a worksheet')
      save_to_worksheet(dict_uids, processes, args.name_worksheet)
    else: 
      print('Downloading objects')
      download_objects(dict_uids, processes)
  
  # ----- ITERATION: GET CATEGORIES FROM DICT
  
  if args.iterations: 
    print('ITERATION')
    dict_uids = get_dict_from_txt(file_path=args.modified_file)
    objects_subset = dict_uids.keys()
    
    # or 
    # reload the modified file 
    modified_uids_dict = reload_file(args.modified_file)
    # download missing objects 
    download_missing_objects(modified_uids_dict, lvis_annotations, args.file_removed_uids, processes)
    # resave dict with new uids
    print('re-saving the dictionary')
    resave_dict(modified_uids_dict)
    
    dict_uids = modified_uids_dict
    
    print('done')
  return None
  #objects_subset = load_categories_from_file('objaverse_subset.csv', args.nb_categories)
  # get a dict with nb_objects per categories 
  
  """dict_uids = get_dict_uids(lvis_annotations, objects_subset, args.nb_objects)
  # save dict
  save_dict_as_txt(args.dict_uid, dict_uids)"""
 
  """# download objects
  if args.save_worksheet: 
    print('Downloading objects and saving the paths to folder in a worksheet')
    save_to_worksheet(dict_uids, processes, args.name_worksheet)
  else: 
    print('Downloading objects')
    download_objects(dict_uids, processes)"""
  

  
  
# --- functions
"""def load_categories_from_file(file_subset, nb_categories): 
  objects_subset = pd.read_csv(file_subset, delimiter=';', nrows= nb_categories)
  return objects_subset

def get_dict_uids(lvis_annotations, objects_subset, nb_objects):
  dict_uids = {}
  for index, row in objects_subset.iterrows(): 
    if nb_objects > row[1]: 
      dict_uids[row[0]] = lvis_annotations[row[0]][:int(row[1])]
    else: 
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

def download_objects(dict_uids, processes): 
  for objects_cat, uids_ in dict_uids.items(): 
    objects = objaverse.load_objects(
        uids=uids_,
        download_processes=processes
    )
  print(objects)
  print('Objects downloaded successfully') 
  return None """

if __name__ == '__main__':
    main()

