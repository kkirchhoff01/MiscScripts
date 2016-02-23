#!/bin/bash

# Input parameters
URL=$1      # YouTube video URL
NAME=$2     # Desired name of audio file

youtube-dl -o /tmp/$NAME.mp4 -f mp4 "$URL"               # Download video as mp4
avconv -i /tmp/$NAME.mp4 -vn -f mp3 ~/Music/$NAME.mp3    # Convert to mp3

# Remove mp4 from downloads
if [ -e /tmp/$NAME.mp4 ]
then
    echo "Removing ~/Downloads/$NAME.mp4"
    rm /tmp/$NAME.mp4
fi
