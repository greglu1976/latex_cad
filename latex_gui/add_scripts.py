import subprocess
import os

def rebuild(tex_dir):
    command = 'lualatex'
    arguments = ['general.tex']
    full_command = [command] + arguments
    result = subprocess.run(full_command, cwd=tex_dir, check=True)
    if result.returncode == 0:
        return 'ok'
    return ''

def tex_opener(filepath):
    os.startfile(filepath+'/general.tex')
    return 'ok'

def pdf_opener(filepath):
    os.startfile(filepath+'/general.pdf')
    return 'ok'