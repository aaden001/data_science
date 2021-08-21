#!/bin/bash
# [System.IO.File] class
$count = 1
$Textfie = "C:\Users\adeni\CS532\Week5\hw2-archiving-aaden001\Q1\dict.txt"
foreach($line in [System.IO.File]::ReadLines($Textfie)){
	
	$stringCount = $count.ToString()
	docker container run -it --rm oduwsdl/memgator --format=json  $line  > C:\Users\adeni\CS532\Week5\hw2-archiving-aaden001\Q2\json\$stringCount.json
	$count++
	
}
