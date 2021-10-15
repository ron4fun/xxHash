#xxHashC++ Class#


A Python implementation of [xxHash](http://code.google.com/p/xxhash/)


Example
---------


	>>> from xxHas32 import *
	>>>
    >>> hash = xxHash32()
    >>> hash.Init()
    >>> hash.Update("hello", 5)
    >>> hash.Digest() == hash.CalculateHash32("hello", 5)
    True
	>>> 
   

License
----------
    BSD 2-clause license.
        
        