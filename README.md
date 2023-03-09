# objaverse-handling
Code for handling Objaverse: 
- downloading from categories
- creating a subset of 3D images 
- keeping track of ids and metadata

## Usage 
1. Git fork the repo
2. Create a python/conda environment with python>=3.7 (I personally use 3.9) and activate it. 
3. Inside the project root directory, pip install the packafe locally with the commmand: 
```
pip install -r requirements.txt
```
4. The file ```config.ini``` shows the paths used by default. Change any of these variables as necessary. 

#### When downloading objects for the first time 
please specify: 
- the csv file from which to get the names of the categories 
- the number of categories to download 
- the number of objects for each categories 
- the file where to store the dictionary of uids 
- the name of the worksheet 


#### When downloading missing objects 
please specify: 
- the file with the dictionary of uids (modified)
- the file with the removed uids 
- the file where to store the new dict (or always overwrite?)
- the worksheet where to store updated files

