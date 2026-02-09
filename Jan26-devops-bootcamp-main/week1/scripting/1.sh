## Command line args and exit code
#! /bin/bash

echo "script running is $0"
echo "Total argument are -> $#"
echo " first argument -> $1 second -> $2  thrird -> $3"
echo "list of  argument -> $@"

exit 1


# r -> read (4) w -> (2)  -> x (1)
# -rwxrwxrwx
# ---(user) ---(group)---(other)

# 1>/dev/null -> 
# 