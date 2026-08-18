#include "../includes/types.hpp"

namespace chess {
    ll blackScore = 0LL;
    ll whiteScore = 0LL;
    
	class StartingBitboards {
        int pawnPoints = 1;
        int rookPoints = 5;
        int bishopKnightPoints = 3;
        int queenPoints = 9;

		U64 whitePawns = 0x000000000000FF00ULL;
		U64 whiteKnights = 0x0000000000000042ULL;
		U64 whiteBishops = 0x0000000000000024ULL;
		U64 whiteRooks = 0x0000000000000081ULL;
		U64 whiteQueen = 0x0000000000000008ULL;
		U64 whiteKing = 0x0000000000000010ULL;

		U64 blackPawns = 0x00FF000000000000ULL;
		U64 blackKnights = 0x4200000000000000ULL;
		U64 blackBishops = 0x2400000000000000ULL;
		U64 blackRooks = 0x8100000000000000ULL;
		U64 blackQueen = 0x0800000000000000ULL;
		U64 blackKing = 0x1000000000000000ULL;

		U64 whitePieces = whitePawns | whiteKnights | whiteBishops | whiteRooks | whiteQueen | whiteKing;
		U64 blackPieces = blackPawns | blackKnights | blackBishops | blackRooks | blackQueen | blackKing;
		U64 occupied = whitePieces | blackPieces;
	};



}