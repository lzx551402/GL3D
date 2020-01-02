#!/usr/bin/bash
DATA_NAME=$1

if [ ! -d download_data_$DATA_NAME ]; then
    mkdir -p download_data_$DATA_NAME
fi

let CHUNK_START=$2
let CHUNK_END=$3

for ((i=CHUNK_START;i<=CHUNK_END;i++)); do
    IDX=$(printf "%03d" $i)
    URL=research.altizure.com/data/gl3d_v2/$DATA_NAME/$DATA_NAME.tar.$IDX
    wget -c $URL -P download_data_$DATA_NAME
    echo $URL
done

URL=research.altizure.com/data/gl3d_v2/$DATA_NAME/sha1sum.txt
wget -c $URL -P download_data_$DATA_NAME

