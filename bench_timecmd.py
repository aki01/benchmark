import subprocess
import csv
import sys
import datetime
import re
import os

args = sys.argv
argc = len(args)
if (argc != 3):
    print("Usage: python %s arg1 arg2" % args[0])
    quit()

dir_name = "data"
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)

file_name = args[1]
run_num = int(args[2])

date = datetime.date.today().strftime("%Y%m%d")
name = file_name.replace('.rb', '')
log_name = '%s_%s.txt' % (name,date)
csv_name = '%s_%s.csv' % (name,date)
log_path = dir_name + "/" + log_name
csv_path = dir_name + "/" + csv_name


def cmd_run(cmd):
    p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print("%s\n%s\n%d\n" % (p.stdout.decode('utf-8'),p.stderr,p.returncode))
    return p

def run_loop_time(loop_num,*args):
    param = args
    date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
    cmd = "/usr/bin/time -p ruby %s" % file_name
    for arg in args:
        cmd += (" %s" % str(arg))

    f = open(csv_path, 'a')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow([date,param])
    f.close()

    num = 0
    count = 0
    while num < loop_num:
        ret = cmd_run(cmd)
        if (ret.returncode == 0):
            # write txt
            f = open(log_path,'a')
            f.write("%s %s\n" % (date,str(args)))
            f.write("%s\n" % ret.stdout.decode('utf-8'))
            f.write("%s\n" % ret.stderr.decode('utf-8'))
            f.close()

            # write csv
            time_out = ret.stderr.decode('utf-8')
            a = re.search('real ([a-zA-Z0-9_.]+)\n', time_out)
            #a = re.search('real\t([a-zA-Z0-9_.]+)\n', time_out)
            if (a != None):
                time_ms = re.findall('[0-9.]+',a.group(1))
                #tims_second = float(time_ms[0]) * 60.0 + float(time_ms[1])

                f = open(csv_path, 'a')
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow([num,time_ms[0]])
                f.close()

            num += 1
        else:
            # write txt
            f = open(log_path,'a')
            f.write("%s %s\n" % (date,str(args)))
            f.write("%s\n" % ret.stdout.decode('utf-8'))
            f.write("%s\n" % ret.stderr.decode('utf-8'))
            f.close()

        count += 1
        if (loop_num*2<count):
            break

    f = open(csv_path, 'a')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow("")
    f.close()

for i in range(1,11):
    run_loop_time(run_num,i*100,i*100)
