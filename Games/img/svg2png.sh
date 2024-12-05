#!/bin/bash
for f in *svg; do
echo $f
inkscape --export-type="png" $f
done
