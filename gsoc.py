def convertUnixNano(filename):
    """
    Return UTC & CERN hour of name of file.
    filename: string
    """
    from datetime import datetime as dt
    from pytz import timezone, utc
    filename = filename[:18]
    filename = int(filename)/(10)**8
    date = dt.utcfromtimestamp(filename).strftime('%Y-%m-%d %H:%M:%S:%f')
    date = dt.strptime(date, '%Y-%m-%d %H:%M:%S:%f')
    tz = timezone('CET')
    cernTime = utc.localize(date, is_dst=None).astimezone(tz)
    print("UTC time:",date)
    print("CERN time:", cernTime)

def openHdf(filename):
    import h5py
    f = h5py.File(filename, 'r')
    return f

info = []
def visitor_func(name, node):
    import h5py
    if isinstance(node, h5py.Dataset):
        size = node.size
        shape = node.shape
        try:
            typ = node.dtype
        except:
            typ = ""
        info.append([name,size,shape,typ])
    else:
        size = ""
        shape = ""
        typ = "Group"
        info.append([name,size,shape,typ])

def createCsv(lst,newFilename):
    import csv
    with open(str(newFilename) + ".csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(info)

file = "1541962108935000000_167_838.h5"

convertUnixNano(file)
openHdf(file).visititems(visitor_func)
createCsv(lst = info,newFilename = "gsoc")