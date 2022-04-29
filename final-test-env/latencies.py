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
    #print(latency)
    if latency[-2:] == "ms":
        return float(latency[:-2])*1000
    else:
        return float(latency[:-2])


size_list = [64, 128,256,512, 1024, 2048, 4096]
thread_split = [4]
norm_latency_dict = {"t1c1":[], "t4c75":[], "t4c150":[]}
norm_sd_dict = {"t1c1":[], "t4c75":[], "t4c150":[]}
#norm_throughput_dict= {"t1c1":[], "t4c75":[], "t4c150":[]}
#norm_data_dict= {"t1c1":[], "t4c75":[], "t4c150":[]}
dirct = (os.getcwd()) + "/normal"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in ["1", "75", "150"]:
        if j == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            print(j + " " + typ)
            l = (file.readline())
            s = (file.readline())
            print(s)
            #t = (file.readline())
            #d = (file.readline())
            l = l.split()
            l = list(map(check_latency, l))
            s = s.split()
            s = list(map(check_latency, s))
            print(s)
      #t = t.split()
            #t = list(map(check_latency, t))
            #d = d.split()
            #d = list(map(check_data, d))
            norm_latency_dict[typ].append(round((sum(l)/len(l)),2))
            norm_sd_dict[typ].append(round((sum(s)/len(s)),2))
            #norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
            #norm_data_dict[typ].append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+j+".txt", "r")
                typ ="t"+str(k)+"c"+j
                l = (file.readline())
                s = (file.readline())
                #t = (file.readline())
                #d = (file.readline())
                l = l.split()
                l = list(map(check_latency, l))
                s = s.split()
                s = list(map(check_latency, s))
                #print(s)
                #t = t.split()
                #t = list(map(check_latency, t))
                #d = d.split()
                #d = list(map(check_data, d))
                norm_latency_dict[typ].append(round((sum(l)/len(l)),2))
                norm_sd_dict[typ].append(round((sum(s)/len(s)),2))
                #norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
                #norm_data_dict[typ].append(round((sum(d)/len(d)),2))
                
mtcp_latency_dict = {"t1c1":[], "t4c75":[], "t4c150":[]}
mtcp_sd_dict = {"t1c1":[], "t4c75":[], "t4c150":[]}
#norm_throughput_dict= {"t1c1":[], "t4c75":[], "t4c150":[]}
#norm_data_dict= {"t1c1":[], "t4c75":[], "t4c150":[]}
dirct = (os.getcwd()) + "/mtcp"
for i in size_list:
    folder = str(i) + "bytes-test"
    f = "experiment-d3s"
    for j in ["1", "75", "150"]:
        if j == "1":
            file = open(dirct+"/"+folder+"/"+f+"-t1-c1.txt", "r")
            typ ="t1c1"
            l = (file.readline())
            s = (file.readline())
            #t = (file.readline())
            #d = (file.readline())
            l = l.split()
            l = list(map(check_latency, l))
            s = s.split()
            s = list(map(check_latency, s))
            #t = t.split()
            #t = list(map(check_latency, t))
            #d = d.split()
            #d = list(map(check_data, d))
            mtcp_latency_dict[typ].append(round((sum(l)/len(l)),2))
            mtcp_sd_dict[typ].append(round((sum(s)/len(s)),2))
            #norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
            #norm_data_dict[typ].append(round((sum(d)/len(d)),2))
        else:
            for k in thread_split:
                file = open(dirct+"/"+folder+"/"+f+"-t"+ str(k)+"-c"+j+".txt", "r")
                typ ="t"+str(k)+"c"+j
                l = (file.readline())
                s = (file.readline())
                #t = (file.readline())
                #d = (file.readline())
                l = l.split()
                l = list(map(check_latency, l))
                s = s.split()
                s = list(map(check_latency, s))
                #t = t.split()
                #t = list(map(check_latency, t))
                #d = d.split()
                #d = list(map(check_data, d))
                mtcp_latency_dict[typ].append(round((sum(l)/len(l)),2))
                mtcp_sd_dict[typ].append(round((sum(s)/len(s)),2))
                #norm_throughput_dict[typ].append(round((sum(t)/len(t)),2))
                #norm_data_dict[typ].append(round((sum(d)/len(d)),2))
                
                
print(mtcp_latency_dict)
print(mtcp_sd_dict)

print(norm_latency_dict)
print(norm_sd_dict)

def graphing(connset):
    threads = connset.split("c")[0][1:]
    connections = connset.split("c")[1]
    yl = np.array(norm_latency_dict[connset])
    print(yl)
    ys = np.array(norm_sd_dict[connset])
    print(ys)
    yu = yl + ys
    yd = yl - ys
    print(yu)
    print(yd)
    yml = np.array(mtcp_latency_dict[connset])
    yms = np.array(mtcp_sd_dict[connset])
    ymu = yml + yms
    ymd = yml - yms
    x  = np.array(size_list)
    fig, ax = plt.subplots(nrows = 1,ncols = 1, constrained_layout = True)
    #fig.suptitle(connections + " connections & " + threads + " threads", fontsize=16)
    ax.set_xlabel('Message Size (Bytes)')
    ax.set_ylabel('Latency (μs)')
    ax.set_xscale('log', base=2)
    ax.set_xticks(size_list)
    ax.get_xaxis().get_major_formatter().labelOnlyBase = False
    ax.get_xaxis().set_major_formatter(ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(NullFormatter())
    ax.plot(x,yl, '--o', label="Linux Stack", color="cornflowerblue")
    ax.fill_between(x,yu,yd,color='cornflowerblue', alpha=0.2)
    ax.plot(x,yml, '--o',label="mTCP", color="coral")
    ax.fill_between(x,ymu,ymd,color='coral', alpha=0.2)
    #ax.plot(x,yu, '--v', label="+sd")
    #ax.plot(x,yd, '--^', label="-sd")
    if connections == "1":
        ax.set_ylim([0,100])
    elif connections == "75":
        ax.set_ylim([0,500])
    else:
        ax.set_ylim([0,1000])
        
    plt.legend(loc="upper left")
    plt.savefig(connset+'-latencies.png')
    plt.close()
    

    
for i in norm_latency_dict.keys():
    graphing(i)
    






