#include <unistd.h>

int main()
{
	while (1) {

		write(1, "Hello World\n", 13);
	}
}

