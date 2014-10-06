#/bin/bash

function get_mimetype {
file --mime-type $1 | cut -f2 -d":"
}

function upload_entity {
echo $1
}

find . -type f \( -name "*.jpg" \) | while read file
do
    upload_entity "$file"
done
