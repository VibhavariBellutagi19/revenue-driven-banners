#!/bin/bash

set -ex

BASE_DIR=$(pwd)
TARGET_DIR="$BASE_DIR"/target
VERSION=$(cat "$BASE_DIR"/VERSION)

# create local target
if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

TARGET_DIR_LAMBDAS="$TARGET_DIR"/"$VERSION"

function packageLambdas() {
  lambdaDir=$BASE_DIR/$1
  lambdaName=$(basename "$lambdaDir")
  tempDir=$TARGET_DIR_LAMBDAS/.tmp/$lambdaName

  cd "$1" || exit

  echo 'Packaging Lambda function' "$lambdaName"
  # Remove old temp data
  if [ -d ../.tmp ]; then rm -rf ../.tmp; fi

  # Create temp dir
  mkdir -p "$tempDir"

  # Move all sources in temp dir
  find . -name '*.py' -exec cp -P {} "$tempDir" \;

  # Package lambda with dependencies
  cd "$TARGET_DIR_LAMBDAS"/.tmp && find . | grep -E "(__pycache__|\.pyc|\.pyo$|*tests*|boto3|botocore)" | xargs rm -rf && zip -r "${lambdaName}_${VERSION}".zip .
  mv *.zip "$TARGET_DIR"
  cd "$BASE_DIR" || exit
  rm -rf "$TARGET_DIR_LAMBDAS"
}

 packageLambdas "src/lambdas/push_to_dynamodb"
