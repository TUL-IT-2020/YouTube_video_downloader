#!/bin/bash
# By Pytel

source ./video.sh
source ./lib.sh

DEBUG=true
#DEBUG=false

VERBOSE=true
#VERBOSE=false

function get_page () { # ( url )
	wget "$url" -q -O -
}

function sort_and_store_videoIDs () { # ( IDs )
	local IDs=$1
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
			togo[$ID]=true
		fi
	done
}

function process_video_link () { # ( link videoID )
	local link="$1"
	local videoID="$2"
	local url=$link$videoID
	$DEBUG && echo "url: $url"
	local page=$(get_page $url)
	#echo -e "$page" > page.html
	
	# remove from togo
	unset togo[$videoID]
	# get meta data
	get_video_metadata video "$page"
	$DEBUG && echo -e "$(rof video.to_string)"
	# add to completed
	completed[$videoID]=$(rof video.to_string)
	# store to csv
	store_to_csv "$(rof video.to_string)" "$fileName"

	IDs=$(get_videos_IDs "$page")
    $DEBUG && echo -e "$IDs"
	
	sort_and_store_videoIDs "$IDs"

}

function process_search () { # ( link search )
	local link=$1
	local search=$2
	local url=$link$search
}

function store_hashMap_to_csv () { # ( hashMap fileName ) 
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
#togo[fbjFofNGHks]=true
#togo[FIWE0hjrDNE]=true
togo[LKC0NG0g2ek]=true

fileName="data.csv"
if [ ! -f $fileName ]; then
	touch $fileName
	echo $(get video.csv_heading) > $fileName
fi

index=0
while [ "${#togo[@]}" -ne 0 ]; do
	for videoID in ${!togo[@]}; do
		index=$(( index + 1 ))
		$VERBOSE && echo "$index"
		process_video_link $link $videoID
	done
	break
done

# TODO
# sed občas na něčem spadne
# pars Json
# ISO 639 formát obsahuje metadata o vide včetně jazyka
# END
