import glob
import numpy as np

# I was having problems with char encoding, so...
import chardet
rawdata=open("K8 fluo 1.txt","r").read()
print "Encoding detection: ", chardet.detect(rawdata)
enc = chardet.detect(rawdata)['encoding']

FLlist = []
ODlist = []
tidx   = []
for file in glob.glob("K8 fluo*.txt"):
    tidx.append( float( file.split(' ')[2].split('.')[0] ) )
    FLlist.append(file)
    ODlist.append('K8 OD '+file.split(' ')[2].split('.')[0]+'.txt')

Idx = np.argsort(tidx)
FLlist = np.array(FLlist)[Idx]
ODlist = np.array(ODlist)[Idx]

# Do we have the list of files sorted properly?
for filename in FLlist:
    print filename
    
    rawdata=open(filename,"r").read()
    fnamenew = 'REK8 fluo ' + filename.split(' ')[2].split('.')[0] + '.txt'
    f=open(fnamenew, 'w')
    strconverted = (""+rawdata.decode(enc)).encode('utf8')
    print strconverted
    f.write(strconverted)
    f.close()


for filename in ODlist:
    print filename
    
    rawdata=open(filename,"r").read()
    fnamenew = 'REK8 OD ' + filename.split(' ')[2].split('.')[0] + '.txt'
    f=open(fnamenew, 'w')
    strconverted = (""+rawdata.decode(enc)).encode('utf8')
    print strconverted
    f.write(strconverted)
    f.close()
