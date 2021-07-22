import seninja
import zlib
import time
import os

SCRIPTDIR = os.path.realpath(os.path.dirname(__file__))

def run_one(bv, buff: str):
    size    = len(buff)
    bv_list = seninja.str_to_bv_list(buff)

    seninja.start_se(bv, 0x4006c0)
    seninja.setup_argv(
        seninja.str_to_bv(str(size), terminator=True))

    s = seninja.get_current_state()
    s.os.write(0, bv_list)
    s.os.seek(0, 0)

    start = time.time()
    address = 0x400785
    while s.get_ip() != address:
        seninja.execute_one_instruction()
        s = seninja.get_current_state().copy()
    elapsed = time.time() - start

    seninja.reset_se()
    return s, elapsed

def run(bv):
    fout = open(os.path.join(SCRIPTDIR, "../results/seninja_data_copy_cow.csv"), "w")
    size = 1
    while size <= 1024:
        print("[+] running size %d" % size)

        _, elapsed = run_one(bv, "a" * size)

        fout.write("%s, %f\n" % (size, elapsed))
        fout.flush()

        size *= 2

    fout.close()
