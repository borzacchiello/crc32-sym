all:
	clang main.c -o main
	clang -DPRINTCRC main.c -o main-dbg

klee:
	clang -DKLEE -I ../../include -emit-llvm -c -g -O0 -Xclang -disable-O0-optnone main.c

run-klee:
	klee --solver-backend=z3 main.bc ${NSYM}

run-klee-docker:
	docker run --rm -it -v /home/luca/code/C/CRC32_SENinja:/home/klee/CRC32 klee/klee:2.2 bash

clean:
	rm -f main main-dbg main.bc
