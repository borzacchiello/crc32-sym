import seninja
import zlib
import time
import os

SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))

def run_one(bv, size):
    seninja.start_se(bv, 0x4006c0)
    seninja.setup_argv(
        seninja.str_to_bv(str(size), terminator=True))

    t, f = seninja.continue_until_branch()

    seninja.reset_se()
    return t, f

def run(bv):
    fout = open(os.path.join(SCRIPTDIR, "../results/seninja_data.csv"), "w")
    size = 1
    while size <= 1024:
        print("[+] running size %d" % size)
        start   = time.time()
        _, f    = run_one(bv, size)
        elapsed = time.time() - start

        print("[+] evaluating for size %d" % size)
        buf = f.solver.evaluate(seninja.get_stdin_bv(f)).as_bytes()
        fout.write("%s, %f, %#x\n" % (size, elapsed, zlib.crc32(buf)))
        fout.flush()

        size *= 2

    fout.close()
