#!/usr/bin/bash
./javac.sh Converter.java
jar xvf jm.jar
jar cvfe converter.jar Converter Converter.class jm/
rm -r jm/
rm Converter.class
rm -r META-INF/
