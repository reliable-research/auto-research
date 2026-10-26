#include <assert.h>

int __VERIFIER_nondet_int(void);

int main(void) {
    int arr[64];
    int n = __VERIFIER_nondet_int();
    int sum = 0;
    int check = 0;
    int i = 0;

    if (n < 1 || n > 49) return 0;

    while (i < n) {
        int v = __VERIFIER_nondet_int() & 1023;   /* bounded: keeps the only
                                                     refutable property the invariant,
                                                     not signed overflow */
        int offset = __VERIFIER_nondet_int();
        int idx = (i + (offset & 31)) & 63;
        arr[idx] = v;
        sum += arr[idx];
        check += v;
        i++;
    }

    assert(sum == check);
    return 0;
}
