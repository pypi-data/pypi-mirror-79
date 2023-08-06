import psutil
import os
import datetime
import numpy as np
import time

def nb_report():
    '''
    Print a full report of the usage of notebooks on atlas-248

    This list is ordered in decreasing order of RAM usage
    '''
    os.system('ps aux | grep ipykernel_launcher > .TMP')

    pid_list = []
    with open('.TMP', 'r') as f:
        lines = f.readlines()
        for line in lines:
            words = line.split()
            pid_list.append(words[1])
    user_list = []
    etime_list = []
    time_list = []
    mem_list = []
    cpu_list = []
    for pid in pid_list:
        try:
            P = psutil.Process(pid=int(pid))
        except:
            continue
        user_list.append(P.username())
        elapsed_time = datetime.timedelta(seconds=time.time()-P.create_time())
        etime_list.append(str(elapsed_time))
        user_time = datetime.timedelta(seconds=P.cpu_times()[0])
        time_list.append(str(user_time))
        mem_list.append(P.memory_info()[1])
        cpu_list.append(P.cpu_percent())
    indexes = np.argsort(mem_list)[::-1]

    for ii in indexes:
        print('- {}\t pid: {},\tmem [GB]: {:.3f},\tcpu [%]: {},\telapsed wallclock time: {},\telapsed cpu time: {}'.format(user_list[ii], pid_list[ii],
                                                                                                                        mem_list[ii] / 1024**3, cpu_list[ii],
                                                                                                                        etime_list[ii], time_list[ii]))
    os.system('rm -f .TMP')