import xlwt
from xlwt import Workbook

style = xlwt.easyxf('font: bold 1')

before = len('/Users/chabenateugenie/.objaverse/hf-objaverse-v1/glbs/')
after = len('4c19ae47dbe8468285ee53ff487fe51a')

def save_to_worksheet(dict_uids, processes): 
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

  wb.save('test_excel_cat.xls')
  return None 
