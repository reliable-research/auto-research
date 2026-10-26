#include <assert.h>

#define BOUND 1000

int main(void) {
    int x = 0;
    int i;
    for (i = 0; i < BOUND; i++) {
        if (i % 2 == 0) {
            x += 2;
        } else {
            x += 4;
        }
        assert(x % 2 == 0);
    }
    return 0;
}
