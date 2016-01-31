import ctypes

class XXH_State(object):
    def __init__(self):
        self.total_len = ctypes.c_uint()
        self.seed = ctypes.c_uint()
        self.v1 = ctypes.c_uint()
        self.v2 = ctypes.c_uint()
        self.v3 = ctypes.c_uint()
        self.v4 = ctypes.c_uint()
        self.memsize = ctypes.c_uint()
        self.memory = None
		
class xxHash32(object):
    __PRIME32_1 = 2654435761
    __PRIME32_2 = 2246822519
    __PRIME32_3 = 3266489917
    __PRIME32_4 = 668265263
    __PRIME32_5 = 374761393
	
    def __init__(self):
        pass

    def Init(self, seed = 0):
        """
        Function initialize XXH_State object
        """
        PRIME32_1 = xxHash32.__PRIME32_1
        PRIME32_2 = xxHash32.__PRIME32_2
        PRIME32_3 = xxHash32.__PRIME32_3
        PRIME32_4 = xxHash32.__PRIME32_4
        PRIME32_5 = xxHash32.__PRIME32_5
    
        self._state = XXH_State()
        
        self._state.seed.value = seed
        self._state.v1.value = seed + PRIME32_1 + PRIME32_2
        self._state.v2.value = seed + PRIME32_2
        self._state.v3.value = seed
        self._state.v4.value = seed - PRIME32_1
        self._state.total_len.value = 0
        self._state.memsize.value = 0
        self._state.memory = ctypes.c_buffer("", size=16)

    def Update(self, buf, length):
        try:
            if type(buf) is str:
                buf = ctypes.c_buffer(buf)
            elif type(buf) is bytearray:
                buf = ctypes.c_buffer(buf.decode("ascii"))
            else:
                raise ValueError("buffer must be of type: bytearray or str")
        except:
            raise ValueError("buffer must be of type: bytearray or str")
        
        _state = self._state
        
        PRIME32_1 = xxHash32.__PRIME32_1
        PRIME32_2 = xxHash32.__PRIME32_2
        PRIME32_3 = xxHash32.__PRIME32_3
        PRIME32_4 = xxHash32.__PRIME32_4
        PRIME32_5 = xxHash32.__PRIME32_5

        index = ctypes.c_int(0)
        indexPtr = ctypes.pointer(index)
	
        _state.total_len.value += length
        if _state.memsize.value + length < 16:
            memPtr = ctypes.byref(_state.memory, _state.memsize.value)
            ctypes.memmove(memPtr, buf, length)
            _state.memsize.value += length
        
            return True

        if (_state.memsize.value > 0):
            memPtr = ctypes.byref(_state.memory, _state.memsize.value)

            ctypes.memmove(memPtr, buf, 16 - _state.memsize.value)
            _state.v1.value = self.CalcSubHash(_state.v1, _state.memory, indexPtr)
            index.value += 4
            _state.v2.value = self.CalcSubHash(_state.v2, _state.memory, indexPtr)
            index.value += 4
            _state.v3.value = self.CalcSubHash(_state.v3, _state.memory, indexPtr)
            index.value += 4
            _state.v4.value = self.CalcSubHash(_state.v4, _state.memory, indexPtr)
            index.value += 4

            index.value = 0
            _state.memsize.value = 0

        if (index.value <= length - 16):
            limit = length - 16
            v1 = _state.v1
            v2 = _state.v2
            v3 = _state.v3
            v4 = _state.v4

            v1.value = self.CalcSubHash(v1, buf, indexPtr)            
            index.value += 4
            v2.value = self.CalcSubHash(v2, buf, indexPtr)
            index.value += 4
            v3.value = self.CalcSubHash(v3, buf, indexPtr)
            index.value += 4
            v4.value = self.CalcSubHash(v4, buf, indexPtr)
            index.value += 4
            while (index.value <= limit):
                v1.value = self.CalcSubHash(v1, buf, indexPtr)
                index.value += 4
                v2.value = self.CalcSubHash(v2, buf, indexPtr)
                index.value += 4
                v3.value = self.CalcSubHash(v3, buf, indexPtr)
                index.value += 4
                v4.value = self.CalcSubHash(v4, buf, indexPtr)
                index.value += 4
                
            _state.v1.value = v1.value
            _state.v2.value = v2.value
            _state.v3.value = v3.value
            _state.v4.value = v4.value
        
        if (index.value < length):
            memPtr = ctypes.byref(buf, index.value)

            ctypes.memmove(_state.memory, memPtr, length - index.value)
            _state.memsize.value = length - index.value

        return True
       
    def Digest(self):
        h32 = ctypes.c_uint()

        _state = self._state
        
        PRIME32_1 = xxHash32.__PRIME32_1
        PRIME32_2 = xxHash32.__PRIME32_2
        PRIME32_3 = xxHash32.__PRIME32_3
        PRIME32_4 = xxHash32.__PRIME32_4
        PRIME32_5 = xxHash32.__PRIME32_5
        
        index = ctypes.c_int(0)
        indexPtr = ctypes.pointer(index)

        if (_state.total_len.value >= 16):
            h32.value = self.RotateLeft(_state.v1.value, 1) + self.RotateLeft(_state.v2.value, 7) + self.RotateLeft(_state.v3.value, 12) + self.RotateLeft(_state.v4.value, 18)
        else:
            h32.value = _state.seed.value + PRIME32_5

        h32.value += _state.total_len.value

        while (index.value + 4 <= _state.memsize.value):
            val = ctypes.c_int(0)
            valPtr = ctypes.pointer(val)

            memPtr = ctypes.byref(_state.memory, index.value)
            
            ctypes.memmove(valPtr, memPtr, 4)
            h32.value += (val.value * PRIME32_3)
            h32.value = self.RotateLeft(h32.value, 17) * PRIME32_4
            index.value += 4
        
        while (index.value < _state.memsize.value):
            h32.value += (ord(_state.memory.value[index.value]) * PRIME32_5)
            h32.value = self.RotateLeft(h32.value, 11) * PRIME32_1
            index.value += 1

        h32.value ^= h32.value >> 15;
        h32.value *= PRIME32_2;
        h32.value ^= h32.value >> 13;
        h32.value *= PRIME32_3;
        h32.value ^= h32.value >> 16;

        return h32.value

    def CalculateHash32(self, buf, length, seed=0):
        try:
            if type(buf) is str:
                buf = ctypes.c_buffer(buf)
            elif type(buf) is bytearray:
                buf = ctypes.c_buffer(buf.decode("ascii"))
            else:
                raise ValueError("buffer must be of type: bytearray or str")
        except:
            raise ValueError("buffer must be of type: bytearray or str")
        
        h32 = ctypes.c_uint()

        _state = self._state
        
        PRIME32_1 = xxHash32.__PRIME32_1
        PRIME32_2 = xxHash32.__PRIME32_2
        PRIME32_3 = xxHash32.__PRIME32_3
        PRIME32_4 = xxHash32.__PRIME32_4
        PRIME32_5 = xxHash32.__PRIME32_5
        
        index = ctypes.c_int(0)
        indexPtr = ctypes.pointer(index)
        
        if (length < 0):
            raise ValueError("No len value inputed")

        if (length >= 16):
            limit = length - 16
            v1 = ctypes.c_uint(seed + PRIME32_1 + PRIME32_2)
            v2 = ctypes.c_uint(seed + PRIME32_2)
            v3 = ctypes.c_uint(seed)
            v4 = ctypes.c_uint(seed - PRIME32_1)
            
            v1.value = self.CalcSubHash(v1, buf, indexPtr)
            index.value += 4
            v2.value = self.CalcSubHash(v2, buf, indexPtr)
            index.value += 4
            v3.value = self.CalcSubHash(v3, buf, indexPtr)
            index.value += 4
            v4.value = self.CalcSubHash(v4, buf, indexPtr)
            index.value += 4
            while (index.value <= limit):
                v1.value = self.CalcSubHash(v1, buf, indexPtr)
                index.value += 4
                v2.value = self.CalcSubHash(v2, buf, indexPtr)
                index.value += 4
                v3.value = self.CalcSubHash(v3, buf, indexPtr)
                index.value += 4
                v4.value = self.CalcSubHash(v4, buf, indexPtr)
                index.value += 4

            h32.value = self.RotateLeft(v1.value, 1) + self.RotateLeft(v2.value, 7) + self.RotateLeft(v3.value, 12) + self.RotateLeft(v4.value, 18)
           
        else:
            h32.value = seed + PRIME32_5

        h32.value += length
    
        while (index.value <= length - 4):
            val = ctypes.c_int(0)
            valPtr = ctypes.pointer(val)

            memPtr = ctypes.byref(buf, index.value)
            
            ctypes.memmove(valPtr, memPtr, 4)
            h32.value += (val.value * PRIME32_3)
            h32.value = self.RotateLeft(h32.value, 17) * PRIME32_4
            index.value += 4

        while (index.value < length):
            h32.value += (ord(buf.value[index.value]) * PRIME32_5)
            h32.value = self.RotateLeft(h32.value, 11) * PRIME32_1
            index.value += 1

        h32.value ^= h32.value >> 15;
        h32.value *= PRIME32_2;
        h32.value ^= h32.value >> 13;
        h32.value *= PRIME32_3;
        h32.value ^= h32.value >> 16;

        return h32.value

    def RotateLeft(self, value, count):
        return (value << count) | (value >> (32 - count))

    def CalcSubHash(self, val, buf, indexPtr):
        read_value = ctypes.c_uint(0)
        read_valuePtr = ctypes.pointer(read_value)
    
        memPtr = ctypes.byref(buf, indexPtr.contents.value)
        ctypes.memmove(read_valuePtr, memPtr, 4)
        
        val.value += (read_value.value * xxHash32.__PRIME32_2)
        val.value = self.RotateLeft(val.value, 13)
        val.value *= xxHash32.__PRIME32_1
        return val.value

    def bytesToUInt32(self, byte_array, indexPtr):
        n = ctypes.c_uint32(0)
        nPtr = ctypes.pointer(n)

        memPtr = ctypes.byref(byte_array, indexPtr.contents.value)
        
        ctypes.memmove(nPtr, memPtr, 4)
        return n
    

if __name__ == "__main__":
    pass
