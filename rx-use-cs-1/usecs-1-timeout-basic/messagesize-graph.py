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


size_list = [64, 256, 1024, 2048, 4096]
thread_split = [4]
norm_latency_dict = {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
norm_throughput_dict= {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
norm_data_dict= {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
dirct = (os.getcwd()) + "/normal-server-1-core"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in ["1", "25", "50", "75", "100", "125", "150"]:
        if j == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
            t = (file.readline())
            d = (file.readline())
            l = l.split()
            l = list(map(lambda a : float(a[:-2]), l))
            t = t.split()
            t = list(map(lambda a : float(a), t))
            d = d.split()
            d = list(map(check_data, d))
            norm_latency_dict[typ].append(round((sum(l)/len(l)),2))
            norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
            norm_data_dict[typ].append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+j+".txt", "r")
                typ ="t"+str(k)+"c"+j
                l = (file.readline())
                t = (file.readline())
                d = (file.readline())
                l = l.split()
                l = list(map(lambda a : float(a[:-2]), l))
                t = t.split()
                t =list(map(lambda a : float(a), t))
                d = d.split()
                d =list(map(check_data, d))
                norm_latency_dict[typ].append(round((sum(l)/len(l)),2))
                norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
                norm_data_dict[typ].append(round((sum(d)/len(d)),2))


mtcp_latency_dict = {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
mtcp_throughput_dict= {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
mtcp_data_dict= {"t1c1":[], "t4c25":[], "t4c50":[],"t4c75":[],"t4c100":[],"t4c125":[], "t4c150":[]}
dirct = (os.getcwd()) + "/mtcp-server-1-core"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in ["1", "25", "50", "75", "100", "125", "150"]:
        if j == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
            t = (file.readline())
            d = (file.readline())
            l = l.split()
            l = list(map(lambda a : float(a[:-2]), l))
            t = t.split()
            t = list(map(lambda a : float(a), t))
            d = d.split()
            d =list(map(check_data, d))
            mtcp_latency_dict[typ].append(round((sum(l)/len(l)),2))
            mtcp_throughput_dict[typ].append(round((sum(t)/len(t)),2))
            mtcp_data_dict[typ].append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+j+".txt", "r")
                typ ="t"+str(k)+"c"+j
                l = (file.readline())
                t = (file.readline())
                d = (file.readline())
                l = l.split()
                l = list(map(lambda a : float(a[:-2]), l))
                t = t.split()
                t =list(map(lambda a : float(a), t))
                d = d.split()
                d =list(map(check_data, d))
                mtcp_latency_dict[typ].append(round((sum(l)/len(l)),2))
                mtcp_throughput_dict[typ].append(round((sum(t)/len(t)),2))
                mtcp_data_dict[typ].append(round((sum(d)/len(d)),2))


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

def graphing(connset, ytyp):
    threads = connset.split("c")[0][1:]
    connections = connset.split("c")[1]
    if ytyp == "rps":
        yt= np.array(norm_throughput_dict[connset])
        ymt = np.array(mtcp_throughput_dict[connset])
    else:
        yt= np.array(norm_data_dict[connset])
        ymt = np.array(mtcp_data_dict[connset])


    yl = np.array(norm_latency_dict[connset])
    yml = np.array(mtcp_latency_dict[connset])
    x  = np.array(size_list)
    fig, ax = plt.subplots(nrows = 1,ncols = 2, constrained_layout = True)
    fig.suptitle(connections + " connections & " + threads + " threads", fontsize=16)
    ax[0].set_title('Latencies')
    ax[0].set_xlabel('Message Size in Bytes')
    ax[0].set_ylabel('Latency in Microseconds')
    ax[0].set_xscale('log', base=2)
    ax[0].set_xticks(size_list)
    ax[0].get_xaxis().get_major_formatter().labelOnlyBase = False
    ax[0].get_xaxis().set_major_formatter(ScalarFormatter())
    ax[0].get_xaxis().set_minor_formatter(NullFormatter())
    ax[0].plot(x,yl, '--o')
    ax[0].plot(x,yml, '--o')
    ax[0].set_ylim(bottom=0)
    if ytyp == "rps":
        ax[1].set_ylabel('Requests/Sec')
    else:
        ax[1].set_ylabel('Mb/Sec')

    ax[1].set_title('Throughput')
    ax[1].set_xlabel('Message Size in Bytes')
    ax[1].set_xscale('log', base=2)
    ax[1].set_xticks(size_list)
    ax[1].get_xaxis().get_major_formatter().labelOnlyBase = False
    ax[1].get_xaxis().set_major_formatter(ScalarFormatter())
    ax[1].get_xaxis().set_minor_formatter(NullFormatter())
    ax[1].plot(x,yt, '--o')
    ax[1].plot(x,ymt, '--o')
    ax[1].set_ylim(bottom=0)

    return fig


pdf = PdfPages('Resultsrps.pdf')
for i in norm_latency_dict.keys():
    pdf.savefig(graphing(i, "rps"))

pdf.close()
pdf = PdfPages('Resultsdata.pdf')
for i in norm_latency_dict.keys():
    pdf.savefig(graphing(i, "data"))

pdf.close()
