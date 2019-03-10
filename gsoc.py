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
    """
    Return hdf read file
    filename: string
    """
    import h5py
    f = h5py.File(filename, 'r')
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
    f.visititems(visitor_func)
    return info

def createCsv(lst,newFilename):
    """
    Create CSV file from array of lists with name newFilename
    lst: list
    newFilename: str
    """
    import csv
    with open(str(newFilename) + ".csv", 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(lst)

def tsk3(filename):
    import numpy as np
    from scipy import signal
    import matplotlib.pyplot as plt
    import h5py
    f = h5py.File(filename, 'r')
    ds = np.array(f["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData"])
    height = f["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight"]
    width = f["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth"]

    ds = np.reshape(ds,(height[0],width[0]))
    filt = signal.medfilt(ds)
    plt.imshow(filt)
    plt.colorbar()
    plt.savefig("streakImageData.png")
    plt.show()
    


file = "1541962108935000000_167_838.h5"

convertUnixNano(file)
f = openHdf(file)
createCsv(lst = f,newFilename = "gsoc")
tsk3(file)