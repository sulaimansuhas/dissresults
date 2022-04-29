import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import ScalarFormatter, NullFormatter
import seaborn as sns
sns.set()

def check_data(data):
    if data[-2:] == "GB":
        return float(data[:-2])*1000
    else:
        return float(data[:-2])
def check_latency(latency):
    print(latency)
    if latency[-2:] == "ms":
        return float(latency[:-2])*1000
    else:
        return float(latency[:-2])


conn_list = [1,25,50,75,100,125,150]
size_list = [4096]
thread_split = [4]
norm_latency_dict = [] 
norm_throughput_dict = []
norm_data_dict = []
dirct = (os.getcwd()) + "/normal"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in conn_list:
        if str(j) == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
            s = (file.readline())
            t = (file.readline())
            d = (file.readline())
            l = l.split()
            l = list(map(check_latency, l))
            t = t.split()
            t = list(map(lambda a : float(a), t))
            d = d.split()
            d = list(map(check_data, d))
            norm_latency_dict.append(round((sum(l)/len(l)),2))
            norm_throughput_dict.append(round((sum(t)/len(t)),2))
            norm_data_dict.append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+str(j)+".txt", "r")
                typ ="t"+str(k)+"c"+str(j)
                l = (file.readline())
                s = file.readline()
                t = (file.readline())
                d = (file.readline())
                l = l.split()
                l = list(map(check_latency, l))
                t = t.split()
                t =list(map(lambda a : float(a), t))
                d = d.split()
                d =list(map(check_data, d))
                norm_latency_dict.append(round((sum(l)/len(l)),2))
                norm_throughput_dict.append(round((sum(t)/len(t)),2))
                norm_data_dict.append(round((sum(d)/len(d)),2))


mtcp_latency_dict = []
mtcp_throughput_dict = []
mtcp_data_dict = []
dirct = (os.getcwd()) + "/mtcp"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in conn_list:
        if str(j) == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
            s = file.readline()
            t = (file.readline())
            d = (file.readline())
            l = l.split()
            l = list(map(check_latency, l))
            t = t.split()
            t = list(map(lambda a : float(a), t))
            d = d.split()
            d =list(map(check_data, d))
            mtcp_latency_dict.append(round((sum(l)/len(l)),2))
            mtcp_throughput_dict.append(round((sum(t)/len(t)),2))
            mtcp_data_dict.append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+str(j)+".txt", "r")
                typ ="t"+str(k)+"c"+str(j)
                l = (file.readline())
                s = file.readline()
                t = (file.readline())
                d = (file.readline())
                l = l.split()
                l = list(map(check_latency, l))
                t = t.split()
                t =list(map(lambda a : float(a), t))
                d = d.split()
                d =list(map(check_data, d))
                mtcp_latency_dict.append(round((sum(l)/len(l)),2))
                mtcp_throughput_dict.append(round((sum(t)/len(t)),2))
                mtcp_data_dict.append(round((sum(d)/len(d)),2))


print(mtcp_latency_dict)
print(mtcp_throughput_dict)
print(mtcp_data_dict)

print(norm_latency_dict)
print(norm_throughput_dict)
print(norm_data_dict)
#
#    file = open("experiment-d3s-t10-c10.txt", "r")
#l = (file.readline())
#t = (file.readline())
#l = l.split()
#t = t.split()
#print(l)
#print(t)
#

def graphing(ytyp):
    if ytyp == "rps":
        yt= np.array(norm_throughput_dict)
        ymt = np.array(mtcp_throughput_dict)
    else:
        yt= np.array(norm_data_dict)
        ymt = np.array(mtcp_data_dict)


    yl = np.array(norm_latency_dict)
    yml = np.array(mtcp_latency_dict)
    x  = np.array(conn_list)
    fig, ax = plt.subplots(nrows = 1,ncols = 1, layout="constrained")
    #fig.suptitle("Connection Stats for " + str(size_list[0])+ " byte packets")
    if ytyp == "rps":
        ax.set_ylabel('Throughput(Requests/s)')
    else:
        ax.set_ylabel('Throughput(MB/s)')

    ax.set_xlabel('Number of Client Connections')
    ax.set_xticks(conn_list)
    ax.plot(x,yt, '--o', label = "Linux Stack", color="cornflowerblue")
    ax.plot(x,ymt, '--o', label = "mTCP", color="coral")
    ax.set_ylim(bottom=0)

    plt.legend(loc="upper left")
    plt.savefig(str(size_list[0]) + "-" + ytyp+'.png')
    plt.close()


graphing("rps")
graphing("data")
