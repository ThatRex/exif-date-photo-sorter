# Imports.
from datetime import datetime
import os
from os import listdir, rename
from os.path import isfile, join
from PIL import Image
from PIL.ExifTags import TAGS
import shutil

# Variables.
folder_unsorted_dir = 'Samples'
folder_sorted_dir = 'Sorted'
look_for_ext = ['.jpg']

print(f'Sorting Photos\n\nUnsorted Folder: {folder_unsorted_dir}\nOutput Folder: {folder_sorted_dir}\nIncluded Extension(s): {look_for_ext}\n\n')

# Image Index.
image_index_1 = []

# Builds image_index_1.
for path, subdirs, files in os.walk(folder_unsorted_dir):
    for name in files:
        for ext in look_for_ext:
            ext = ext.lower()
            if name.lower().endswith(ext):
                current_path = join(path, name)
                for tag, value in Image.open(current_path)._getexif().items():
                    if tag == 36867: 
                        date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        image_index_1.append([current_path, date, ext, None])

# Sorts image_index_1.
image_index_1.sort(key=lambda lst: lst[1].strftime('%Y:%m:%d %H:%M:%S'), reverse=True)

# Updates Names.
count = None
for img_details in image_index_1:
    print(img_details)
    name_date = img_details[1].strftime('%Y%m%d')
    count = 0
    for im_de in image_index_1:
        if not im_de[3]:
            if img_details[1].strftime('%Y%m%d') == im_de[1].strftime('%Y%m%d'): count += 1
    count = f'_{count}' if count else ''
    new_name = f'IMG_{name_date}{count}{img_details[2]}'
    img_details[3] = new_name

# Copies and renames images. 
count = 1
for img_details in image_index_1:
    original_path = img_details[0]
    new_path = join(folder_sorted_dir, img_details[3])
    try:
        shutil.copy(original_path, new_path)
        status = f'Copied\nOriginal: {original_path}\nTaken Date: {img_details[1]}\nNew: {new_path}\n'
    except Exception as error:
         status = f'Failed\nError: {error}'
    print(f'Image: {count} | Status: {status}\n')
    count += 1

print('\nDone')