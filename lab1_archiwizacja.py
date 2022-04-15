#!/usr/bin/env python3

import os
import prettytable as pt
import time
import shutil as sh

folders = ('doc','doc_obrazki','exe','filmy','grafika','muzyka','pdf','pliki_branzowe','txt','xls') #folders in which will be files

dict_of_commands = {'zip':'zip -q {0}.zip {1}',
                    'rar':'rar a {0}.rar {1} > /dev/null',
                    '7zip':'7z a  {0}.7z {1} > /dev/null',
                    'lz3':'lz4 -q {1} {0}.lz4',
                    'zstandart':'zstd -q {1} -o {0}.zst',
                    'lzop':'lzop -q {1} -o {0}.lzo',
                    'pixz':'pixz -k {1} {0}.pxz',
                    'lrzip zpaq':'lrzip -zq {1}',
                    'pigz':'pigz -kq {1}',
                    'bzip2':'bzip2 -kq {1}',
                    'lzma':'lzma -kq {1}',
                    'xz':'xz -kq {1}'} #linux commands to compress files

'''file compressors: zip, rar, 7zip, lz4, zstandart, lzop, pigz, pixz, bzip2, lzma, lrzip, xz'''

def timer(func): #Decorator funciton to calculate time it takes to execute another function
    def wrap(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(f'File was compressed in {(t2-t1):.6f}s')
    return wrap

@timer
def to_archive(command): #function that redirects commands to linux shell
    os.system(command)


def archivization(dicto,folds=('pdf',)): #main component of program, where everything is distributed
    for compressor, command in dicto.items():
        for folder in folds:
            sourcefolder = 'Dane_do/' + folder + '/*'
            endfile = 'Dane_po/' + folder
            archive_command = command.format(endfile,sourcefolder)
            print(archive_command)
           # to_archive(archive_command)
           # checkAndMove(sourcefolder,endfile)
           #TODO reconstruct this function and make it work

# def checkAndMove(sourcefolder,endfolder):
#    os.path.exists()
#    sh.copytree()
#    sh.copy2(sourcefolder + '*',endfolder)



    #TODO Checking is files exist and if they do moving them to the proper folder

def getListofFiles(directory=os.getcwd()):
    return os.listdir(directory)

def getPathName(directory=os.getcwd()):
    try:
        curpath = os.getcwd()
        os.chdir(directory)
        listoffiles = getListofFiles(directory)
        for i,j in enumerate(listoffiles):
            listoffiles[i] = os.path.abspath(j)
    except OSError as e:
        raise
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
    #archivization(dict_of_commands)
    print(getPathName('/lost+found/'))
    #TODO make proper main()

if __name__ == '__main__':
    main()
