#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "crc32.h"

#ifdef KLEE
#include <klee/klee.h>
#endif

#define SEED 0xabadcafe

int test_harness(char* sym_buf, char* conc_buf, int len) {
    // compute CRC of symbolic bytes
    unsigned int conc_crc = crc32(conc_buf, len);
    unsigned int sym_crc  = crc32(sym_buf, len);

#ifdef PRINTCRC
    printf("size: %d, crc: %#x\n", len, conc_crc);
#endif

    // compare the two CRCs
    if (sym_crc == conc_crc) {
        return 1;
    }
    return 0;
}

int main(int argc, char* argv[])
{
    if (argc < 2)
        return -1;

    int len = atoi(argv[1]);

    char* sym_buf  = (char*)malloc(sizeof(char) * len);
    char* conc_buf = (char*)malloc(sizeof(char) * len);

    srand(SEED);

    int i;
    for (i = 0; i < len; i++)
        conc_buf[i] = (char) rand();

#ifdef KLEE
    klee_make_symbolic(sym_buf, len, "sym_buf");
#else
    read(0, sym_buf, len);
#endif

    return test_harness(sym_buf, conc_buf, len);
}