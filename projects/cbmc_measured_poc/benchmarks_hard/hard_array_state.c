/* hard_array_state.c — symbolic writes to arr[64] at nondet positions;
   invariant: every written cell equals the last value assigned to it,
   so reading arr[idx] right after writing v gives v → sum tracks check. */
#include <assert.h>

int __VERIFIER_nondet_int(void);

int main(void) {
    int arr[64];
    int n = __VERIFIER_nondet_int();
    int written = 0;
    int read_back = 0;
    int i = 0;

    if (n < 1 || n > 49) return 0;

    while (i < n) {
        int v  = __VERIFIER_nondet_int() & 1023;  /* bounded: keeps the only
                                                     refutable property the invariant,
                                                     not signed overflow */
        int k  = __VERIFIER_nondet_int();
        int idx = k & 63;                /* safe: always in [0,63] */
        arr[idx] = v;
        read_back += arr[idx];           /* must equal v */
        written   += v;
        i++;
    }

    /* linear invariant: read_back == written */
    assert(read_back == written);
    return 0;
}
