#!/bin/bash
ROOT=Latex
USER=
TOKEN=
SERVER=http://tesismometro.appspot.com

if [ -z "$USER" ]
then
    echo "You have to fill the user name"
    exit
fi

texcount $ROOT.tex -merge > .tesiscount

words=$(grep "Words in text" .tesiscount | cut -d ' ' -f 4)
figures=$(grep "Number of floats" .tesiscount | cut -d ' ' -f 4)
inlines=$(grep "math inlines" .tesiscount | cut -d ' ' -f 5)
equations=$(grep "math displayed" .tesiscount | cut -d ' ' -f 5)
cites=$(grep -c "<bcf:citekey order=" $ROOT.bcf | cut -d '"' -f 2)
pages=$(grep "Output written on" $ROOT.log | cut -d ' ' -f 5 | tr -d '(')

echo "words $words" 
echo "figures $figures" 
echo "inlines $inlines" 
echo "equations $equations"
echo "cites $cites"
echo "pages $pages"

echo "#Uploading server"
echo "curl --data "name=$USER\&words=$words\&equations_inline=$inlines\&equations=$equations\&figures=$figures\&cites=$cites\&pages=$pages" $SERVER/post"
curl --data "name=$USER&words=$words&equations_inline=$inlines&equations=$equations&figures=$figures&cites=$cites&pages=$pages&token=$TOKEN" $SERVER/post -o .post_output
xdg-open .post_output
