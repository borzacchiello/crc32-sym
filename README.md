# Symbolic Benchmark CRC32

This repository contains a CRC32 benchmark for symbolic engines. You can use the scripts under `runners` to run angr and KLEE on the benchmark.

### Compile

Just type `make`.

To compile the binary for KLEE:

```
$ docker pull klee/klee:2.2
$ make start-klee-docker
klee@8e72bbd9050d:~$ cd CRC32
klee@8e72bbd9050d:~/CRC32$ make klee
```
