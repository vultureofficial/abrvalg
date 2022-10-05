#include <data_types.h>
#include <vector>
#include <range.h>


#include <io.h>
int main(i32 argc, i8** argv) {
file filePtr = io().openFile ("testing2.txt" , "r");;
string contents = io().readFile (filePtr);;
io().println (contents);
io().closeFile (filePtr);
return 0;
}
