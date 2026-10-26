#include <assert.h>

#define BOUND 1000

int main(void) {
    int acc = 0;
    int i;
    for (i = 0; i < BOUND; i++) {
        acc += 2;
        /* Violates assertion when acc exceeds BOUND */
        assert(acc <= BOUND);
    }
    return 0;
}
