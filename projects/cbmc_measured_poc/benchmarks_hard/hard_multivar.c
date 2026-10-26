/* hard_multivar.c — four interacting int accumulators updated via nondet
   choices, with symbolic array reads.  Invariant: a + b + c + d == 10 * i. */
#include <assert.h>

int __VERIFIER_nondet_int(void);

int main(void) {
    int arr[64];
    int n = __VERIFIER_nondet_int();
    int a = 0, b = 0, c = 0, d = 0;
    int i = 0;

    if (n < 1 || n > 49) return 0;

    while (i < n) {
        int sel = __VERIFIER_nondet_int();
        int k   = __VERIFIER_nondet_int();
        int idx = k & 63;

        arr[idx] = 10;            /* write constant via nondet index */

        if (sel > 0) {
            a += arr[idx];        /* reads arr[idx] which is 10 */
        } else if (sel < -10) {
            b += arr[idx];
        } else if (sel == 0) {
            c += arr[idx];
        } else {
            d += arr[idx];
        }

        /* linear invariant: all four paths add 10 total */
        assert(a + b + c + d == 10 * (i + 1));
        i++;
    }

    return 0;
}
