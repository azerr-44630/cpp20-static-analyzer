#include <iostream>
#include <memory>

class Base {
public:
    Base() {}
    ~Base() {}
};

class Vulnerable : public Base {
private:
    int* data;
public:
    Vulnerable() {
        data = std::make_unique<int[]>(100);
    }
    ~Vulnerable() {
    }
};
