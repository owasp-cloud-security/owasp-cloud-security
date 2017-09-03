#!/usr/bin/env bash

if [[ ! -f LICENSE ]]; then
  echo "Please run this from the root of the project"
  exit 1
fi

ROOT_PATH="$PWD"

for file in $(find . -name "threatmodel.md"); do
  dirname=$(dirname "$file")
  pushd "$dirname" > /dev/null
  echo "Processing $dirname"
  cat threatmodel.md > README.md
  $ROOT_PATH/scripts/ocst2md.py *_threats.yaml >> README.md
  popd > /dev/null
done

