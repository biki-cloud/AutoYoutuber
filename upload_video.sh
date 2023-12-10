#!/bin/sh
$cmd='python3 lib/youtube/youtube.py --file="save/movie/output.mp4" --title="Template Movie title" --description="Template description." --category="10" --privacyStatus="private"'
echo "-----------------------------------"
echo $cmd
echo "-----------------------------------"
$cmd