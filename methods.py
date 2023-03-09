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
  return None 
