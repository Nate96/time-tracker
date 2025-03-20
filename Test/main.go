package main

import (
   "fmt"
   "os"
   "testing")

func main() {
   // os.Args provides access to raw command-line arguments
   args := os.Args

   fmt.Printf("Number of arguments: %d\n", len(args))

   for i, arg := range args {
      fmt.Printf("Argument %d: %s\n", i, arg)
   }
}

