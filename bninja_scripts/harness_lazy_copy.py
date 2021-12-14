from guppy import hpy

import seninja
import psutil
import zlib
import time
import os
import gc

SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))
h = hpy()

def run_one(bv, size):
    process = psutil.Process(os.getpid())
    start_mem_pr = process.memory_info().rss
    start_mem_gp = h.heap().size

    start = time.time()
    seninja.start_se(bv, 0x4006c0)
    executor = seninja.get_executor()
    executor.bncache.settings["save_unsat"] = "true"

    seninja.setup_argv(
        seninja.str_to_bv(str(size), terminator=True))

    # Just before the branch
    s = seninja.continue_until_address(0x400697)
    elapsed  = time.time() - start
    used_mem_gp = h.heap().size - start_mem_gp
    used_mem_pr = process.memory_info().rss - start_mem_pr

    print(executor.fringe)

    seninja.reset_se()
    return s, elapsed, used_mem_gp, used_mem_pr

def run(bv):
    # heat up
    _ = run_one(bv, 1)

    fout = open(os.path.join(SCRIPTDIR, "../results/seninja_data_no_solver_cow_2048.csv"), "w")
    size = 1
    while size <= 1024:
        print("[+] running size %d" % size)

        _, elapsed, mem_usage_gp, _ = run_one(bv, size)

        print("[+] calling GC...", end=" ")
        gc.collect()
        print("DONE")
        fout.write("%s, %d, %f\n" % \
            (size,  mem_usage_gp, elapsed))
        fout.flush()

        size *= 2

    fout.close()
