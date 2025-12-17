#!/bin/bash
set -euo pipefail

# Normalize CIFAKE filenames on HDFS: replace spaces with underscores
# so that Spark image reader does not hit FileNotFoundException

export PATH="${PATH}:/opt/hadoop-3.2.1/bin"

hdfs dfs -ls -R /datasets/cifake | \
  while read -r f1 f2 f3 f4 f5 f6 f7 path; do
    # Skip summary or empty lines
    if [ -z "${path:-}" ]; then
      continue
    fi

    base="$(basename "${path}")"
    dir="$(dirname "${path}")"

    # Replace spaces with underscores in filename only
    newbase="${base// /_}"

    if [ "${base}" != "${newbase}" ]; then
      echo "Renaming: ${path} -> ${dir}/${newbase}"
      hdfs dfs -mv "${path}" "${dir}/${newbase}"
    fi
  done

