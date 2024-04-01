# uint8_t
The uint8_t type is an unsigned integer type that is exactly 8 bits wide. In C and C++, this type is defined in the <stdint.h> header file (or <cstdint> in C++), which is part of the C99 standard. The uint8_t type is used when you need an integer that is guaranteed to be 8 bits in size on any platform. Being unsigned means it can store values from 0 to 255, inclusive.

Here's a quick breakdown:

    uint: Stands for "unsigned integer," meaning it can only represent non-negative values.
    8: Indicates the size of the integer in bits.
    t: Stands for "type."

Using uint8_t and other fixed-width integers (int16_t, uint32_t, etc.) is beneficial when you need precise control over the size of your data, which is particularly important in systems programming, embedded systems, and when interfacing with hardware or network protocols where the exact size of an integer matters for compatibility and efficiency.


# usigned char

unsigned char is a character datatype where the variable consumes all the 8 bits of the memory and there is no sign bit (which is there in signed char). So it means that the range of unsigned char data type ranges from 0 to 255.