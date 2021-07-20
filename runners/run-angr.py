import sys
import angr
import zlib
import time
import ctypes
import claripy

from tdeco import timeout, TimeoutError

libc_native_path = ctypes.util.find_library('c')
libc_native = ctypes.cdll.LoadLibrary(libc_native_path)

class srand(angr.SimProcedure):
    def run(self, seed):
        # print("srand(%#x)" % seed.args[0])
        libc_native.srand(seed.args[0])
        return claripy.BVV(1, 32)

class rand(angr.SimProcedure):
    def run(self):
        val = libc_native.rand()
        # print("rand() = %#x" % val)
        return claripy.BVV(val, 64)

@timeout(3600)
def run_one(proj, size):
    args = [proj.filename, str(size)]
    s    = proj.factory.entry_state(args=args)

    s.memory.read_strategies = [
        angr.concretization_strategies.SimConcretizationStrategyRange(sys.maxsize)
    ]

    simgr = proj.factory.simgr(s)

    start = time.time()
    simgr.explore(find=0x40069d, avoid=[0x4006a9])
    elapsed = time.time() - start

    # print(simgr.found[0].posix.dumps(0))
    return elapsed, zlib.crc32(simgr.found[0].posix.dumps(0))

def run():
    proj = angr.Project("./main", auto_load_libs=False)
    proj.hook_symbol("srand", srand(), replace=True)
    proj.hook_symbol("rand", rand(), replace=True)

    fout = open("./results/angr_data.csv", "w")

    size = 1
    while size <= 1024:
        print("[+] running with size %d" % size)
        try:
            elapsed, crc = run_one(proj, size)
        except TimeoutError:
            elapsed, crc = 3600, 0
            fout.write("%s, %f, %#x\n" % (size, elapsed, crc))
            break

        print("[+] size %d done" % size)
        fout.write("%s, %f, %#x\n" % (size, elapsed, crc))
        fout.flush()

        size *= 2

    while size <= 1024:
        fout.write("%s, %f, %#x\n" % (size, 3600, 0))
        fout.flush()

        size *= 2

    fout.close()

run()