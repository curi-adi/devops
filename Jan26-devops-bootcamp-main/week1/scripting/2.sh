# conditionals
#!/bin/bash

if [ ! -f "$1" ]; then
    echo "file dont exists"
    exit 1
fi

# echo " zipping the log file $1"
# zip   "$1.zip" "$1" >/dev/null 2>&1
# cat /dev/null > "$1"
# touch "$1"


echo " zipping the log file $1"
zip "$1.$(date +%s).zip" "$1" >/dev/null 2>&1
cat /dev/null > "$1"
touch "$1"