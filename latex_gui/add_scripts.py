import subprocess
import os
import sys


def rebuild(tex_dir):
    command = 'lualatex'
    arguments = ['general.tex']
    full_command = [command] + arguments
    result = subprocess.run(full_command, cwd=tex_dir, check=True)
    if result.returncode == 0:
        return 'ok'
    return ''

def tex_opener(filepath):
    if sys.platform.startswith('win'):
        os.startfile(filepath+'/general.tex')
        return 'ok'
    
    subprocess.run(['xdg-open', filepath+'/general.tex'], check=True)
    #subprocess.run(filepath+'/general.tex')
    return 'ok'


def pdf_opener(filepath):
    if sys.platform.startswith('win'):    
        os.startfile(filepath+'/general.pdf')
        return 'ok'
    subprocess.run(['xdg-open', filepath+'/general.pdf'], check=True)
    #subprocess.run(filepath+'/general.tex')
    return 'ok'
