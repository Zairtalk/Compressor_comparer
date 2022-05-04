#!/usr/bin/env python3

import os
import prettytable as pt
import time
import shutil as sh
from stat import S_ISDIR
import json

with open('info_dict.json','r') as f:
    information = json.load(f)

folders = os.listdir('Dane_do')

dict_of_commands = {'zip (.zip)':'zip -rq {0}.zip {1}',
                    'rar (.rar)':'rar a {0}.rar {1} > /dev/null',
                    '7zip (.7z)':'7z a  {0}.7z {1} > /dev/null',
                    'zstandart (.zst)':'zstd -q {0}.tar',
                    'lz4 (.lz4)':'lz4 -qr {0}.tar',
                    'lrzip zpaq (.lrz)':'lrz -zk {0}.tar',
                    'pigz (.gz)':'pigz -kq {0}.tar',
                    'bzip2 (.bz2)':'bzip2 -kq {0}.tar',
                    'lzma (.lzma)':'lzma -kq {0}.tar',
                    'xz (.xz)':'xz -kq {0}.tar'}

'''file compressors: zip, rar, 7zip, lz4, zstandart, pigz, bzip2, lzma, lrzip, xz'''

timers = None
def timer(func): #Decorator funciton to calculate time it takes to execute another function
    def wrap(*args, **kwargs):
        global timers
        t1 = time.perf_counter()
        func(*args, **kwargs)
        t2 = time.perf_counter()
        timers = t2 - t1
        # print(f'File was compressed in {timer:.4f} sec')
    return wrap

@timer
def to_archive(command): #function that redirects commands to linux shell
    os.system(command)


def archivization(dicto,folds=folders): #main component of program, where everything is distributed
    created = False
    curdir = os.getcwd()
    for folder in folds:
        for compressor, command in dicto.items():
            sourcefolder = 'Dane_do/' + folder
            endfile = 'Dane_po/'
            if compressor not in ('lz4 (.lz4)','pixz (.pixz)','zstandart (.zst)','lrzip zpaq (.lrz)',\
                                  'pigz (.gz)','bzip2 (.bz2)','lzma (.lzma)','xz (.xz)'):
                archive_command = command.format(endfile + folder,sourcefolder,folder)
                to_archive(archive_command)
                index = compressor.index('.')
                saveData(compr=compressor[:index-2],filetype=folder,time=round(timers,4),\
                         size=showSize(endfile + folder + compressor[index:-1]),\
                        difference=changeInSize(sourcefolder,endfile + folder + compressor[index:-1]))
            else:
                if not created:
                    created = True
                    os.system('tar -cf {1}.tar {0}/'.format(sourcefolder,endfile + folder))
                    os.chdir(endfile)
                archive_command = command.format(folder)
                to_archive(archive_command)
                index = compressor.index('.')
                saveData(compr=compressor[:index-2],filetype=folder,time=round(timers,4),\
                         size=showSize(folder + '.tar' + compressor[index:-1]),\
                        difference=changeInSize('../' + sourcefolder,folder + '.tar' + compressor[index:-1]))
        created = False
        os.chdir(curdir)
    else:
        os.chdir(endfile)
        os.system('rm *.tar')
        os.chdir(curdir)

def saveData(compr,filetype,size=None,time=None,difference=None):
    global information
    if time:
        information['Time spent'][filetype][compr] = time
        time = None
    if size:
        information['Output size'][filetype][compr] = size
        size = None
    if difference:
        information['Size difference'][filetype][compr] = difference
        difference = None

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

def getSize(path):
    size = 0
    if not S_ISDIR(os.lstat(path).st_mode):
        return os.stat(path).st_size
    else:
        for i,ele in enumerate(os.walk(path)):
            if ele[2] is None:
                continue
            for j in ele[2]:
                file = ele[0] + '/' + j
                size += os.stat(file).st_size
        return size

def showSize(file): # Convert size to human readable
    if isinstance(file,str):
        fsize = getSize(file)
    elif isinstance(file,int):
        fsize = file
    if abs(fsize) > (1024 * 1024 * 1024):
        return f'{fsize/(1024**3):.4f} Gb'
    elif abs(fsize) > (1024 * 1024):
        return f'{fsize/(1024**2):.4f} Mb'
    elif abs(fsize) > (1024):
        return f'{fsize/(1024):.4f} Kb'
    else:
        return f'{fsize:.4f} b'

def changeInSize(srcfile,endfile):
    change = getSize(srcfile) - getSize(endfile)
    if change > 100:
        percentage = f'+{(getSize(endfile)/getSize(srcfile) * 100) - 100:.2f} %'
    elif change < 100:
        percentage = f'-{100 - (getSize(endfile)/getSize(srcfile) * 100):.2f} %'
    else:
        percentage = 'No difference'
    return (showSize(change),percentage)

def makeTables():
    table_size = pt.PrettyTable()
    table_time = pt.PrettyTable()
    table_diff = pt.PrettyTable()
    for i in information.keys():
        if i == 'Output size':
            table_size.add_column('Compressor',list(x for x in information['Output size']['doc'].keys()),align='l')
            for j in information[i]:
                table_size.add_column(j,list(x for x in information['Output size'][j].values()),align='l')
        elif i == 'Size difference':
            table_diff.add_column('Compressor',list(x for x in information['Size difference']['doc'].keys()),align='l')
            for j in information[i]:
                table_diff.add_column(j,list(str(x[0]) + ' / ' + str(x[1]) for x in information['Size difference'][j].values()),align='l')
        elif i == 'Time spent':
            table_time.add_column('Compressor',list(x for x in information['Time spent']['doc'].keys()),align='l')
            for j in information[i]:
                table_time.add_column(j,list(str(x) + ' sec' for x in information['Time spent'][j].values()),align='l')
        else:
            raise ValueError
    print('Size after comprssion'.center(50,'-'))
    print(table_size)
    print('Time of compression'.center(50,'-'))
    print(table_time)
    print('Difference in size'.center(50,'-'))
    print(table_diff)

def main():
    archivization(dict_of_commands)
    pprint(information)
    makeTables()

if __name__ == '__main__':
    main()
