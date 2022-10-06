#ifndef _IO_H_

#include <iostream>
#include <stdio.h>
#include "data_types.h"


/**
 * @brief Input/ Output class for Falcon Programming language
 * 
 * This class the official class for reading and writing to the screen (terminal) and files. 
 * 
 * ** Still a work in progress **
 */
class io {
    public:
    io() {}
    ~io() {}
    
    /**
     * @brief Output method print
     * 
     * @tparam Printable 
     * @param msg 
     * 
     * prints </code> msg </code> to the standard output
     */
    template<typename Printable>
    void print(Printable msg) {
        std::cout << msg ; 
    }

    /**
     * @brief Output method println
     * 
     * @tparam Printable 
     * @param msg 
     * 
     * prints </code> msg </code> and appends a new line
     */
    template<typename Printable>
    void println(Printable msg) {
        print(msg); 
        print("\n");
    }

    /**
     * @brief Input method readI32
     * 
     * @return i32 
     * 
     * reads an i32 integer from the keyboard
     */
    i32 readI32() {
        using namespace std;
        i32 in;
        cin >> in; 
        return in; 
    }


    /**
     * @brief Input method readU32
     * 
     * @return u32 
     */
    u32 readU32() {
        using namespace std;
        u32 in;
        cin >> in; 
        return in; 
    }

    i64 readI64() {
        using namespace std;
        i64 in;
        cin >> in; 
        return in; 
    }

    u64 readU64() {
        using namespace std;
        u64 in;
        cin >> in; 
        return in; 
    }

    i16 readI16() {
        using namespace std;
        i16 in;
        cin >> in; 
        return in; 
    }

    u16 readU16 () {
        using namespace std;
        u16 in;
        cin >> in; 
        return in; 
    }

    i8 readI8() {
        using namespace std;
        i8 in;
        cin >> in; 
        return in; 
    }

    u8 readU8() {
        using namespace std;
        u8 in;
        cin >> in; 
        return in; 
    }

    f32 readF32() {
        using namespace std;
        f32 in;
        cin >> in; 
        return in; 
    }

    f64 readF64() {
        using namespace std;
        f64 in;
        cin >> in; 
        return in; 
    }

    file openFile(string filename, string mode) {
        file filePtr = fopen(filename.c_str(), mode.c_str()); 
        return filePtr; 
    }

    void writeFile(file filePtr, string text) {
        fprintf(filePtr, "%s", text.c_str());
    }

    void closeFile(file filePtr) {
        if (filePtr != null) fclose(filePtr);
    }

    string readFile(file filePtr) {
        fseek(filePtr, 0, SEEK_END);
        i32 size = ftell(filePtr); 
        fseek(filePtr, 0, SEEK_SET);

        char *buffer = (char *) malloc(size * 1); 

        if (buffer == null) {
            return null; 
        }

        fread(buffer, size+1, 1, filePtr); 
        string ret(buffer);
        free(buffer); 
        
        return ret;  
    }
};


//Output io = Output();


#endif // !1
