#include <assert.h>

#define BOUND 1000

int main(void) {
    int i;
    for (i = 0; i < BOUND; i++) {
        /* Fails specifically on the last iteration when i == BOUND - 1 */
        assert(i < BOUND - 1);
    }
    return 0;
}
