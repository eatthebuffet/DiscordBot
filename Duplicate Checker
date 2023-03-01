# Program to find duplicates in the list and return list of duplicate items in Python

from itertools import groupby

duplicate_item_list = []


original_list = [ 
'',
'',
'',
''
]


for a, b in groupby(sorted(original_list)):
    if len(list(b)) > 1:
        duplicate_item_list.append(a)
print('duplicate item in a list :', duplicate_item_list)
