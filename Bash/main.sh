#!/bin/bash
# By Pytel

source ./video.sh

DEBUG=true
#DEBUG=false

function get_videos_IDs () { # ( page ) 
	local page="$1"
	echo -e "$page" | tr "," "\n" | grep '"url":"/watch?v=' | grep -v "&" | sort | uniq | cut -d "=" -f2 | tr -d '"'
}

function get_video_metadata () { # ( video page )
	declare -n video_l=$1
	local page=$2
	# TODO
	local videoDetails=$(echo -e "$page" | tr "}" "\n" | grep -m 1 "videoDetails" | tr "," "\n" | tr "{" "\n" )
	video_l[id]=$(echo -e "$videoDetails" | grep "videoId" | cut -d ":" -f2)
	video_l[name]=$(echo -e "$videoDetails" | grep "title" | cut -d ":" -f2)
	video_l[channelId]=$(echo -e "$videoDetails" | grep "channelId" | cut -d ":" -f2)
	video_l[captions]=$(echo -e "$page" | tr "]" "\n" | grep '"captions":' | tr "}" "\n" | tr "," "\n" | grep "language" | cut -d ":" -f 2 | tr -d '"' | tr "\n" " ")
	# echo -e "$page" | tr "]" "\n" | grep '"captions":' | tr "}" "\n" | tr "," "\n" | grep "simpleText" | cut -d ":" -f 3 | tr -d '"

}

function process_video_link () { # ( link videoID )
	local link="$1"
	local videoID="$2"
	local url=$link$videoID
	$DEBUG && echo "url: $url"
	local page=$(wget "$url" -q -O -)
	#echo -e "$page " > new_page.html
	
	# remove from togo
	unset togo[$videoID]
	# add completed + meta data
	get_video_metadata video "$page"
	completed[$videoID]=$(rof video.to_string)
	$DEBUG && echo -e "$(rof video.to_string)"

	IDs=$(get_videos_IDs "$page")
    $DEBUG && echo -e "$IDs"
	
	for ID in $IDs; do	
		# is ID in completed?
		if [ ${completed[$ID]+_} ]; then
			$DEBUG && echo -e "$ID already copmleted."
			continue
		fi

		# is ID in togo?
		if [ ! ${togo[$ID]+_} ]; then
			$DEBUG && echo -e "Adding: $ID -> to go."
			togo[$ID]="to go"
		fi
	done

}

function process_search () { # ( link search )
	local link=$1
	local search=$2
	local url=$link$search
}

function store_to_csv () { # ( hashMap fileName ) 
	declare -n hashMap=$1
	local fileName=$2
	local file=""
	
	if [ -f $fileName ]; then
		file=$(cat $fileName)
else
		touch $fileName
		echo $(get video.csv_heading) > $fileName
	fi

	for key in ${!hashMap[@]}; do
		$DEBUG && echo "$key"
		if [ $(echo "$file" | grep -c -- "$key") -ge 1 ]; then
			file=$(sed "s/$key.*/${hashMap[$key]}/" <<< "$file")
		else
			file="$file\n${hashMap[$key]}"
		fi
	done

	echo -e "$file" > $fileName
}

declare -A togo
declare -A completed

declare -A video
new video = Video

link="https://www.youtube.com/watch?v="
videoID="fbjFofNGHks"
videoID="FIWE0hjrDNE"
url=$link$videoID
file="data.csv"

process_video_link $link $videoID

store_to_csv completed $file

# pars Json

# END

