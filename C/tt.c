#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
   // argc: argument count
   // argv: argument vector (array of strings)

   if (argc == 0) {
      printf("ERROR or Status");
   }

   if (strcmp(argv[1], "i") == 0) {
      int res;

      switch (res) {
         case -1:
            printf("No Database");
            break;
         case 0:
            printf("Already Punched in");
            break;
         case 1:
            printf("Punched in Success");
            break;
      }
   } else if (strcmp(argv[1], "o") == 0) {
      int res;

      switch (res) {
         case -1:
            printf("No Database");
            break;
         case 0:
            printf("Already Punched in");
            break;
         case 1:
            printf("Punched in Success");
            break;
      }
   } else if (strcmp(argv[1], "status") == 0)  {
      printf("Status");
   } else if (strcmp(argv[1], "report") == 0)  {
      printf("report");
   } else {
      printf("ERROR Invalid input, please refer to README for more information");
   }
} 

//   switch (*argv[1]) {
//      case "i":
//         printf("punch in");
//         break;
//      case "o":
//            printf("punch out");
//            break;
//      case "status":
//            printf("punch out");
//            break;
//      default:
//         printf("ERROR: invalid input, refer to README.md");
//   }
   
