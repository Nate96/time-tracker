.PHONY: install

help:
	@echo "comp: Compile the main program"
	@echo "test: Compile and run the test program"

comp:
	gcc -o tt main.c

test:
	gcc -0 test test.c
	./test
