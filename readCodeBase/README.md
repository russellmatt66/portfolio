# Dependencies
- `pandas`

# Overview
Recursive program that scans through an entire project for files with a specified set of extensions, and counts the number of lines in each file that it finds. 

The program constructs a dictionary out of this data, and uses pandas to compile a report out of this information.

Report details the name of the file, path to it, and the line count, for each file that is found. 

# Run Instructions
- `python3 readCodeBase.py path/to/project name_of_programming_language`
- Example: `python3 readCodeBase.py ~/someproject/ C`
    - This command would produce a directory named `report-someproject/`, and a file `report_C.csv` inside detailing the line count for each file ending with `.c`, or `.h`, that 
    is inside `~/someproject/`

# Future Work
Parallelize the scanning process over the different supported file extensions, (found in 'extensions.txt'). 
