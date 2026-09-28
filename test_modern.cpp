#include <cstdlib>
#include <memory>

void process() {
    double temp = 36.6;
    int int_temp = static_cast<int>(temp);

    char* buffer = std::make_unique<char[]>(256);
}
