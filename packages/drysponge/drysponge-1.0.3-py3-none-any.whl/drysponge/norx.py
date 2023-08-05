import binascii
import copy

class Norx(object):
    def __init__(self,width,rounds=0):
        assert(width in [32,64])
        self.__width = width

    @staticmethod
    def rotr(val,r,width):
        return ((val >> r) ^ (val << (width-r))) % (1 << width)

    @staticmethod
    def h(x,y,mask):
        return mask & ((x^y)^((x&y)<<1))

    @staticmethod
    def g(a,b,c,d,width):
        mask = (1<<width)-1
        if 32==width:
            (r0,r1,r2,r3) = (8,11,16,31)
        else:
            (r0,r1,r2,r3) = (8,19,40,63)
        a = Norx.h(a,b,mask)
        d = Norx.rotr(a^d,r0,width)
        c = Norx.h(c,d,mask)
        b = Norx.rotr(b^c,r1,width)
        a = Norx.h(a,b,mask)
        d = Norx.rotr(a^d,r2,width)
        c = Norx.h(c,d,mask)
        b = Norx.rotr(b^c,r3,width)
        return (a,b,c,d)

    def round(self,S,round=0):
        """
        Norx core permutation.
        S: Norx state, a list of nw width-bit integers
        round: round to perform (not used since no round constants in NORX)
        returns nothing, updates S
        """
        #Col
        (S[ 0],S[ 4],S[ 8],S[12]) = self.g(S[ 0],S[ 4],S[ 8],S[12],self.__width)
        (S[ 1],S[ 5],S[ 9],S[13]) = self.g(S[ 1],S[ 5],S[ 9],S[13],self.__width)
        (S[ 2],S[ 6],S[10],S[14]) = self.g(S[ 2],S[ 6],S[10],S[14],self.__width)
        (S[ 3],S[ 7],S[11],S[15]) = self.g(S[ 3],S[ 7],S[11],S[15],self.__width)
        #Diag
        (S[ 0],S[ 5],S[10],S[15]) = self.g(S[ 0],S[ 5],S[10],S[15],self.__width)
        (S[ 1],S[ 6],S[11],S[12]) = self.g(S[ 1],S[ 6],S[11],S[12],self.__width)
        (S[ 2],S[ 7],S[ 8],S[13]) = self.g(S[ 2],S[ 7],S[ 8],S[13],self.__width)
        (S[ 3],S[ 4],S[ 9],S[14]) = self.g(S[ 3],S[ 4],S[ 9],S[14],self.__width)


if __name__ == "__main__":
    def test_vector32():
        u = [
            0x0454EDAB,
            0xAC6851CC,
            0xB707322F,
            0xA0C7C90D,
            0x99AB09AC,
            0xA643466D,
            0x21C22362,
            0x1230C950,
            0xA3D8D930,
            0x3FA8B72C,
            0xED84EB49,
            0xEDCA4787,
            0x335463EB,
            0xF994220B,
            0xBE0BF5C9,
            0xD7C49104]
        s = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        impl = Norx(32)
        impl.round(s)
        impl.round(s)
        for i in range(0,16):
            print("%2d %08x"%(i,s[i]))
            assert(s[i]==u[i])

    def test_vector64():
        u = [
            0xE4D324772B91DF79,
            0x3AEC9ABAAEB02CCB,
            0x9DFBA13DB4289311,
            0xEF9EB4BF5A97F2C8,
            0x3F466E92C1532034,
            0xE6E986626CC405C1,
            0xACE40F3B549184E1,
            0xD9CFD35762614477,
            0xB15E641748DE5E6B,
            0xAA95E955E10F8410,
            0x28D1034441A9DD40,
            0x7F31BBF964E93BF5,
            0xB5E9E22493DFFB96,
            0xB980C852479FAFBD,
            0xDA24516BF55EAFD4,
            0x86026AE8536F1501]
        s = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        impl = Norx(64)
        impl.round(s)
        impl.round(s)
        for i in range(0,16):
            print("%2d %016x"%(i,s[i]))
            assert(s[i]==u[i])

    test_vector32()
    test_vector64()
