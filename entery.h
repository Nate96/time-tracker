#include <time.h>

typedef struct{
   int id;
   struct tm in_punch; 
   struct tm out_punch; 
   char* title[140];
   char* comment[140];
} entry;
