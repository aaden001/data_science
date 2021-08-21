#Set the directoryPath
$directoryPath = "C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q1\processed\"
#Save the file names in an array
$files = Get-ChildItem -Name -Path "$directoryPath"

$pattern = "coronavirus"
#to track the number of documents that had the term coronavirus
$stopDocument = 0 

#declare an array of Object
$testObject = @()

#final path to Export-Csv
$finalPath = "C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q2\final.csv"
#run a for loop
foreach ($filenames in $files){
    #concatenate the full file path
    $directoryfilenames = "$directoryPath$filenames"
    #get the number of times, the term coronavirus is found in the document
    $termFrequency= (Get-Content $directoryfilenames| Select-String -pattern "$pattern").length
    #Get the total word per document
    $t = Get-Content $directoryfilenames| Measure-Object -word | Select-Object -expandproperty Words


    #avoid dividing by zero
    #Get TF value frequency/ total word count in document
    if($t -eq 0){
        $tf = 0
    }else {
        $tf = ($termFrequency/$t)  
    }
    
    #Get-Content $directoryfilenames| Measure-Object –Word|Select-Object -expand Words
    #get only document that has a frequency of at least 1
    #Answering Q4 when the frequency of  the word in document is at least one then we can count it once
    if($termFrequency -gt 1){
        $stopDocument++

        $testObject += New-Object pscustomobject -Property @{'Frequency' = $termFrequency;'TotalWord' =$t; 'TF'= $tf;'IDF' = "";'Name'=$filenames; 'URL'=""}
    }
}
$filePath = "C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q2\urlHash.csv"
#get Generated url hash csv
#and make a hashtable 
$mytable = Import-CSV -Path $filePath
$headers = $mytable[0].psobject.properties.name
$key = $headers[0]
$value = $headers[1]
$hashTable = @{}
$mytable | %{$hashTable[$_."$key"] = $_."$value"}


#use the look up table to link to the corresponding Url to test object
$testObject | ForEach-Object {
    $_.URL = $hashTable[$_.Name]
}| Set Object
<# Question 4 #>
echo "This is the total document with at least One occurence of the term coronavirus"
echo $stopDocument
#export finalresorting outputs
$testObject | Export-Csv -Append -Path C:\Users\adeni\CS532\Week8\hw-ranking-aaden001\Q2\final.csv -NoTypeInformation
