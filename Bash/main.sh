#!/bin/bash
# By Pytel

DEBUG=true
#DEBUG=false


function get_videos_IDs () { # ( page ) 
	local page=$1
	echo -e $page | tr "," "\n" | grep '"url":"/watch?v=' | grep -v "&" | uniq | cut -d "=" -f2 | tr -d '"'
}

function get_video_metadata () { # ( page )
	local page=$1
	# TODO
	echo "test"
}

function process_video_link () { # ( link videoID )
	local link="$1"
	local videoID="$2"
	local url=$link$videoID
	$DEBUG && echo "url: $url"
	local page=$(wget "$url" -q -O -)
	#echo -e "$page"
	
	# remove from togo
	unset togo[$videoID]
	# add completed + meta data
	completed[$videoID]=$(get_video_metadata $page)

	IDs=$(get_videos_IDs $page)
    $DEBUG && echo -e "$IDs"
	
	for ID in IDs; do	
		# is ID in completed?
		if [ ${complete[$ID]+_} ]; then
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

function store_to_csv () { # ( hash_map file_name ) 
	local file=$2
}

declare -A togo
declare -A completed

link="https://www.youtube.com/watch?v="
videoID="fbjFofNGHks"
url=$link$videoID

process_video_link $link $videoID

# pars Json

# END

