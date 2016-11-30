import sys
import bench_timecmd as bt

args = sys.argv
argc = len(args)
if (argc < 3):
    print("Usage: python %s run_file mode [loop_num]" % args[0])
    quit()
elif (argc == 3):
    bench = bt.Bench(args[1],args[2])
else:
    bench = bt.Bench(args[1],args[2],args[3])

for i in range(1,11):
    bench.run_loop_time(i*100,i*100)
