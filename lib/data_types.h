#include <stdint.h>
#include <iostream>
#include <fstream>
#include <stdio.h>

/**
 * @brief predefined data types for Falcon programming language
 * 
 * These types were chosen with the intent of being compatible with existing c/c++ codebases. 
 * Interger type names were/are inspired by the rust programming language
 *
 **/


/**
 * @brief Signed and unsigned 8-bit integers
 * 
 */

typedef unsigned char u8;
typedef signed char i8; 

/**
 * @brief Signed and unsigned 16-bit integers
 * 
 */
typedef unsigned short u16;
typedef signed short i16; 


/**
 * @brief Signed and unsigned 32-bit integers
 * 
 */
typedef unsigned int u32;
typedef signed int i32; 


/**
 * @brief Signed and unsigned 64-bit integers
 * 
 */
typedef unsigned long long u64;
typedef signed long long i64; 


/**
 * @brief 64-bit and 32-bit floating point real numbers
 * 
 */
typedef double f64; 
typedef float f32; 


/**
 * @brief string type (OOP String for out-of-the-box features)
 * 
 */
typedef std::string string; 


/**
 * @brief File pointer
 * 
 * I chose to use the c version because in c++ we have to use different streams for reading and writing 
 * to files. 
 * 
 */
typedef FILE* file; 


/**
 * @brief null alias for compatability
 * 
 */
#define null (NULL)

