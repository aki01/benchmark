import subprocess
import csv
import sys
import datetime
import re
import os
import platform

class Bench:

    def __init__(self, name, mode=0, num=1):
        dir_name = "data"

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)

        self.file_name = name
        self.run_num = int(num)

        date = datetime.date.today().strftime("%Y%m%d")
        name = re.sub('\w+/', "", self.file_name).replace('.rb', '')
        log_name = '%s_%s.txt' % (name,date)
        csv_name = '%s_%s.csv' % (name,date)
        csv_avg_name = '%s_%s_avg.csv' % (name,date)
        self.log_path = dir_name + "/" + log_name
        self.csv_path = dir_name + "/" + csv_name
        self.csv_avg_path = dir_name + "/" + csv_avg_name
        self.select = int(mode)
        self.avg = []

        if (self.select == 0):
            date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
            f = open(self.csv_avg_path, 'a')
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([date,str("loop:%d" % self.run_num)])
            f.close()
        elif (self.select >= 2 ) :
            print("run_loop_time: self.select = 0 or 1")
            print("    0: # time ruby ...")
            print("    1: # ruby ...")
            quit()

    def cmd_run(self,cmd):
        p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #print("%s\n%s\n%d\n" % (p.stdout.decode('utf-8'),p.stderr,p.returncode))
        return p

    def run_loop_time(self,*args):
        param = args
        date = datetime.datetime.today().strftime("%Y%m%d %H:%M:%S")
        if (self.select == 0):
            if (platform.system() == 'Darwin'):
                cmd = "time ruby %s" % self.file_name
            else :
                cmd = "/usr/bin/time -p ruby %s" % self.file_name
        elif (self.select == 1):
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
                f.write("%s\n" % ret.stderr.decode('utf-8'))
                f.close()

                # write csv

                if (self.select == 0):
                    time_out = ret.stderr.decode('utf-8')
                    if (platform.system() == 'Darwin'):
                        real_time = re.search('real\t([a-zA-Z0-9_.]+)\n', time_out)
                    else :
                        real_time = re.search('real ([a-zA-Z0-9_.]+)\n', time_out)

                    if (real_time != None):
                        if (platform.system() == 'Darwin'):
                            time_get = re.findall('[0-9.]+',real_time.group(0))
                            time_ms = float(time_get[0]) * 60.0 + float(time_get[1])
                        else :
                            time_get = re.findall('[0-9.]+',real_time.group(1))
                            time_ms = float(time_get[0])

                        f = open(self.csv_path, 'a')
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerow([num,time_ms])
                        f.close()

                        self.avg.append(time_ms)

                elif (self.select == 1):
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
                f = open(self.log_path,'a')
                f.write("%s %s\n" % (date,str(args)))
                f.write("%s\n" % ret.stdout.decode('utf-8'))
                f.write("%s\n" % ret.stderr.decode('utf-8'))
                f.close()

            count += 1
            if (self.run_num*2<count):
                f = open(self.log_path,'a')
                f.write("not run loop_num times\n")
                f.close()
                break

        if (self.select == 0):
            agt_num = 1
            for n in param:
                agt_num *= n
            time_avg = sum(self.avg) / len(self.avg)

            f = open(self.csv_avg_path, 'a')
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([agt_num,time_avg])
            f.close()

        f = open(self.csv_path, 'a')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow("")
        f.close()
