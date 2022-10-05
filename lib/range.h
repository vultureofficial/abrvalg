#ifndef _RANGE_H_

namespace range {
    #include <vector>
    #include <stdexcept>
    #include <iostream>

    template <typename IntType>
    std::vector<IntType> range(IntType start, IntType stop, IntType step)
    {
    if (step == IntType(0))
    {
        throw std::invalid_argument("step for range must be non-zero");
    }

    std::vector<IntType> result;
    IntType i = start;
    while ((step > 0) ? (i < stop) : (i > stop))
    {
        result.push_back(i);
        i += step;
    }

    return result;
    }

    template <typename IntType>
    std::vector<IntType> range(IntType start, IntType stop)
    {
        if (start > stop) return range(start, stop - IntType(1), IntType(-1)); //for i in 200...0:
        return range(start, stop + IntType(1), IntType(1));
    }

    template <typename IntType>
    std::vector<IntType> range(IntType stop)
    {
    return range(IntType(0), stop, IntType(1));
    }

/*

for i in 0..100:
    io::println(i)

for i in 100..0:
    io::println(i)


for (auto i: range(1, 100)) {
    io().println((i));
}

*/
}

#endif //_RANGE_H_