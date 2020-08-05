#!/usr/bin/env bash

VARIANT=stretch-slim

echo $VARIANT

slash='/'; image="mergebilling:${VARIANT//$slash/-}"

docker build -t "$image" .