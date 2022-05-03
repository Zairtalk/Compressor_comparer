#!/usr/bin/env python3

import os
import prettytable as pt
import time
import shutil as sh

folders = os.listdir('Dane_do')

dict_of_commands = {'zip':'zip -rq {0}.zip {1}',
                    'rar':'rar a {0}.rar {1} > /dev/null',
                    '7zip':'7z a  {0}.7z {1} > /dev/null',
                    'lzop':'lzop -q {1} -o {0}.lzo',
                    'zstandart':'zstd -q {0}.tar',
                    'lz4':'lz4 -qr {0}.tar',
                    'lrzip zpaq':'lrzip -zq {0}.tar',
                    'pigz':'pigz -kq {0}.tar',
                    'bzip2':'bzip2 -kq {0}.tar',
                    'lzma':'lzma -kq {0}.tar',
                    'xz':'xz -kq {0}.tar',
                    'pixz':'pixz -k {0}.tar'} #linux commands to compress files

list_of_extensions = ['.zip','.rar','.7z','.lz4','.zst','.lzo','.tpxz','.lrz','.gz','.bz2','.lzma','.xz']

'''file compressors: zip, rar, 7zip, lz4, zstandart, lzop, pigz, pixz, bzip2, lzma, lrzip, xz'''

timer = None
def timer(func): #Decorator funciton to calculate time it takes to execute another function
    def wrap(*args, **kwargs):
        global timer
        t1 = time.perf_counter()
        func(*args, **kwargs)
        t2 = time.perf_counter()
        timer = t2 - t1
        # print(f'File was compressed in {timer:.4f} sec')
    return wrap

@timer
def to_archive(command): #function that redirects commands to linux shell
    os.system(command)


def archivization(dicto,folds=('pdf','doc')): #main component of program, where everything is distributed
    created = False
    curdir = os.getcwd()
    for folder in folds:
        for compressor, command in dicto.items():
            sourcefolder = 'Dane_do/' + folder
            endfile = 'Dane_po/'
            if compressor not in ('lz4','pixz','zstandart','lrzip zpaq','pigz','bzip2','lzma','xz'):
                archive_command = command.format(endfile + folder,sourcefolder,folder)
            else:
                if not created:
                    created = True
                    os.system('tar -cf {1}.tar {0}/'.format(sourcefolder,endfile + folder))
                    os.chdir(endfile)
                archive_command = command.format(folder)
            to_archive(archive_command)
            print(round(timer,))
        os.system('rm *.tar')
        os.chdir(curdir)
        created = False
    else:
        os.chdir(curdir)

def saveData():
    pass

# def checkAndMove(sourcefolder,endfolder):
#     if os.path.exists(sourcefolder) and os.path.exists(endfolder):
#         listoffiles = getPathName(sourcefolder)
#         for i in listoffiles:
#             if i[1] in list_of_extensions:
#                 try:
#                     sh.move(i[0] + i[1], endfolder)
#                 except OSError:
#                     raise
#     else:
#         print(os.path.exists(sourcefolder),os.path.exists(endfolder))

def getPathName(directory=os.getcwd()):
    try:
        curpath = os.getcwd()
        os.chdir(directory)
        listoffiles = os.listdir(os.getcwd())
        for i,j in enumerate(listoffiles):
            listoffiles[i] = os.path.splitext(j)
    except OSError as e:
        raise e
    finally:
        os.chdir(curpath)
    return listoffiles

def getFileSize(file):
    return os.stat(file).st_size

def showFileSize(file): # Convert size to human readable
    fsize = getFileSize(file)
    if fsize > (1024 * 1024 * 1024):
        return f'{fsize/(1024**3):.4f} Gb'
    elif fsize > (1024 * 1024):
        return f'{fsize/(1024**2):.4f} Mb'
    elif fsize > (1024):
        return f'{fsize/(1024):.4f} Kb'
    else:
        return f'{fsize:.4f} b'

def change_in_size(srcfile,endfile):
    change = getFileSize(srcfile) - getFileSize(endfile)
    percentage = f'{getFileSize(endfile)/getFileSize(srcfile) * 100} %'
    return (change,percentage)

def makeTables():
    table = pt.PrettyTable()
    #table.field_names()
    #TODO make pretty table for every compressor

def main():
    archivization(dict_of_commands)
    # print(getPathName('Dane_do/pdf'))
    #TODO make proper main()

if __name__ == '__main__':
    main()
