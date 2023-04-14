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
parser.add_argument('-f', '--file_name', default=None, type=str, help='file to store the metadata')
parser.add_argument('-s', '--save', default=True, type=bool, help='whether to store the metadata to a file or not')


def main(): 
  args = parser.parse_args()
  
  uids = objaverse.load_uids()
  
  # loading annotations 
  print('Loading annotations from objaverse...')
  annotations = objaverse.load_annotations([args.uid])
  
  if args.save:
    if args.filename is None: 
      args.file_name = f'metadata{args.uid}.txt'
    with open(args.file_name, 'w') as f: 
      for line in line: 
        f.write(line)
        f.write('\n')
  
    # pretty print
    for uid, content in annotations.items(): 
      print('uid: ', uid)
      f.write(uid)
    
      for key, data in content.items(): 
        print(key, ': ')
        print(data)
        f.write(key + ': ')
        f.write(data)
      
    
  
  # save in file 


    
main()
