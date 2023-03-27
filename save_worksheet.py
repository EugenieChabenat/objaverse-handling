import xlwt
from xlwt import Workbook

import xlrd
from xlrd import open_workbook 
from xlutils.copy import copy

import objaverse

style = xlwt.easyxf('font: bold 1')

before = len('/Users/chabenateugenie/.objaverse/hf-objaverse-v1/glbs/')
after = len('4c19ae47dbe8468285ee53ff487fe51a')

def save_to_worksheet(dict_uids, processes, name_worksheet='objects_folder.xls'): 
  wb = Workbook()

  # add a sheet 
  for objects_cat, uids_ in dict_uids.items(): 
    sheet = wb.add_sheet(objects_cat)

    # name the columns
    sheet.write(0, 0, 'UID', style)
    sheet.write(0, 1, 'FOLDER NAME', style)

    objects = objaverse.load_objects(
              uids=uids_,
              download_processes=processes, 
          )
    
    i = 1 
    for id_, loc in objects.items():
      name_ = loc[before:]
      sheet.write(i, 0, id_)
      sheet.write(i, 1, name_[:7])
      i += 1
      
  wb.save('result_files/objects_folder.xls')
  print('worksheet saved')
  return None 

def modify_worksheet(path_worksheet, object_cat, objects, nb_removed):
  rb = open_workbook(path_worksheet)
  wb = copy(rb)
  writable_sheet = wb.get_sheet(object_cat)
  
  i = 11 + nb_removed
  for id_, loc in objects.items():
      name_ = loc[before:]
      writable_sheet.write(i, 0, id_, , style)
      writable_sheet.write(i, 1, name_[:7], , style)
      i += 1
  
  wb.save('result_files/new_objects_folder.xls')
  print('worksheet saved')
  return None 


