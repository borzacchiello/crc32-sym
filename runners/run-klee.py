import subprocess
import time
import zlib
import os

from tdeco import timeout, TimeoutError

def get_buff(f):
    with open(f, "rb") as f:
        raw_test = f.read()

    buf_idx = 0
    for i in range(len(raw_test)):
        if raw_test[i:].startswith(b"sym_buf"):
            buf_idx = i + len("sym_buf")

    l    = int.from_bytes(raw_test[buf_idx:buf_idx+4], "big")
    data = raw_test[buf_idx+4:buf_idx+4+l]
    return data

@timeout(3600)
def run_one(size):
    start = time.time()
    subprocess.check_call(["klee", "--solver-backend=z3", "./main.bc", str(size)])
    elapsed = time.time() - start

    buf1 = get_buff("./klee-last/test000001.ktest")
    buf2 = get_buff("./klee-last/test000002.ktest")

    os.system("rm -rf ./klee-*")

    return elapsed, zlib.crc32(buf1), zlib.crc32(buf2)

def run():
    fout = open("./results/klee_data.csv", "w")

    size = 1
    while size <= 1024:
        try:
            elapsed, crc1, crc2 = run_one(size)
        except TimeoutError:
            elapsed, crc1, crc2 = 3600, 0, 0
            fout.write("%s, %f, %#x, %#x\n" % (size, elapsed, crc1, crc2))
            break

        fout.write("%s, %f, %#x, %#x\n" % (size, elapsed, crc1, crc2))
        fout.flush()

        size *= 2

    while size <= 1024:
        fout.write("%s, %f, %#x, %#x\n" % (size, 3600, 0, 0))
        fout.flush()

        size *= 2

    fout.close()

run()
