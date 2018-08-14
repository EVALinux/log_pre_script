import os
import tarfile
import time
from os import getcwd , listdir
from os.path import join , isfile , isdir

def read_file(file,filter_dic):
    i = 1
    out_str, buffer = '', None
    with open(file, "r", encoding='UTF-8', errors="ignore") as f:
        for line in f:
            for filter_log in filter_dic:
                if filter_log in line:
                    if switch[filter_log](filter_dic[filter_log],line):
                        buffer = line
                        pass
                pass
            i += 1
            if buffer is not None:
                str = '%s...%s...%s...%s' % (file, ' line:', i, buffer)
                # write_result('report_pre.txt',str)
                out_str += str
                buffer = None
    return out_str

def write_result(file_name,buffer):
    with open(join(getcwd(),file_name),'a') as fo:
        fo.writelines(buffer)
    pass

# Get a list of all files that meet the 'condition' condition in this path
def get_all_log(condition):
    effective = []
    file_list = []
    file_list += open_dir(getcwd())
    for file in file_list:
        for str in condition:
            if str in file:
                effective.append(file)
    return effective

def open_dir(path):
    list_file = []
    if isfile(path):
        list_file.append(path)
    else:
        objlist = listdir(path)
        for f in objlist:
            path_now = join(path, f)
            if isfile(path_now):
                list_file.append(path_now)
            elif isdir(path_now):
                list_file += open_dir(path_now)
    return list_file

def do_check(file_name_condition, filter_dic):
    str = ''
    file_list = get_all_log(file_name_condition)
    #print ("file_list" + str(file_list))
    unzip_file(file_list)
    file_list = get_all_log(file_name_condition)
    for f in file_list:
        str += read_file(f,filter_dic)
    return str

def unzip_file(file_list):
    zip_file_list = []
    for file in file_list:
        if (".tar.gz" in file):
            #print("tgz file:" + file)
            tar = tarfile.open(file, "r:gz")
            dirs = file[:-7]
            print(dirs)
            tar.extractall(path = dirs)
            tar.close
            pass
        pass
    #Delete files that have been extracted
    # time.sleep(10)
    # for file_name in file_list:
    #     if (".tar.gz" in file_name):
    #         os.remove(file_name)
    #         pass
    #     pass
    #print(zip_file_list)
    pass

#check test result function +++

# if return true , print it
switch = {
    '***mStatus.pLevel:':lambda condition,line:int(line.split(': ')[2].strip().strip('%')) < int(condition),
    '**mStatus.pLevel:':lambda condition,line:int(line.split(': ')[2].strip().strip('%')) > int(condition),
    'tpOpenShort(): rt:':lambda condition,line:not(condition in line),
    'ADB_SERVICES:' :lambda condition,line: condition in line,
    'interceptKeyBeforeQueueing' :lambda condition,line: condition in line,
    'DefaultItemActivity' :lambda condition,line: condition in line,
    'AndroidRuntime' :lambda condition,line: condition in line,
    'RunInTestII_activity:' :lambda condition,line: condition in line,
    'isScreenOn:':lambda condition,line:not(condition in line),
    'java.lang.RuntimeException:':lambda condition,line: condition in line,
    'ShutdownThread:':lambda condition,line: condition in line,
    'BatteryService':lambda condition,line: condition in line,
    'run start ':lambda condition,line: condition in line,
    'RuntimeException:':lambda condition,line: condition in line,
    'ItemDataMap:':lambda condition,line: condition in line
}

def check_battery_level():
    #file_name_condition.append('main_log_')
    #file_name_condition.append('logcat-log')
    #file_name_condition.append('android')
    filter_dic['**mStatus.pLevel:'] = '70'
    filter_dic['***mStatus.pLevel:'] = '60'
    filter_dic['battery status'] = 'result:false'
    filter_dic['BatteryService'] = 'run stop charger'
    filter_dic['run start '] = 'run start charger'
    pass

def check_tpopenshort():
    #file_name_condition.append('main_log_')
    #file_name_condition.append('logcat-log')
    #file_name_condition.append('android')
    filter_dic['tpOpenShort(): rt:'] = 'result=1'
    filter_dic['isScreenOn:'] = 'true'
    #do_check(file_name_condition,filter_dic)
    pass

def check_exception_reboot():
    #file_name_condition.append('main_log_')
    #file_name_condition.append('logcat-log')
    #file_name_condition.append('android')
    filter_dic['ADB_SERVICES:'] = 'service_to_fd'
    filter_dic['interceptKeyBeforeQueueing'] = 'keyCode ='
    filter_dic['DefaultItemActivity'] = 'onKeyDown:'
    filter_dic['AndroidRuntime'] = 'DeadSystemException'
    filter_dic['RunInTestII_activity:'] = 'mRebootExceptionTimes = 1'
    filter_dic['ItemDataMap:'] = 'time out'
    #filter_dic['ShutdownThread:'] = 'longPressBehavior=1'
    pass

def check_camera_exception():
    filter_dic['java.lang.RuntimeException:'] = 'takePicture failed'
    filter_dic['RuntimeException:'] = 'Fail to connect to camera service'
    pass

#check test result function ---
file_name_condition = []
filter_dic = {}
file_name_condition.append('main_log_')
file_name_condition.append('logcat-log')
file_name_condition.append('android')
check_battery_level()
check_tpopenshort()
check_exception_reboot()
check_camera_exception()
file_name_condition = [i for i in set(file_name_condition)]
print ("filter_dic: " + str(filter_dic))
write_result('report_pre.txt',do_check(file_name_condition,filter_dic))
