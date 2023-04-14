import objaverse 
import json
import pandas as pd 
import multiprocessing 

import argparse
import os
import warnings
import time 

processes = 1

parser = argparse.ArgumentParser(description='get metadata')

parser.add_argument('uid', type=str, help='uid of the model you want the metadata for')
parser.add_argument('-c', '--category', default=None, type=str, help='LVIS category the object belongs to')

def main(): 
  args = parser.parse_args()
  
  uids = objaverse.load_uids()
  
  # loading annotations 
  print('Loading annotations from objaverse...')
  annotations = objaverse.load_annotations([args.uid])
  
  # pretty print
  for uid, content in annotations.items(): 
    print('uid: ', uid)
    
    for key, data in content.items(): 
      print(key, ': \n')
      print(data)
    
      print('')
    
  
  # save in file 


    
main()
