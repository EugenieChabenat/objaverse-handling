import json
import random
import objaverse
from save_worksheet import *

# reload the json file after potential manual modification
def reload_file(file_dict_uids): 
  with open(file_dict_uids, 'r') as fp: 
      new_uids_dict = json.load(fp)
  return new_uids_dict

def download_missing_objects(new_uids_dict, lvis_annotations, file_removed_uids, processes, path_worksheet): 
  #file_removed_uids = 'removed_uids_test.txt'
  file_removed_uids = 'removed_uids_new.txt'
  with open(file_removed_uids, 'r') as fp: 
      removed_uids = json.load(fp)
  
  print('removed uids: \n', removed_uids)
  print('\nnew uids dict: \n', new_uids_dict)
  
  
  # re-download missing objects 
  for objects_cat, uids_ in new_uids_dict.items():
    print(objects_cat)
    
    print('removed: ', removed_uids[objects_cat]) 
    print('lvis: ', lvis_annotations[objects_cat])
    if removed_uids[objects_cat] and len(lvis_annotations[objects_cat])>10:
      print('yes')
      # nb of objects to replace
      
      nb_to_download = len(removed_uids[objects_cat])
        
      # get their ids 
      ids = []
      new_uids = []

      while(len(ids)!=nb_to_download): 
          for elm in range(nb_to_download): 
              tmp_id = random.randint(0, len(lvis_annotations[objects_cat]) - 1)
              annot = lvis_annotations[objects_cat][tmp_id]
              if annot not in removed_uids[objects_cat] and annot not in new_uids_dict[objects_cat]: 
                  ids.append(annot)
                  new_uids_dict[objects_cat].append(annot)

      # load objects 
      objects = objaverse.load_objects(
          uids=ids,
          download_processes=processes
      )
      # modify worksheet 
      modify_worksheet('result_files/objects_folder.xls', objects_cat, objects, nb_removed=len(removed_uids[objects_cat]))
    else: 
        print('no')
        
  print(objects)
  return None

def resave_dict(new_uids_dict): 
  # revsave the new dict 
  with open('result_test.txt', 'w') as fp: 
      json.dump(new_uids_dict, fp)
  print('Dictionary saved to json successfully')
  return None 
