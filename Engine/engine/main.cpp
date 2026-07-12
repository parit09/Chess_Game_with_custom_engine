#include <stdint.h>

typedef uint64_t U64;

#define setBit(b,i) ((b) |= (1ULL << (i)))
#define clearBit(b,i) ((b) &= ~(1ULL << (i)))
#define getBit(b,i) ((b) & (1ULL << (i)))
#define getLSB(b) (__builtin_ctzll(b))


int main(){

    return 0;
}