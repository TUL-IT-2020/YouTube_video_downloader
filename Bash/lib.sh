#!/bin/bash
# By Pytel

function get_page () { # ( url )
	local url=$1
	wget "$url" -q -O -
}

function get_videos_IDs () { # ( page ) 
	local page="$1"
	echo -e "$page" | tr "," "\n" | grep '"url":"/watch?v=' | grep -v "&" | sort | uniq | cut -d "=" -f2 | tr -d '"'
}

function get_video_metadata () { # ( video page )
	declare -n video_l=$1
	local page=$2
	if [ -z "$page" ]; then 
		echo -e "ERROR: no page to parse! $(get video.id)" 1>&2
		return 1 
	fi
	local videoDetails=$(echo -e "$page" | tr "}" "\n" | grep -m 1 "videoDetails" | tr "," "\n" | tr "{" "\n" )
	video_l[id]=$(echo -e "$videoDetails" | grep "videoId" | cut -d ":" -f2 | tr -d '"')
	video_l[name]=$(echo -e "$videoDetails" | grep "title" | cut -d ":" -f2 | tr -d '"')
	video_l[channelId]=$(echo -e "$videoDetails" | grep "channelId" | cut -d ":" -f2 | tr -d '"')
	video_l[captions]=$(echo -e "$page" | tr "]" "\n" | grep '"captions":' | tr "}" "\n" | tr "," "\n" | grep "language" | cut -d ":" -f 2 | tr -d '"' | tr "\n" " ")
	# echo -e "$page" | tr "]" "\n" | grep '"captions":' | tr "}" "\n" | tr "," "\n" | grep "simpleText" | cut -d ":" -f 3 | tr -d '"
	return 0
}

function store_to_csv () { # ( string fileName ) 
	local string=$1
    local key=$(echo $1 | cut -d ";" -f1)
	local fileName=$2

    if $DEBUG ; then
        echo "args: $@"
        echo "string: $string"
        echo "key: $key"
        echo "file: $fileName"
    fi 

	if [ -z "$key" ]; then 
		echo -e "ERROR: no ID!" 1>&2; return 1
	fi
	
	if [ $(cat "$fileName" | grep -c -- "$key") -ge 1 ]; then
        $DEBUG && echo "Editing line"
		sed -i "s/${key}.*/${string}/" "$fileName"
	else
        $DEBUG && echo "Adding new line"
		echo $string >> $fileName
	fi
	return 0
}
