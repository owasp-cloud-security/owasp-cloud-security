#!/usr/bin/env bash

usage() {
  echo "Usage: test_threat_file.sh [--all] [FILE...]"
  echo ""
  echo "Runs BDD tests for threat yaml file"
  echo "Options:"
  echo "    --all   Recursively finds all ocst*.yaml files and runs tests"
  echo "    FILE    Test one or more files"
  exit 2
}

if [[ "$#" == "0" ]]; then
  usage
fi

if [[ "$1" == "-h" || "$1" == "--help" ]]; then
  usage
fi

if [[ ! -d "venv" ]]; then
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  deactivate
fi

source venv/bin/activate

total_files=0
failed_files=0

if [[ "$1" == "--all" ]]; then
  for filename in $(find . -name 'ocst*.yaml'); do
    total_files=$((total_files + 1))
    export OCST_FILE="$filename"
    echo "*** Testing $filename"
    behave features/threat_yaml_file.feature
    if [[ "$?" != "0" ]]; then
      failed_files=$((failed_files + 1))
    fi
    echo
  done
else
  for filename in $@; do
    total_files=$((total_files + 1))
    export OCST_FILE="$filename"
    echo "*** Testing $filename"
    behave features/threat_yaml_file.feature
    if [[ "$?" != "0" ]]; then
      failed_files=$((failed_files + 1))
    fi
    echo
  done
fi

deactivate

echo ""
echo "*** Total test summary"
echo "${total_files} files tested, ${failed_files} failed"
if [[ "$failed_files" > "0" ]]; then
  exit 1
else
  exit 0
fi
