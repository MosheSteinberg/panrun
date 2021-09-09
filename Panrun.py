from sys import argv
import frontmatter as front
from os import system, environ
import re
import subprocess



def get_pandoc_opts():
    '''
    Function to get all pandoc options
    '''
    # create process
    proc = subprocess.Popen(['pandoc','--bash-completion'], stdout=subprocess.PIPE)
    # read from process
    lines_from_stdout = proc.stdout.readlines()
    # find line with 'opts' on it
    opts_line = [line.decode('UTF-8') for line in lines_from_stdout if line.decode('UTF-8').find('opts=')!=-1][0]
    # get info between quotation marks
    first_qmark = opts_line.find('"')
    second_qmark = opts_line.find('"', first_qmark+1)
    opts_withdash = opts_line[first_qmark+1:second_qmark].split(' ')
    # Return options without dashes and cutting out single letter options 
    # (as they have a full named alternative)
    return [option[2:] for option in opts_withdash if len(option)>2]


if __name__ == '__main__':

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


    # check pandoc on path
    if not re.search('pandoc', environ['PATH'], re.IGNORECASE):
        print('Pandoc is not on the path environment variable')
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
    # Can this be used to work out the list of options?

    # for debugging
    print(command)