import pylab as pl
import numpy as np
import pandas as pd
import copy


def filterString(string):
    return string.rstrip().split('\t')


def filterTime(time):
    tsplit = time.split(':')
    coef = {3 : 3600., 2 : 60., 1 : 1.}
    nterms = len(tsplit)
    
    ftime = 0.0
    for item in tsplit:
        ftime += coef[nterms]*float(item)
        nterms -= 1
    
    return ftime


def ReadFluor_nanomed(filename, header = 3):
    f = open(filename, 'r')
    for j in range(3):
        f.readline()
    
    Readings = []
    Times = []
    
    while True:
        line = f.readline()
        if not line: break
        
        read = filterString( line )
        if len(read) > 1:
            Lines = []
            
            for nwell in range( 8 ):
                
                line = []
                
                if read[0] != "": Times.append( filterTime(read[0]) )
                
                for reading in read[2:]:
                    line.append( float(reading) )
                
                Lines.append(line)
                
                read = filterString( f.readline() )
            
            Readings.append( np.array( Lines ) )
            
    return np.array( Times ), Readings




def ReadFluor_timefmt_nanomed(ListOfFiles, nr_header = 2, sep = '\t'):
    """Importing a set of data, interpreted as a time series. The time is
    supposed to be encoded in the filename. GNANO fluorimeter has
    several export formats. This function reads data from 'time
    format'.
    
    Data is assumed to be separated by sep character (standard \t).
    
    list ListOfFiles :: a list with all filenames
    int nr_header    :: number of lines of the header 
    
    """

    # Storing the HEADER
    f = open(ListOfFiles[0], 'r')
    for j in range(nr_header): f.readline()
    line = f.readline()
    f.close()
    HEADERS = line.split(sep)[1:-1]
    # To ensure alphabetical order during sorting...
    for j in range(len(HEADERS)):
        if (HEADERS[j][:4] == 'Temp'): HEADERS[j] = 'T(oC)'
        if ( len(HEADERS[j]) < 3 ): HEADERS[j] = HEADERS[j][0] + "0" + HEADERS[j][1]

    TSeries = {}
    for header in HEADERS:
        TSeries[header] = []
    
    # Getting the data
    for filename in ListOfFiles[1:]:
        
        f = open(filename, 'r')
        for j in range(nr_header+1):
            f.readline()
            
        Readings = []
        Times = []
            
        while True:
            line = f.readline()
            if not line or line == '\r\n' : break

            line_usfl = line.split(sep)[1:-1]

            cnt = 0
            for item in line_usfl:
                if ( item == '' ): TSeries[HEADERS[cnt]].append( '' )
                else:              TSeries[HEADERS[cnt]].append( float(item) )
                cnt += 1
            
        # Closing the file
        f.close()

    
    # Turning it into a Pandas DataFrame object
    dictdata = {}
    for header in HEADERS:
        dictdata[header] = TSeries[header]
    
    TimeReadings = pd.DataFrame(data = dictdata)
    
    return TimeReadings





def normalizeByOD(Readings, OD):
    
    NormReadings = copy.deepcopy( Readings )
    
    for Reading in NormReadings:
        Reading = np.divide(Reading, OD)
    
    return NormReadings



def AbsorbLineReading(Times, Data, lines = np.arange(8)):
    
    ntimes = Times.shape[0]
    m = np.zeros( (lines.shape[0], ntimes) )
    
    for time in range(ntimes):
        for line in lines:
            m[line,time] = Data[time][line].mean()
    
    return m




def ODplot(Data, title=""):
    for j in range(8):
        pl.plot(Data[j,:], '-')
    
    pl.xlim(-1,9)
    pl.title(title)
    pl.xlabel('Sample id')
    pl.ylabel('OD')
    pl.show()
