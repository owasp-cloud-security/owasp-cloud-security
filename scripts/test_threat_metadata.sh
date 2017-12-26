#!/usr/bin/env bash

usage() {
  echo "Usage: test_feature_file.sh [--all] [FILE...]"
  echo ""
  echo "Runs BDD tests for threat and control feature file metadata"
  echo "Options:"
  echo "    --threats   Recursively finds all ocst*.feature files and runs tests"
  echo "    --controls  Recursively finds all ocsc*.feature files and runs tests"
  echo "    --all       Recursively finds all *.feature files and runs tests"
  echo "    FILE        Test one or more files"
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

threats_tested=0
controls_tested=0
total_threat_files=0
failed_threat_files=0
total_control_files=0
failed_control_files=0

test_threat_file() {
  threats_tested=1
  filename="$1"
  total_threat_files=$((total_threat_files + 1))
  export OCST_FILE="$filename"
  echo "*** Testing threat feature file: $filename"
  behave features/threat_feature_file.feature
  if [[ "$?" != "0" ]]; then
    failed_threat_files=$((failed_threat_files + 1))
  fi
  echo
}

test_threat_files() {
  for filename in $(find . -name 'ocst*.feature'); do
    test_threat_file "$filename"
  done
}

test_control_file() {
  controls_tested=1
  filename="$1"
  total_control_files=$((total_control_files + 1))
  export OCSC_FILE="$filename"
  echo "*** Testing control feature file: $filename"
  behave features/control_feature_file.feature
  if [[ "$?" != "0" ]]; then
    failed_control_files=$((failed_control_files + 1))
  fi
  echo
}

test_control_files() {
  for filename in $(find . -name 'ocsc*.feature'); do
    test_control_file "$filename"
  done
}

test_given_files() {
  echo hi
  echo $@
  for filename in $@; do
    file_basename=$(basename "$filename")
    if [[ "$file_basename" == ocst* ]]; then
      test_threat_file "$filename"
    else
      if [[ "$file_basename" == ocsc* ]]; then
        test_control_file "$filename"
      else
        echo "Unknown file type: $filename"
        exit 3
      fi
    fi
  done
}

case "$1" in
  "--all")
    test_threat_files
    test_control_files
    ;;
  "--threats")
    test_threat_files
    ;;
  "--controls")
    test_control_files
    ;;
  *)
    test_given_files "$@"
    ;;
esac

deactivate

echo ""
echo "*** Feature file test summary"
if [[ "$threats_tested" == "1" ]]; then
  echo "${total_threat_files} threat files tested, ${failed_threat_files} failed"
fi
if [[ "$controls_tested" == "1" ]]; then
  echo "${total_control_files} control files tested, ${failed_control_files} failed"
fi

if [[ "$failed_threat_files" > "0" ]] || [[ "$failed_control_files" > "0" ]]; then
  exit 1
else
  exit 0
fi
