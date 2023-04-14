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
  print('keys: ',annotations)
  for key, value in annotations.items(): 
    print('key: ', key)
    print('value', value)
    
    print('')
    
  
  # save in file 


    
main()
