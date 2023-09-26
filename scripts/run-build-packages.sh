#!/bin/bash

set -ex

BASE_DIR=$(pwd)
TARGET_DIR="$BASE_DIR"/target

# clean local target
rm -rf "$TARGET_DIR"
mkdir -p "$TARGET_DIR"


function create_package() {

  utilDir=$BASE_DIR/$1
  utilName=$(basename "$utilDir")
  tempDir=$TARGET_DIR/.tmp/$utilName

  cd "$1" || exit

  echo 'Creating package' "$utilName"
  # Remove old temp data
  if [ -d ../.tmp ]; then rm -rf ../.tmp; fi

  # Create temp dir
  mkdir -p "$tempDir"

  # Move all sources in temp dir
  find . -name '*' -exec cp  -r -P {} "$tempDir" \;

  # Install wheel requirements
  cd "$tempDir"
  python3 setup.py bdist_wheel

  # Package util with dependencies
  cd $TARGET_DIR/.tmp
  mv ./$utilName/dist/*.whl "$TARGET_DIR"/
  cd "$BASE_DIR" || exit
  rm -rf "$TARGET_DIR"/.tmp
}

create_package src/glue_job