#include <iostream>
#ifdef _WIN32
    #include <windows.h>
#endif
#ifdef __APPLE__
    #include <OpenGl/gl.h>
#else
    #include <GL/gl.h>
#endif

int main()
{
    std::cout << "Bincrafters\n";
    return 0;
}
