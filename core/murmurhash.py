def hash32(key: str, seed=0x0):
    ''' 32位 murmur3 实现 '''

    key = bytearray(key.encode())

    def fmix(h):
        h ^= h >> 16
        h = (h * 0x85ebca6b) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0xc2b2ae35) & 0xFFFFFFFF
        h ^= h >> 16
        return h

    length = len(key)
    nblocks = int(length / 4)

    h1 = seed

    c1 = 0xcc9e2d51
    c2 = 0x1b873593


    for block_start in range(0, nblocks * 4, 4):

        k1 = key[block_start + 3] << 24 | \
             key[block_start + 2] << 16 | \
             key[block_start + 1] << 8 | \
             key[block_start + 0]

        k1 = (c1 * k1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  
        k1 = (c2 * k1) & 0xFFFFFFFF

        h1 ^= k1
        h1 = (h1 << 13 | h1 >> 19) & 0xFFFFFFFF  
        h1 = (h1 * 5 + 0xe6546b64) & 0xFFFFFFFF

    tail_index = nblocks * 4
    k1 = 0
    tail_size = length & 3

    if tail_size >= 3:
        k1 ^= key[tail_index + 2] << 16
    if tail_size >= 2:
        k1 ^= key[tail_index + 1] << 8
    if tail_size >= 1:
        k1 ^= key[tail_index + 0]

    if tail_size > 0:
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  
        k1 = (k1 * c2) & 0xFFFFFFFF
        h1 ^= k1

    
    unsigned_val = fmix(h1 ^ length)
    if unsigned_val & 0x80000000 == 0:
        return unsigned_val
    else:
        return -((unsigned_val ^ 0xFFFFFFFF) + 1)


def hash64(key, seed=0x0, x64arch=True):
    """ 64位 murmur3 实现 ,返回两个64位int"""

    hash_128 = hash128(key, seed, x64arch)

    unsigned_val1 = hash_128 & 0xFFFFFFFFFFFFFFFF
    if unsigned_val1 & 0x8000000000000000 == 0:
        signed_val1 = unsigned_val1
    else:
        signed_val1 = -((unsigned_val1 ^ 0xFFFFFFFFFFFFFFFF) + 1)

    unsigned_val2 = (hash_128 >> 64) & 0xFFFFFFFFFFFFFFFF
    if unsigned_val2 & 0x8000000000000000 == 0:
        signed_val2 = unsigned_val2
    else:
        signed_val2 = -((unsigned_val2 ^ 0xFFFFFFFFFFFFFFFF) + 1)

    return (int(signed_val1), int(signed_val2))


def hash128(key, seed=0x0, x64arch=True):
    """ 128位 murmur3 实现 """

    def hash128_x64(key, seed):
        def fmix(k):
            k ^= k >> 33
            k = (k * 0xff51afd7ed558ccd) & 0xFFFFFFFFFFFFFFFF
            k ^= k >> 33
            k = (k * 0xc4ceb9fe1a85ec53) & 0xFFFFFFFFFFFFFFFF
            k ^= k >> 33
            return k

        length = len(key)
        nblocks = int(length / 16)

        h1 = seed
        h2 = seed

        c1 = 0x87c37b91114253d5
        c2 = 0x4cf5ad432745937f


        for block_start in range(0, nblocks * 8, 8):

            k1 = key[2 * block_start + 7] << 56 | \
                 key[2 * block_start + 6] << 48 | \
                 key[2 * block_start + 5] << 40 | \
                 key[2 * block_start + 4] << 32 | \
                 key[2 * block_start + 3] << 24 | \
                 key[2 * block_start + 2] << 16 | \
                 key[2 * block_start + 1] << 8 | \
                 key[2 * block_start + 0]

            k2 = key[2 * block_start + 15] << 56 | \
                 key[2 * block_start + 14] << 48 | \
                 key[2 * block_start + 13] << 40 | \
                 key[2 * block_start + 12] << 32 | \
                 key[2 * block_start + 11] << 24 | \
                 key[2 * block_start + 10] << 16 | \
                 key[2 * block_start + 9] << 8 | \
                 key[2 * block_start + 8]

            k1 = (c1 * k1) & 0xFFFFFFFFFFFFFFFF
            k1 = (k1 << 31 | k1 >> 33) & 0xFFFFFFFFFFFFFFFF  
            k1 = (c2 * k1) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1

            h1 = (h1 << 27 | h1 >> 37) & 0xFFFFFFFFFFFFFFFF  
            h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
            h1 = (h1 * 5 + 0x52dce729) & 0xFFFFFFFFFFFFFFFF

            k2 = (c2 * k2) & 0xFFFFFFFFFFFFFFFF
            k2 = (k2 << 33 | k2 >> 31) & 0xFFFFFFFFFFFFFFFF  
            k2 = (c1 * k2) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2

            h2 = (h2 << 31 | h2 >> 33) & 0xFFFFFFFFFFFFFFFF  
            h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
            h2 = (h2 * 5 + 0x38495ab5) & 0xFFFFFFFFFFFFFFFF


        tail_index = nblocks * 16
        k1 = 0
        k2 = 0
        tail_size = length & 15

        if tail_size >= 15:
            k2 ^= key[tail_index + 14] << 48
        if tail_size >= 14:
            k2 ^= key[tail_index + 13] << 40
        if tail_size >= 13:
            k2 ^= key[tail_index + 12] << 32
        if tail_size >= 12:
            k2 ^= key[tail_index + 11] << 24
        if tail_size >= 11:
            k2 ^= key[tail_index + 10] << 16
        if tail_size >= 10:
            k2 ^= key[tail_index + 9] << 8
        if tail_size >= 9:
            k2 ^= key[tail_index + 8]

        if tail_size > 8:
            k2 = (k2 * c2) & 0xFFFFFFFFFFFFFFFF
            k2 = (k2 << 33 | k2 >> 31) & 0xFFFFFFFFFFFFFFFF 
            k2 = (k2 * c1) & 0xFFFFFFFFFFFFFFFF
            h2 ^= k2

        if tail_size >= 8:
            k1 ^= key[tail_index + 7] << 56
        if tail_size >= 7:
            k1 ^= key[tail_index + 6] << 48
        if tail_size >= 6:
            k1 ^= key[tail_index + 5] << 40
        if tail_size >= 5:
            k1 ^= key[tail_index + 4] << 32
        if tail_size >= 4:
            k1 ^= key[tail_index + 3] << 24
        if tail_size >= 3:
            k1 ^= key[tail_index + 2] << 16
        if tail_size >= 2:
            k1 ^= key[tail_index + 1] << 8
        if tail_size >= 1:
            k1 ^= key[tail_index + 0]

        if tail_size > 0:
            k1 = (k1 * c1) & 0xFFFFFFFFFFFFFFFF
            k1 = (k1 << 31 | k1 >> 33) & 0xFFFFFFFFFFFFFFFF  
            k1 = (k1 * c2) & 0xFFFFFFFFFFFFFFFF
            h1 ^= k1


        h1 ^= length
        h2 ^= length

        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF

        h1 = fmix(h1)
        h2 = fmix(h2)

        h1 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF
        h2 = (h1 + h2) & 0xFFFFFFFFFFFFFFFF

        return (h2 << 64 | h1)

    def hash128_x86(key, seed):
        def fmix(h):
            h ^= h >> 16
            h = (h * 0x85ebca6b) & 0xFFFFFFFF
            h ^= h >> 13
            h = (h * 0xc2b2ae35) & 0xFFFFFFFF
            h ^= h >> 16
            return h

        length = len(key)
        nblocks = int(length / 16)

        h1 = seed
        h2 = seed
        h3 = seed
        h4 = seed

        c1 = 0x239b961b
        c2 = 0xab0e9789
        c3 = 0x38b34ae5
        c4 = 0xa1e38b93


        for block_start in range(0, nblocks * 16, 16):
            k1 = key[block_start + 3] << 24 | \
                 key[block_start + 2] << 16 | \
                 key[block_start + 1] << 8 | \
                 key[block_start + 0]

            k2 = key[block_start + 7] << 24 | \
                 key[block_start + 6] << 16 | \
                 key[block_start + 5] << 8 | \
                 key[block_start + 4]

            k3 = key[block_start + 11] << 24 | \
                 key[block_start + 10] << 16 | \
                 key[block_start + 9] << 8 | \
                 key[block_start + 8]

            k4 = key[block_start + 15] << 24 | \
                 key[block_start + 14] << 16 | \
                 key[block_start + 13] << 8 | \
                 key[block_start + 12]

            k1 = (c1 * k1) & 0xFFFFFFFF
            k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  
            k1 = (c2 * k1) & 0xFFFFFFFF
            h1 ^= k1

            h1 = (h1 << 19 | h1 >> 13) & 0xFFFFFFFF  
            h1 = (h1 + h2) & 0xFFFFFFFF
            h1 = (h1 * 5 + 0x561ccd1b) & 0xFFFFFFFF

            k2 = (c2 * k2) & 0xFFFFFFFF
            k2 = (k2 << 16 | k2 >> 16) & 0xFFFFFFFF  
            k2 = (c3 * k2) & 0xFFFFFFFF
            h2 ^= k2

            h2 = (h2 << 17 | h2 >> 15) & 0xFFFFFFFF  
            h2 = (h2 + h3) & 0xFFFFFFFF
            h2 = (h2 * 5 + 0x0bcaa747) & 0xFFFFFFFF

            k3 = (c3 * k3) & 0xFFFFFFFF
            k3 = (k3 << 17 | k3 >> 15) & 0xFFFFFFFF  
            k3 = (c4 * k3) & 0xFFFFFFFF
            h3 ^= k3

            h3 = (h3 << 15 | h3 >> 17) & 0xFFFFFFFF  
            h3 = (h3 + h4) & 0xFFFFFFFF
            h3 = (h3 * 5 + 0x96cd1c35) & 0xFFFFFFFF

            k4 = (c4 * k4) & 0xFFFFFFFF
            k4 = (k4 << 18 | k4 >> 14) & 0xFFFFFFFF 
            k4 = (c1 * k4) & 0xFFFFFFFF
            h4 ^= k4

            h4 = (h4 << 13 | h4 >> 19) & 0xFFFFFFFF 
            h4 = (h1 + h4) & 0xFFFFFFFF
            h4 = (h4 * 5 + 0x32ac3b17) & 0xFFFFFFFF


        tail_index = nblocks * 16
        k1 = 0
        k2 = 0
        k3 = 0
        k4 = 0
        tail_size = length & 15

        if tail_size >= 15:
            k4 ^= key[tail_index + 14] << 16
        if tail_size >= 14:
            k4 ^= key[tail_index + 13] << 8
        if tail_size >= 13:
            k4 ^= key[tail_index + 12]

        if tail_size > 12:
            k4 = (k4 * c4) & 0xFFFFFFFF
            k4 = (k4 << 18 | k4 >> 14) & 0xFFFFFFFF  
            k4 = (k4 * c1) & 0xFFFFFFFF
            h4 ^= k4

        if tail_size >= 12:
            k3 ^= key[tail_index + 11] << 24
        if tail_size >= 11:
            k3 ^= key[tail_index + 10] << 16
        if tail_size >= 10:
            k3 ^= key[tail_index + 9] << 8
        if tail_size >= 9:
            k3 ^= key[tail_index + 8]

        if tail_size > 8:
            k3 = (k3 * c3) & 0xFFFFFFFF
            k3 = (k3 << 17 | k3 >> 15) & 0xFFFFFFFF  
            k3 = (k3 * c4) & 0xFFFFFFFF
            h3 ^= k3

        if tail_size >= 8:
            k2 ^= key[tail_index + 7] << 24
        if tail_size >= 7:
            k2 ^= key[tail_index + 6] << 16
        if tail_size >= 6:
            k2 ^= key[tail_index + 5] << 8
        if tail_size >= 5:
            k2 ^= key[tail_index + 4]

        if tail_size > 4:
            k2 = (k2 * c2) & 0xFFFFFFFF
            k2 = (k2 << 16 | k2 >> 16) & 0xFFFFFFFF  
            k2 = (k2 * c3) & 0xFFFFFFFF
            h2 ^= k2

        if tail_size >= 4:
            k1 ^= key[tail_index + 3] << 24
        if tail_size >= 3:
            k1 ^= key[tail_index + 2] << 16
        if tail_size >= 2:
            k1 ^= key[tail_index + 1] << 8
        if tail_size >= 1:
            k1 ^= key[tail_index + 0]

        if tail_size > 0:
            k1 = (k1 * c1) & 0xFFFFFFFF
            k1 = (k1 << 15 | k1 >> 17) & 0xFFFFFFFF  
            k1 = (k1 * c2) & 0xFFFFFFFF
            h1 ^= k1

        
        h1 ^= length
        h2 ^= length
        h3 ^= length
        h4 ^= length

        h1 = (h1 + h2) & 0xFFFFFFFF
        h1 = (h1 + h3) & 0xFFFFFFFF
        h1 = (h1 + h4) & 0xFFFFFFFF
        h2 = (h1 + h2) & 0xFFFFFFFF
        h3 = (h1 + h3) & 0xFFFFFFFF
        h4 = (h1 + h4) & 0xFFFFFFFF

        h1 = fmix(h1)
        h2 = fmix(h2)
        h3 = fmix(h3)
        h4 = fmix(h4)

        h1 = (h1 + h2) & 0xFFFFFFFF
        h1 = (h1 + h3) & 0xFFFFFFFF
        h1 = (h1 + h4) & 0xFFFFFFFF
        h2 = (h1 + h2) & 0xFFFFFFFF
        h3 = (h1 + h3) & 0xFFFFFFFF
        h4 = (h1 + h4) & 0xFFFFFFFF

        return (h4 << 96 | h3 << 64 | h2 << 32 | h1)

    temp = key.encode()
    key = bytearray(temp)

    if x64arch:
        return hash128_x64(key, seed)
    else:
        return hash128_x86(key, seed)


def hash_bytes(key, seed=0x0, x64arch=True):
    """ 128位实现bytes版"""

    hash_128 = hash128(key, seed, x64arch)

    bytestring = ''

    for i in range(0, 16, 1):
        lsbyte = hash_128 & 0xFF
        bytestring = bytestring + str(chr(lsbyte))
        hash_128 = hash_128 >> 8

    return bytestring


if __name__ == '__main__':
    print(hash128('hello world'))
