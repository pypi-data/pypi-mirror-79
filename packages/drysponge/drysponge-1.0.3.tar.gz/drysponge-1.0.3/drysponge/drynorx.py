
import binascii
import copy

if __name__ == "__main__":
    from base import DrySponge
    from norx import Norx
    from feistel_rxr import FeistelRxrPX
else:
    from drysponge.base import DrySponge
    from drysponge.norx import Norx
    from drysponge.feistel_rxr import FeistelRxrPX

class DryNorx(object):
    def __init__(self,key_min_width=128,nonce_width=128,rate_width=64,capacity_width=512,init_rounds=8,rounds = 4,final_rounds=8):
        assert(0==(capacity_width%64))
        self.nw = capacity_width // 64
        self.norxwidth = capacity_width // 16
        assert(self.norxwidth in [32, 64])
        self.InitRounds = init_rounds
        self.Rounds = rounds
        self.FinalRounds = final_rounds
        self.MinKeyWidth = key_min_width
        self.NonceWidth = nonce_width
        self.RateWidth = rate_width
        self.CapacityWidth = capacity_width
        x = [0xe5e445df,0xc8a21cd1,0xbf9a6c59,0xaa5748b7]
        self.pw = (rate_width+9) // 10
        self.xw = 1
        assert((self.pw+self.xw)*64<=capacity_width)
        self.frxrpx = FeistelRxrPX(64,2,x,self.pw,1)

    @staticmethod
    def DryNorx32_128():
        return DryNorx(128,128,64,512,8,4)

    @staticmethod
    def DryNorx32():
        return DryNorx(256,128,64,512)

    @staticmethod
    def DryNorx64():
        return DryNorx(256,128,128,1024)

    def instance(self):
        return DrySponge(self.MinKeyWidth,self.NonceWidth,self.RateWidth,self.CapacityWidth,self.MixPhase,self.InitRounds,self.Rounds,self.FinalRounds,self.CoreRound)

    def MixPhase(self,c,i):
        work = DrySponge.bytes_to_int(c[0:(self.pw+self.xw)*8])
        ii =   DrySponge.bytes_to_int(i)
        work = self.frxrpx.apply(work,ii)
        c[0:(self.pw+self.xw)*8] = DrySponge.int_to_bytes(work,(self.pw+self.xw)*64)
        return c

    def CoreRound(self,c,rounds,round):
        S = [0]*16
        bytewidth = self.norxwidth // 8
        for i in range(0,16):
            S[i] = DrySponge.bytes_to_int(c[i*bytewidth:(i+1)*bytewidth])
        impl = Norx(self.norxwidth,rounds)
        impl.round(S,round)
        for i in range(0,16):
            c[i*bytewidth:(i+1)*bytewidth] = DrySponge.int_to_bytes(S[i],self.norxwidth)
        return c

if __name__ == "__main__":
    impl = DryNorx().instance()
    def gen_hash_test_vectors():
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
        impl.Verbose(DrySponge.SPY_F_IO)
        key = binascii.unhexlify(b'000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F')[0:impl.key_size()]
        nonce = binascii.unhexlify(b'202122232425262728292A2B2C2D2E2F')[0:impl.nonce_size()]
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
        nonce = binascii.unhexlify(b'00')*impl.nonce_size()
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
