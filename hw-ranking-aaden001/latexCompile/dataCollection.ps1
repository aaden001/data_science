$Textfie = "C:\Users\adeni\CS532\Week5\hw2-archiving-aaden001\Q1\dict.txt"
$arrayUrlMd5 = @()
foreach($line in [System.IO.File]::ReadLines($Textfie)){
	#Build the output file for each URL
	$md5 = New-Object -TypeName System.Security.Cryptography.MD5CryptoServiceProvider
	$utf8 = New-Object -TypeName System.Text.UTF8Encoding
    #hash the each URLs in the dict.txt
	$hash = [System.BitConverter]::ToString($md5.ComputeHash($utf8.GetBytes($line)))
	$hash = $hash.Replace('-','') #has md5hash values

    #User for question 1
	docker container run -it --rm curlimages/curl -L  $line  > C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q1\html\$hash.html
	#user for Question 2
    #Generate csv file for url hash
    $hash = "$hash.txt"
    $arrayUrlMd5 += New-Object pscustomobject -Property @{'URL'=$line; 'hash' = $hash} 

    $count++
	
}
#save object to csv file
$arrayUrlMd5 | Export-Csv -Append -Path C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q2\urlHash.csv -NoTypeInformation

