import sys
import bench_timecmd as bt

args = sys.argv
argc = len(args)
if (argc < 2):
    print("Usage: python %s run_file [loop_num]" % args[0])
    quit()
elif (argc == 2):
    bench = bt.Bench(args[1])
else:
    bench = bt.Bench(args[1],args[2])

for i in range(1,11):
    bench.run_loop_time(i*100,i*100)
