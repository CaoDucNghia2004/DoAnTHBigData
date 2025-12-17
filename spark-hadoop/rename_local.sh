#!/bin/bash
# Rename files with spaces to underscores in local /data directory

for dir in /data/train/FAKE /data/train/REAL /data/test/FAKE /data/test/REAL; do
    echo "Processing $dir..."
    cd "$dir"
    find . -name "* *" -type f | while read file; do
        newname=$(echo "$file" | tr ' ' '_')
        mv "$file" "$newname" 2>/dev/null
    done
    echo "Done $dir"
done
echo "All done!"

