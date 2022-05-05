import json,os,pprint

information = ('Time spent','Output size','Size difference')

folders = os.listdir('Dane_do')

compressors = ('zip','rar','7zip','zstandart','lz4','lrzip zpaq','pigz','bzip2','lzma','xz')

with open('info_dict.json','w') as f:
    dictionary_info = {x:{y:{z:None for z in compressors} for y in folders} for x in information}
    json.dump(dictionary_info,f)
