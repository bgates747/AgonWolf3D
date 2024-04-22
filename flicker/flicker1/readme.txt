version 5 not only flickers badly on hardware, it doesn't even make it into the proper screen mode. runs as expected on the emulator.

version 6 runs correctly on both hardware and the emulator

the only difference between the two versions is that 6 loads far fewer image buffers ... see the code which has been commented out beginning at line 595. 

hardware: C8 vdp 2.8.0 mos 2.2.3
emulator: 0.9.43 vdp 2.7.3 mos 2.2.3 ubuntu 22.04