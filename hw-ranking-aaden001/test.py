import requests
import sys
from boilerpy3 import extractors

# Tested on HTML documents downloaded with
# wget -O test.html "https://www.cnn.com/2021/03/03/business/wendys-breakfast-sales/index.html"
# wget -O test.html "https://www.cnn.com/2021/03/03/world/iceland-volcano-eruption-keilir-intl-latam/index.html"

# % python3 boiler-test.py < test.html > test.txt

# If you get UnicodeDecodeError, uncomment these lines
#sys.stdin.reconfigure(encoding='utf-8')
#sys.stdout.reconfigure(encoding='utf-8')

# read in entire input into a string

with open(sys.argv[2], 'r') as f:
    f.reconfigure(encoding='utf-16')
    contents = f.read()
#text = sys.stdin.read()
print(contents)
# strip tags
extractor = extractors.ArticleExtractor()
content = extractor.get_content(str(contents))

# write processed output to stdout
print(content)