#include <cstring>
void bad_function(char* input) {
    char buffer[50];
    strcpy(buffer, input);
    int* arr = new int[100];
    char* p = (char*)malloc(50);
}
