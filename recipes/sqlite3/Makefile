CFLAGS=-DSQLITE_ENABLE_FTS4 -Wno-everything

sqlite3: static
	cp sqlite3.a libsqlite3.a

compile:
	$(CC) $(CFLAGS) -c -o sqlite3.o sqlite3.c
	
static: compile
	$(AR) rc sqlite3.a sqlite3.o
