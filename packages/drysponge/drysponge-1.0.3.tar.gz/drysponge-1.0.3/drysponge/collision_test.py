import sys
import binascii
import os
import copy
import random
from base import SafeSponge

def collision_test_trial(impl,width):
    impl.Verbose(0)
    hmap = {}
    #impl.Verbose(SafeSponge.SPY_ALG_IO)
    for i in range(0,1<<width):
        if 0 == i % 0x10000:
            print("i=0x%x"%i)
        ii = random.randint(0, (1<<width)-1)
        ib = SafeSponge.int_to_bytes(ii,width)
        ob = impl.hash(ib)
        o = SafeSponge.bytes_to_int(ob)
        if o in hmap.keys():
            if hmap[o] != ii:
                print("Collision on output")
                SafeSponge.print_bytes_as_hex(ob)
                print("input a:")
                SafeSponge.print_bytes_as_hex(SafeSponge.int_to_bytes(hmap[o],width))
                print("input b:")
                SafeSponge.print_bytes_as_hex(ib)
                print("total hash count = %d"%len(hmap))
                return len(hmap)
        hmap[o] = ii
    return -1

def collision_test(impl,width,trials):
    hsum = 0
    for i in range(1,trials):
        hsum += collision_test_trial(impl,width)
        print("average hash to find 1 collision: %d"%(hsum//i))
