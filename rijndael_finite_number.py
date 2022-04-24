"""
rijndael_finite_number
https://en.wikipedia.org/wiki/Finite_field_arithmetic#:~:text=a%20finite%20field.-,Rijndael's%20(AES)%20finite%20field,x3%20%2B%20x%20%2B%201.
Understanding Cryptography: A Textbook for Students and Practitioners
"""

class RijndaelFiniteNumber(int):
    def __init__(self, value):
        super().__init__()
        self = value ^ 0xFF
    
    def __op1(self, __x):
        return RijndaelFiniteNumber(int(self) ^ int(__x))
    
    def __op2(self, __x):
        res = 0
        a = int(self)
        b = int(__x)
        while a != 0 and b != 0:
            if (b & 1) != 0:
                res ^= a
            if a & 0x80:
                a = (a << 1) ^ 0x11B
            else:
                a <<= 1
            b >>= 1
        return RijndaelFiniteNumber(res)
    
    def __add__(self, __x):
        return self.__op1(__x)

    def __radd__(self, __x):
        return self.__op1(__x)

    def __iadd__(self, __x):
        self = self.__op1(__x)
        return self
        
    def __sub__(self, __x):
        return self.__op1(__x)
    
    def __rsub__(self, __x):
        return self.__op1(__x)

    def __isub__(self, __x):
        self = self.__op1(__x)
        return self
  
    def __mul__(self, __x):
        return self.__op2(__x)
    
    def __rmul__(self, __x):
        return self.__op2(__x)

    def __imul__(self, __x):
        self = self.__op2(__x)
        return self
    
    def __xor__(self, __n):
        return self.__op1(__n)

    def __rxor__(self, __n):
        return self.__op1(__n)

    def __ixor__(self, __n):
        self = self.__op1(__n)
        return self
    
    def __index__(self) -> int:
        return int(self)
    
    def __int__(self) -> int:
        return super().__int__()
    
    def __str__(self) -> str:
        return f"'{hex(int(self))}'"
    
    def __repr__(self) -> str:
        return f"'{hex(int(self))}'"


