import seninja
import psutil
import zlib
import time
import os
import gc

SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))

def run_one(bv, size):
    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss

    seninja.start_se(bv, 0x4006c0)
    executor = seninja.get_executor()
    executor.bncache.settings["save_unsat"] = "true"

    seninja.setup_argv(
        seninja.str_to_bv(str(size), terminator=True))

    # Just before the branch
    s = seninja.continue_until_address(0x400697)
    end_mem = process.memory_info().rss - start_mem

    print(executor.fringe)

    seninja.reset_se()
    return s, end_mem

def run(bv):
    fout = open(os.path.join(SCRIPTDIR, "../results/seninja_data_no_solver_cow.csv"), "w")
    size = 1
    while size <= 1024:
        print("[+] running size %d" % size)

        start        = time.time()
        _, mem_usage = run_one(bv, size)
        elapsed      = time.time() - start

        print("[+] calling GC...", end=" ")
        gc.collect()
        print("DONE")
        fout.write("%s, %d, %f\n" % (size,  mem_usage, elapsed))
        fout.flush()

        size *= 2

    fout.close()
