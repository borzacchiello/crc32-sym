mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

all:
	clang main.c -o main
	clang -DPRINTCRC main.c -o main-dbg

klee:
	clang -DKLEE -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone main.c

start-klee-docker:
	docker run --rm -it -v $(current_dir):/home/klee/CRC32 klee/klee:2.2 bash

clean:
	rm -f main main-dbg main.bc
