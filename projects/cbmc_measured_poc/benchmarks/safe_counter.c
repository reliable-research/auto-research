#include <assert.h>

#define BOUND 1000

int main(void) {
    int counter;
    for (counter = 0; counter < BOUND; counter++) {
        assert(counter <= BOUND);
    }
    return 0;
}
