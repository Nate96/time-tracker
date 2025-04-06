#include <time.h>

typedef struct {
   int id;
   char* type[3];
   struct tm punch; 
   char* comment[140];
} punch;
