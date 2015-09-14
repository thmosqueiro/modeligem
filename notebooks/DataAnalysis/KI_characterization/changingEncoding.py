import glob
import numpy as np

# I was having problems with char encoding, so...
import chardet
rawdata=open("KI fluo 1.txt","r").read()
print "Encoding detection: ", chardet.detect(rawdata)
enc = chardet.detect(rawdata)['encoding']

FLlist = []
ODlist = []
tidx   = []
for file in glob.glob("KI fluo*.txt"):
    tidx.append( float( file.split(' ')[2].split('.')[0] ) )
    FLlist.append(file)
    ODlist.append('KI OD '+file.split(' ')[2].split('.')[0]+'.txt')

Idx = np.argsort(tidx)
FLlist = np.array(FLlist)[Idx]
ODlist = np.array(ODlist)[Idx]

# Do we have the list of files sorted properly?
for filename in FLlist:
    print filename
    
    rawdata=open(filename,"r").read()
    fnamenew = 'REKI fluo ' + filename.split(' ')[2].split('.')[0] + '.txt'
    f=open(fnamenew, 'w')
    strconverted = (""+rawdata.decode(enc)).encode('utf8')
    print strconverted
    f.write(strconverted)
    f.close()


# Do we have the list of files sorted properly?
for filename in ODlist:
    print filename
    
    rawdata=open(filename,"r").read()
    fnamenew = 'REKI OD ' + filename.split(' ')[2].split('.')[0] + '.txt'
    f=open(fnamenew, 'w')
    strconverted = (""+rawdata.decode(enc)).encode('utf8')
    print strconverted
    f.write(strconverted)
    f.close()
