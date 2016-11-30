import subprocess
import csv
import sys
import datetime
import re
import os

class Bench:

    def __init__(self, name, num=1):
        dir_name = "data"

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

        self.file_name = name
        self.run_num = int(num)

        date = datetime.date.today().strftime("%Y%m%d")
        name = re.sub('\w+/', "", self.file_name).replace('.rb', '')
        log_name = '%s_%s.txt' % (name,date)
        csv_name = '%s_%s.csv' % (name,date)
        self.log_path = dir_name + "/" + log_name
        self.csv_path = dir_name + "/" + csv_name


    def cmd_run(self,cmd):
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("%s\n%s\n%d\n" % (p.stdout.decode('utf-8'),p.stderr,p.returncode))
        return p

    def run_loop_time(self,*args):
        param = args
        date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
        cmd = "/usr/bin/time -p ruby %s" % self.file_name
        for arg in args:
            cmd += (" %s" % str(arg))

        f = open(self.csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([date,param])
        f.close()

        num = 0
        count = 0
        while num < self.run_num:
            ret = self.cmd_run(cmd)
            if (ret.returncode == 0):
                # write txt
                f = open(self.log_path,'a')
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

                    f = open(self.csv_path, 'a')
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerow([num,time_ms[0]])
                    f.close()

                num += 1
            else:
                # write txt
                f = open(self.log_path,'a')
                f.write("%s %s\n" % (date,str(args)))
                f.write("%s\n" % ret.stdout.decode('utf-8'))
                f.write("%s\n" % ret.stderr.decode('utf-8'))
                f.close()

            count += 1
            if (self.run_num*2<count):
                break

        f = open(self.csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow("")
        f.close()

    def run_loop(self,*args):
        param = args
        date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
        cmd = "ruby %s" % self.file_name
        for arg in args:
            cmd += (" %s" % str(arg))

        f = open(self.csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([date,param])
        f.close()

        num = 0
        count = 0
        while num < self.run_num:
            ret = self.cmd_run(cmd)
            if (ret.returncode == 0):
                # write txt
                f = open(self.log_path,'a')
                f.write("%s %s\n" % (date,str(args)))
                f.write("%s\n" % ret.stdout.decode('utf-8'))
                f.close()

                # write csv
                results = ret.stdout.decode('utf-8').split("\n")
                results.remove('')
                for result in results:
                    # [num:bench[s]]
                    run_index,run_time = result.split(":")
                    f = open(self.csv_path, 'a')
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerow([num,run_time])
                    f.close()
                num += 1
            else:
                # write txt
                f = open(self.log_path,'a')
                f.write("%s %s\n" % (date,str(args)))
                f.write("%s\n" % ret.stderr.decode('utf-8'))
                f.close()

            count += 1
            if (self.run_num*2<count):
                f = open(self.log_path,'a')
                f.write("not run loop_num times\n")
                f.close()
                break

        f = open(self.csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow("")
        f.close()
