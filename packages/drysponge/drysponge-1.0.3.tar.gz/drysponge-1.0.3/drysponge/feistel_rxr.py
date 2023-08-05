
import binascii
import copy

class Rxr(object):
    def __init__(self, width, x):
        self.__width = width
        self.__limit = 1<<width
        self.__mask = self.__limit-1
        assert(x<self.__limit)
        self.__x = x

    def __rotr(self,i,shift):
        assert(shift<self.__width)
        o = self.__mask & ((i>>shift)|(i<<(self.__width-shift)))
        assert(o<self.__limit)
        return o

    def x(self):
        return copy.deepcopy(self.__x)

    def apply(self,i,shift):
        assert(i<self.__limit)
        o = i
        o = self.__rotr(o,shift)
        o ^= self.__x
        o = self.__rotr(o,shift)
        #print("i=%x --> o=%x (x=%x)"%(i,o,self.__x))
        assert(o<self.__limit)
        return o

class FeistelRxr(object):
    def __init__(self, total_width, rounds, x, double_rounds=False):
        assert(0==(total_width%2))
        self.__rounds = rounds
        self.__double_rounds = double_rounds
        self.__total_width = total_width
        self.__total_limit = 1<<total_width
        width = total_width // 2 #width of a branch
        self.__width = width
        self.__limit = 1<<width
        self.__mask = self.__limit-1
        self.__rxr = []
        for xi in x:
            assert(xi<self.__limit)
            self.__rxr.append(Rxr(width,xi))
        self.__xlen = len(x)
        self.__key_width = (width-1).bit_length()
        self.__key_limit = 1<<self.__key_width
        self.__key_mask = self.__key_limit-1
        self.__total_key_width = self.__key_width*self.__rounds
        self.__total_key_limit = 1<<self.__total_key_width
        #print("width",width)
        #print("width.bit_length()",(width-1).bit_length())
        #print("self.__key_width",self.__key_width)
        #print("self.__xlen",self.__xlen)
        #print("self.__key_mask = 0x%x"%self.__key_mask)

    def key_width(self):
        return self.__total_key_width

    def apply(self, i, k):
        assert(i<self.__total_limit)
        assert(k<self.__total_key_limit)
        c = [i & self.__mask, i >> self.__width]
        #print("c[0]=%08x, c[1]=%08x r0=%x r1=%x x0=%x, x1=%x --> "%(c[0],c[1],k&self.__key_mask,k>>self.__key_width,self.__rxr[0].x(),self.__rxr[1].x()),end="")
        total_rounds = self.__rounds
        rdiv = 1
        if self.__double_rounds:
            total_rounds *= 2
            rdiv = 2
        for round in range(0,total_rounds):
            kr = k & self.__key_mask
            if 0 == ((round+1) % rdiv):
                k = k >> self.__key_width
            c[(round+1)%2] ^= self.__rxr[(round // rdiv)% self.__xlen].apply(c[round%2],kr)
        #print("c[0]=%08x, c[1]=%08x"%(c[0],c[1]))
        return (c[1]<<self.__width)|c[0]

class FeistelRxrPX(object):
    def __init__(self, unit_width, rounds, x, pw,xw,double_rounds=False):
        self.__nw = pw+xw
        assert(pw>xw)
        self.__pw = pw
        self.__xw = xw
        self.__frxr = []
        assert(0==(len(x)%rounds))
        for i in range(0,self.__nw):
            s = (i*rounds) % len(x)
            e = s+rounds
            self.__frxr.append(FeistelRxr(unit_width,rounds,x[s:e],double_rounds) )
        self.__total_width = self.__nw * unit_width
        self.__total_limit = 1<<self.__total_width
        self.__unit_width = unit_width
        self.__unit_limit = 1<<unit_width
        self.__unit_mask = self.__unit_limit-1
        self.__unit_key_width = self.__frxr[0].key_width()
        self.__unit_key_limit = 1<<self.__unit_key_width
        self.__unit_key_mask = self.__unit_key_limit-1
        self.__total_key_width = self.__pw * self.__unit_key_width
        self.__total_key_limit = 1<<self.__total_key_width
        self.__xk_width = xw*self.__unit_key_width
        #print("self.__unit_key_width",self.__unit_key_width)
        #print("self.__total_key_width",self.__total_key_width)
        #print("self.__unit_key_mask = 0x%x"%self.__unit_key_mask)

    def key_width(self):
        return self.__total_key_width

    def apply(self, i, k):
        assert(i<self.__total_limit)
        assert(k<self.__total_key_limit)
        o = 0
        xk = 0
        c = i
        a = c>>(self.__pw*self.__unit_width) & self.__unit_mask
        for w in range(0,self.__pw):
            wi = i & self.__unit_mask
            i = i >> self.__unit_width
            kr = k & self.__unit_key_mask
            k = k >> self.__unit_key_width
            if self.__xk_width>0:
                xk ^= kr<<((w*self.__unit_key_width) % self.__xk_width)
                #print("xk",xk)
            wi = self.__frxr[w].apply(wi,kr)
            o |= wi << (self.__unit_width*w)
            wi = c>>(self.__pw*self.__unit_width) & self.__unit_mask
            wi = self.__frxr[w].apply(wi,kr)
            a ^= wi
        o |= a << (self.__unit_width*self.__pw)

        return o

class PairedRxr(object):
    def __init__(self, total_width, rounds, x):
        assert(0==(total_width%2))
        self.__rounds = rounds
        self.__total_width = total_width
        self.__total_limit = 1<<total_width
        width = total_width // 2 #width of a branch
        self.__width = width
        self.__limit = 1<<width
        self.__mask = self.__limit-1
        self.__rxr = []
        for xi in x:
            assert(xi<self.__limit)
            self.__rxr.append(Rxr(width,xi))
        self.__xlen = len(x)
        self.__key_width = (width-1).bit_length()
        self.__key_limit = 1<<self.__key_width
        self.__key_mask = self.__key_limit-1
        self.__total_key_width = self.__key_width*self.__rounds
        self.__total_key_limit = 1<<self.__total_key_width
        #print("width",width)
        #print("width.bit_length()",(width-1).bit_length())
        #print("self.__key_width",self.__key_width)
        #print("self.__xlen",self.__xlen)
        #print("self.__key_mask = 0x%x"%self.__key_mask)

    def key_width(self):
        return self.__total_key_width

    def apply(self, i, k):
        assert(i<self.__total_limit)
        assert(k<self.__total_key_limit)
        c = [i & self.__mask, i >> self.__width]
        #print("c[0]=%08x, c[1]=%08x r0=%x r1=%x x0=%x, x1=%x --> "%(c[0],c[1],k&self.__key_mask,k>>self.__key_width,self.__rxr[0].x(),self.__rxr[1].x()),end="")
        for round in range(0,self.__rounds):
            kr = k & self.__key_mask
            k = k >> self.__key_width
            c[round%2] = self.__rxr[round%self.__xlen].apply(c[round%2],kr)
        #print("c[0]=%08x, c[1]=%08x"%(c[0],c[1]))
        return (c[1]<<self.__width)|c[0]

class PairedRxrPX(object):
    def __init__(self, unit_width, rounds, x, pw,xw):
        self.__nw = pw+xw
        assert(pw>xw)
        self.__pw = pw
        self.__xw = xw
        self.__frxr = []
        assert(0==(len(x)%rounds))
        for i in range(0,self.__nw):
            s = (i*rounds) % len(x)
            e = s+rounds
            self.__frxr.append(PairedRxr(unit_width,rounds,x[s:e]) )
        self.__total_width = self.__nw * unit_width
        self.__total_limit = 1<<self.__total_width
        self.__unit_width = unit_width
        self.__unit_limit = 1<<unit_width
        self.__unit_mask = self.__unit_limit-1
        self.__unit_key_width = self.__frxr[0].key_width()
        self.__unit_key_limit = 1<<self.__unit_key_width
        self.__unit_key_mask = self.__unit_key_limit-1
        self.__total_key_width = self.__pw * self.__unit_key_width
        self.__total_key_limit = 1<<self.__total_key_width
        self.__xk_width = xw*self.__unit_key_width
        #print("self.__unit_key_width",self.__unit_key_width)
        #print("self.__total_key_width",self.__total_key_width)
        #print("self.__unit_key_mask = 0x%x"%self.__unit_key_mask)

    def key_width(self):
        return self.__total_key_width

    def apply(self, i, k):
        assert(i<self.__total_limit)
        assert(k<self.__total_key_limit)
        o = 0
        c = i
        a = c>>(self.__pw*self.__unit_width) & self.__unit_mask
        for w in range(0,self.__pw):
            wi = i & self.__unit_mask
            i = i >> self.__unit_width
            kr = k & self.__unit_key_mask
            k = k >> self.__unit_key_width
            wi = self.__frxr[w].apply(wi,kr)
            o |= wi << (self.__unit_width*w)
            wi = c>>(self.__pw*self.__unit_width) & self.__unit_mask
            wi = self.__frxr[(w+1)%2].apply(wi,kr)
            a ^= wi
        o |= a << (self.__unit_width*self.__pw)

        return o
