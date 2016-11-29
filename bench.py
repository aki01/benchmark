import subprocess
import csv
import sys
import datetime
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

def run(*args):
    param = args
    date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
    cmd = "ruby %s" % file_name
    for arg in args:
        cmd += (" %s" % str(arg))
    ret = cmd_run(cmd)

    if (ret.returncode == 0):
        # write txt
        f = open(log_path,'a')
        f.write("%s %s\n" % (date,str(args)))
        f.write("%s\n" % ret.stdout.decode('utf-8'))
        f.close()

        # write csv
        results = ret.stdout.decode('utf-8').split("\n")
        results.remove('')
        f = open(csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([date,param])
        f.close()
        for result in results:
            # [num:bench[s]]
            loop_num,run_time = result.split(":")
            f = open(csv_path, 'a')
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([loop_num,run_time])
            f.close()
    else:
        # write txt
        f = open(log_path,'a')
        f.write("%s %s\n" % (date,str(args)))
        f.write("%s\n" % ret.stderr.decode('utf-8'))
        f.close()

def run_loop(loop_num,*args):
    param = args
    date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
    cmd = "ruby %s" % file_name
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
            f.close()

            # write csv
            results = ret.stdout.decode('utf-8').split("\n")
            results.remove('')
            for result in results:
                # [num:bench[s]]
                run_index,run_time = result.split(":")
                f = open(csv_path, 'a')
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow([num,run_time])
                f.close()
            num += 1
        else:
            # write txt
            f = open(log_path,'a')
            f.write("%s %s\n" % (date,str(args)))
            f.write("%s\n" % ret.stderr.decode('utf-8'))
            f.close()

        count += 1
        if (loop_num*2<count):
            f = open(log_path,'a')
            f.write("not run loop_num times\n")
            f.close()
            break

    f = open(csv_path, 'a')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow("")
    f.close()

for i in range(1,11):
    run_loop(run_num,i*100,i*100)
