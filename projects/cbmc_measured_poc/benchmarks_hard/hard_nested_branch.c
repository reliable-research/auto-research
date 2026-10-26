/* hard_nested_branch.c — nested conditionals inside a symbolic-bound loop
   with array state indexed via nondet offset.
   Invariant: sum == check tracks accumulator across all branch choices. */
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
        int c1 = __VERIFIER_nondet_int();
        int c2 = __VERIFIER_nondet_int();
        int k  = __VERIFIER_nondet_int();
        int v;
        int idx = (i + (k & 31)) & 63;

        if (c1 > 0) {
            if (c2 > 0) {
                v = 5;
            } else {
                v = 10;
            }
        } else {
            if (c2 > 0) {
                v = 15;
            } else {
                v = 20;
            }
        }

        arr[idx] = v;
        sum += arr[idx];
        check += v;

        /* linear invariant: sum matches check across all branch combinations */
        assert(sum == check);
        i++;
    }

    return 0;
}
