#include <data_types.h>
#include <vector>
#include <range.h>

#include <io.h>
i32 main(i32 argc, char** argv) {
auto arr = std::vector {std::vector {"Vincent","20"},std::vector {"Vincent","20"},std::vector {"Vincent","20"}};
i32 outer = arr.size ();;
auto first = arr[0];
i32 inner = first.size ();;
for ( auto i: range::range(0,outer - 1)) {
for ( auto j: range::range(0,inner - 1)) {
auto str = arr[i][j];
io().print (i);
io().print (": ");
io().print (str);
io().print (" : ");
io().println (j);
}
}
return 0;
}
