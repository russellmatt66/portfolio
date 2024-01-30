import sys 
import os
import pandas as pd 
import re

# TODO - parallelize
# import threading
# import concurrent.futures
'''
HELPER FUNCTIONS
'''
# Accepts a string representing the language to scan the code-base for
# Returns a list of the file extensions to look for
def readExtensions(prog_lang: str) -> list[str]:
    print(prog_lang)
    with open('extensions.txt', 'r') as ext_file:
        for line in ext_file:
            if line.split('=')[0] == prog_lang:
                pattern = re.compile("'.(.+?)'")
                matches = pattern.findall(line)

    return matches

# Reads a file, and returns how many lines there are 
def countLines(path_to_file: str) -> int:
    l_c = 0
    with open(path_to_file, 'r') as file:
        for line in file:
            l_c += 1
    return l_c

# Accepts a string representing the path to the codebase, an extension to scan for, and the dict in which to put the information 
# Recursive wrapper around the reading logic
def readCodeBase(root: str, ext_str: str, code_base_dict: dict) -> None:
    # Get a list of all relevant files, and sub-directories in root
    list_of_subdirs = next(os.walk(root))[1] # sub-directories
    # print(list_of_subdirs)
    list_of_files = [file for file in next(os.walk(root))[2] if (len(file.split('.')) != 1) and (file.split('.')[1] == ext_str)] # files

    for file in list_of_files:
        line_count = countLines(root + file)
        code_base_dict['file_name'].append(file)
        code_base_dict['path'].append(root) # This can be cleaned downstream
        code_base_dict['line_count'].append(line_count)

    for sub_dir in list_of_subdirs:
        readCodeBase(root + sub_dir + "/", ext_str, code_base_dict)

    return

'''
MAIN CODE
# Program flow
# ext_list = readExtensions(prog_lang)
# code_base_dict = readCodeBase(path_to_root)
# pd.DataFrame(code_base_dict) 
'''
path_to_code_base_root = sys.argv[1] # Absolute path
prog_lang = sys.argv[2] # Performing multi scan is a feature for a later day

ext_list = readExtensions(prog_lang)
print(ext_list)

codebase_dict = {}
features = ['file_name', 'path', 'line_count']
for feature in features:
    codebase_dict[feature] = []

# Recursive solution
for extension in ext_list:
    readCodeBase(path_to_code_base_root, extension, codebase_dict)

codebase_df = pd.DataFrame(codebase_dict)

# need to calculate a name for the directory in which to put the reports
num_fwdslash = 0
for c in path_to_code_base_root:
    if c == '/': num_fwdslash += 1

root_components = path_to_code_base_root.split('/')
project_name = root_components[num_fwdslash-1]
print(project_name)

report_dir = './report_' + project_name
try: 
    os.mkdir(report_dir)
    print(f"Directory '{report_dir}' created successfully.")
except FileExistsError:
    print(f"Directory '{report_dir}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

codebase_df.to_csv(report_dir + "/" + "report_" + prog_lang + '.csv')
