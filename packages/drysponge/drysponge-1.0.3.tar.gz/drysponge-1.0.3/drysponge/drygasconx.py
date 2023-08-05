
import binascii
import copy
import sys
import math

if __name__ == "__main__":
    from base import DrySponge
    from gascon import Gascon
else:
    from drysponge.base import DrySponge
    from drysponge.gascon import Gascon

class DryGasconx(object):
    def __init__(self,key_min_width,nonce_width,rate_width,capacity_width,x_width,init_rounds,rounds,accumulate_factor=2):
        assert(0==(capacity_width%64))
        self.nw = capacity_width // 64
        assert(1==(self.nw % 2))
        self.InitRounds = init_rounds
        self.Rounds = rounds
        #self.FinalRounds = final_rounds
        self.MinKeyWidth = key_min_width
        self.NonceWidth = nonce_width
        self.RateWidth = rate_width
        self.CapacityWidth = capacity_width
        assert(0==(x_width%32))
        self.xwords = x_width // 32
        self.MprInputWidth = (self.xwords-1).bit_length()*(self.CapacityWidth//32)
        #print(self.RateWidth,self.xwords,self.MprInputWidth)
        self.MprInputMask = (1<<self.MprInputWidth)-1
        self.XIdxWidth = (self.xwords-1).bit_length()
        self.XIdxMask = (1<<self.XIdxWidth)-1
        self.AccumulateFactor = accumulate_factor
        self.mprounds = (self.RateWidth+self.MprInputWidth-1)// self.MprInputWidth
        #print(self.mprounds,self.XIdxWidth,self.XIdxMask)
        self.dsfree = (self.mprounds*self.MprInputWidth-4 >= rate_width)
        assert(self.dsfree)
        self.ds=None

    @staticmethod
    def DryGasconx128():
        return DryGasconx(128,128,128,320,32*4,12,8,2)

    @staticmethod
    def DryGasconx256():
        return DryGasconx(256,128,128,576,32*4,12,8,4)

    def instance(self):
        return DrySponge(self)

    def DomainSeparator(self,pad,domain,finalize):
        self.ds = pad+finalize*2+domain*4

    def MixPhaseRound(self,c,x,ib,biti,ds=None):
        #DrySponge.print_bytes_as_hex(c)
        ii =   DrySponge.bytes_to_int(ib)
        if ds is not None:
            #print("ds=%x"%ds)
            #print(ib)
            ii |= ds << (len(ib)*8)
        r=(ii>>biti) & self.MprInputMask
        #print("biti=%d, r=0x%x"%(biti,r))
        for j in range(0,self.CapacityWidth // 32):
            i = r & self.XIdxMask
            r = r>>self.XIdxWidth
            for k in range(0,4):
                #print(i,j,k,j*4+k,i*4+k)
                c[j*4+k] ^= x[i*4+k]
        return (c,x)

    def MixPhase(self,c,x,i):
        biti=0
        for j in range(0,self.mprounds-1):
            (c,x) = self.MixPhaseRound(c,x,i,biti)
            #DrySponge.print_bytes_as_hex(c)
            biti += self.MprInputWidth
            c = self.CoreRound(c,self.InitRounds,0)
            c = self.CoreRound(c,self.InitRounds,1)
        (c,x) = self.MixPhaseRound(c,x,i,biti,self.ds)
        self.ds = None
        return (c,x)

    def CoreRound(self,c,rounds,round):
        S = [0]*self.nw
        for i in range(0,self.nw):
            S[i] = DrySponge.bytes_to_int(c[i*8:(i+1)*8])
        gascon = Gascon(self.nw,rounds)
        gascon.round(S,round)
        for i in range(0,self.nw):
            c[i*8:(i+1)*8] = DrySponge.int_to_bytes(S[i],64)
        return c

if __name__ == "__main__":
    if 128==int(sys.argv[1]):
        impl = DryGasconx.DryGasconx128().instance()
    if 256==int(sys.argv[1]):
        impl = DryGasconx.DryGasconx256().instance()
    def gen_hash_test_vectors():
        print(r"""\newpage
        \subsection{Hash test vectors}""")
        impl.Verbose(DrySponge.SPY_FULL)
        print(r"""\begin{lstlisting}[caption={Detailed test vector}]""")
        impl.hash(binascii.unhexlify(b'0001020304050607'))
        impl.Verbose(DrySponge.SPY_F_IO)
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Less detailed test vector}]""")
        impl.hash(binascii.unhexlify(b'0001020304050607'))
        impl.Verbose(DrySponge.SPY_ALG_IO)
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Test vectors}]""")
        m=binascii.unhexlify(b'')
        for i in range(0,33):
            impl.hash(m)
            m+=bytes([i])
        impl.Verbose(DrySponge.SPY_NONE)
        iterations = 100
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Iterative test vector}]""")
        print("Hashing null message %d times"%iterations)
        m=binascii.unhexlify(b'')
        for i in range(0,iterations):
            m=impl.hash(m)
        print("   Digest: ",end="")
        DrySponge.print_bytes_as_hex(m)
        print(r"""\end{lstlisting}""")

    def gen_aead_test_vectors():
        print(r"""
\subsection{AEAD test vectors}""")
        impl.Verbose(DrySponge.SPY_F_IO)
        nonce = binascii.unhexlify(b'F0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF')[0:impl.nonce_size()]
        #key = binascii.unhexlify(b'000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F')[0:impl.key_size()]
        key = bytearray()
        for i in range(0,impl.fullkey_size()):
            key.append(i)
        print(r"""\begin{lstlisting}[caption={Detailed test vector: m=0, a=0, full key profile}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b''),binascii.unhexlify(b''))
        print(r"""\end{lstlisting}""")
        key = key[:impl.fastkey_size()]
        print(r"""\begin{lstlisting}[caption={Detailed test vector: m=0, a=0, fast key profile}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b''),binascii.unhexlify(b''))
        print(r"""\end{lstlisting}""")
        key = key[:impl.key_size()]
        print(r"""\begin{lstlisting}[caption={Detailed test vector: m=0, a=0}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b''),binascii.unhexlify(b''))
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Detailed test vector: m=0, a=1}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b''),binascii.unhexlify(b'AA'))
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Detailed test vector: m=1, a=0}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b'DD'),binascii.unhexlify(b''))
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Detailed test vector: m=1, a=1}]""")
        impl.encrypt(key,nonce,binascii.unhexlify(b'DD'),binascii.unhexlify(b'AA'))
        print(r"""\end{lstlisting}""")

        impl.Verbose(DrySponge.SPY_ALG_IO)
        print(r"""\begin{lstlisting}[caption={Test vectors}]""")
        m=binascii.unhexlify(b'')
        for i in range(0,33):
            impl.encrypt(key,nonce,m,bytes([0])*16)
            m+=bytes([i])
        impl.Verbose(DrySponge.SPY_NONE)
        print(r"""\end{lstlisting}

\begin{lstlisting}[caption={Iterative test vector}]""")
        iterations = 100
        print("Encrypting null message %d times with tag feedback as associated data"%iterations)
        m=binascii.unhexlify(b'')
        for i in range(0,iterations):
            m=impl.encrypt(key,nonce,binascii.unhexlify(b''),m)
        print("   CipherText: ",end="")
        DrySponge.print_bytes_as_hex(m)
        print(r"""\end{lstlisting}""")

    def test_hash_mode():
        impl.Verbose(DrySponge.SPY_ALG_IO)
        impl.hash(binascii.unhexlify(b'00'))
        impl.hash(binascii.unhexlify(b'0001'))
        impl.hash(binascii.unhexlify(b'0000'))
        impl.hash(binascii.unhexlify(b'000000'))
        impl.hash(binascii.unhexlify(b'01'))
        impl.hash(binascii.unhexlify(b'02'))
        impl.hash(binascii.unhexlify(b'03'))

    def aead_enc_dec(key,nonce,message=None,ad=None):
        if message is None:
            message = bytearray(binascii.unhexlify(b''))
        c = impl.encrypt(key,nonce,message,ad)
        p = impl.decrypt(key,nonce,c,ad)
        assert(p==message)

    def debug():
        impl.Verbose(DrySponge.SPY_ALG_IO)
        key = binascii.unhexlify(b'00')*impl.key_size()
        nonce = binascii.unhexlify(b'00')*impl.block_size()
        aead_enc_dec(key,nonce)
        aead_enc_dec(key,nonce,binascii.unhexlify(b'00'))
        aead_enc_dec(key,nonce,binascii.unhexlify(b'0001'))
        aead_enc_dec(key,nonce,binascii.unhexlify(b'0000'))
        aead_enc_dec(key,nonce,binascii.unhexlify(b'000000'))
        aead_enc_dec(key,nonce,binascii.unhexlify(b'00000001'))
        #test_hash_mode()
        impl.Verbose(DrySponge.SPY_NONE)
        impl.Verbose(DrySponge.SPY_ALG_IO)
        iterations = 16
        print("Generating expected tag for benchmark on %d iterations"%iterations)
        m=binascii.unhexlify(b'00')*impl.block_size()
        for i in range(0,iterations):
            o=impl.encrypt(key,nonce,m,binascii.unhexlify(b''))
            m=copy.deepcopy(o[impl.block_size():])
        print("   CipherText: ",end="")
        DrySponge.print_bytes_as_hex(o[impl.block_size():])

    #debug()
    gen_aead_test_vectors()
    gen_hash_test_vectors()
