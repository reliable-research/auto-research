#include <assert.h>

#define BOUND 1000

int main(void) {
    long sum = 0;
    int i;
    for (i = 1; i <= BOUND; i++) {
        sum += i;
        assert(sum >= 0);
    }
    return 0;
}
