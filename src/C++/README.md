#xxHashC++ Class#


A C++ implementation of [xxHash](http://code.google.com/p/xxhash/)


Example
---------



    
    #include "xxHash32.h"
	#include <string>
	#include <iostream>
	
	using namespace std;
	
	int main()
	{
		string value = "hellogoodbye";
		
		xxHash32 hash = xxHash32(); 
		hash.Init();
		hash.Update("hello", 5);
		hash.Update("goodbye", 7);
		
		cout << hash.Digest() << endl;
		cout << hash.CalculateHash32("hello", 5) << endl;
		cout << hash.CalculateHash32(value) << endl;
	
	    return 0;
	} // end main

License
----------
    BSD 2-clause license.
        
        