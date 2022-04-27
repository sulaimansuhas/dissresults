import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import ScalarFormatter, NullFormatter

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
dirct = (os.getcwd()) + "/normal-server-1-core"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in conn_list:
        if str(j) == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
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
dirct = (os.getcwd()) + "/mtcp-server-1-core"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in conn_list:
        if str(j) == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
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
    fig, ax = plt.subplots(nrows = 1,ncols = 2, constrained_layout = True)
    fig.suptitle("Connection Stats for " + str(size_list[0])+ " byte packets")
    ax[0].set_title('Latencies')
    ax[0].set_xlabel('Number of Client Connections')
    ax[0].set_ylabel('Latency in Microseconds')
    ax[0].set_xticks(conn_list)
    ax[0].plot(x,yl, '--o')
    ax[0].plot(x,yml, '--o')
    ax[0].set_ylim(bottom=0)
    if ytyp == "rps":
        ax[1].set_ylabel('Requests/Sec')
    else:
        ax[1].set_ylabel('Mb/Sec')

    ax[1].set_title('Throughput')
    ax[1].set_xlabel('Number of Client Connections')
    ax[1].set_xticks(conn_list)
    ax[1].plot(x,yt, '--o')
    ax[1].plot(x,ymt, '--o')
    ax[1].set_ylim(bottom=0)

    return fig


pdf = PdfPages(str(size_list[0]) + ' Resultsrps.pdf')
pdf.savefig(graphing("rps"))
pdf.close()
pdf = PdfPages(str(size_list[0]) + ' Resultsdata.pdf')
pdf.savefig(graphing("data"))
pdf.close()
