from sys import argv
import frontmatter as front
from os import system

# check a file has been provided
if len(argv) == 1:
    print('Please provide the path to a file for use by panrun.')
    exit()

# get file name
output_file_name = argv[1]
print(output_file_name)

# load file and metadata
output_file = front.load(output_file_name)
YAML = output_file.metadata
try:
    panrun_params = YAML['panrun']
except:
    print('No parameters supplied for panrun')
    exit()

# build command
command = 'pandoc "' + output_file_name + '"'
for key, value in panrun_params.items():
    if value==True:
        command += ' --' + key
    else:
        command += ' --' + key + ' ' + value

# run 
system(command)

# For alternative methods, see
# https://janakiev.com/blog/python-shell-commands/

# for debugging
print(command)