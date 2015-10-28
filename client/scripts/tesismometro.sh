#!/bin/bash
TEXNAME=tesis.tex
USER=""
#SERVER=http://localhost:8080
SERVER=http://tesismometro.appspot.com

if [ -z "$USER" ]
then
    echo "You have to fill the user name"
    exit
fi

texcount $TEXNAME -merge > .tesiscount

words=$(grep "Words in text" .tesiscount | cut -d ' ' -f 4)
figures=$(grep "Number of floats" .tesiscount | cut -d ' ' -f 4)
inlines=$(grep "math inlines" .tesiscount | cut -d ' ' -f 5)
equations=$(grep "math displayed" .tesiscount | cut -d ' ' -f 5)


echo "words $words" 
echo "figures $figures" 
echo "inlines $inlines" 
echo "equations $equations" 

echo "#Uploading server"
echo "curl --data "name=$USER\&words=$words\&equations_inline=$inlines\&equations=$equations\&figures=$figures" $SERVER/post"
curl --data "name=$USER&words=$words&equations_inline=$inlines&equations=$equations&figures=$figures" $SERVER/post
