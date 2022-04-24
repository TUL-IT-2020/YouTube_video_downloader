#!/bin/bash
# By Pytel

source ./video.sh
source ./lib.sh

#DEBUG=true
DEBUG=false

VERBOSE=true
#VERBOSE=false

function printHelp () {
	echo -e "OPTIONS:"	
    echo -e "  -h, --help \t\t print this text"
	echo -e "  -d, --debug\t\t enable debug output"
	echo -e "  -v, --verbose\t\t increase verbosity"
	echo -e "  -c, --clean \t\t clean unneeded files"
	echo -e "  -s, --seed \t\t file with seeds"
    echo -e ""
}

function cleanup () {
	rm $log
	rm downloader.log
	rm ${pages}*
}

function download () {
    local name=$1
    local url=$2
	$VERBOSE && echo -e "Downloading: $url"
	./download_process_and_store.sh -s -p -f "pages" -n "$name" -l "$url" &
}

function get_n_keys_from_hashMap () { # ( hashMap n )
	declare -n hashMap=$1
	local n=$2
	local i=0
	declare -a array=()
	for key in ${!hashMap[@]}; do
		array+=( $key )
		$DEBUG && echo -e "Index: $i, key: $key" 1>&2
		if [ $i -gt $n ]; then 
			$DEBUG && echo -e "Max itex."  1>&2
			break
		fi
		i=$(( i + 1 ))
	done
	echo -e "${array[@]}"
	return 0
}

function get_next_videoId () { # ( hashMap videoId )
	local -n id=$2
	if [ $video_slice_index -ge $video_slice_size ]; then
		$DEBUG && echo -e "index: $video_slice_index >= size: $video_slice_size" 1>&2
		#read -r -a video_slice <<< $(get_n_keys_from_hashMap $1 $video_slice_max_size)
		video_slice=( $(get_n_keys_from_hashMap $1 $video_slice_max_size) )
		video_slice_size=${#video_slice[@]}
		video_slice_index=0
		$DEBUG && echo -e "Size: $video_slice_size, index: $video_slice_index" 1>&2
	fi
	id=${video_slice[$video_slice_index]}
	video_slice_index=$(( video_slice_index + 1 ))
	$DEBUG && echo -e "VideoId: $id, new index: $video_slice_index" 1>&2
}

function setSeed () { # ( file )
	# empty argument
	if [ -z "$1" ]; then
		echo -e "${RED}ERROR: ${NC}empty argument!" 1>&2
		return 1
	fi

	local file="$1"

	# do folder exist?
	if [ ! -f $file ]; then
		$VERBOSE && echo "${RED}ERROR: ${Blue}$file${NC} do not exist!" 1>&2
		return 2
	fi

	for ID in $(cat $file); do
		$DEBUG && echo "Adding: $ID to go."
		togo[$ID]=true
	done

	return 0
}

function sort_and_store_videoIDs () { # ( IDs )
	local IDs=$1
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

function process_video_json () { # ( path/file )
	local path="$1"
	$DEBUG && echo "file: $path"
	local file=$(cat $path)

	# get data
	rof Video.from_json video "$file"

	# store to csv
	$DEBUG && echo -e "$file"
	$DEBUG && echo -e "$(rof video.to_string)"
	store_to_csv "$(rof video.to_string)" "$fileName"

	# add new IDs
	IDs=$(get video.videoIds)
    $DEBUG && echo -e "$IDs"
	
	sort_and_store_videoIDs "$IDs"
	return 0
}

function process_search () { # ( link search )
	local link=$1
	local search=$2
	local url=$link$search
	# vytvoří seedy
	# jak vyřečím speciální parametry pro vyhledávání titulků?
	page=$(get_page $url)
}

declare -A togo
declare -A completed

declare -A video
new video = Video

link="https://www.youtube.com/watch?v="

pages="pages/"
fileName="data.csv"
log="main.log"

threads=0
max_threads=10
video_slice=()
video_slice_max_size=100
video_slice_size=0
video_slice_index=0

# parse input
$DEBUG && echo "Args: [$@]"
arg=$1
while [ $# -gt 0 ] ; do
	$DEBUG && echo "Arg: $arg remain: $#"

	# vyhodnoceni
	case $arg in
		-h | --help) 	printHelp; exit 2;;
		-d | --debug) 	DEBUG=true;;
		-v | --verbose) VERBOSE=true;;
		-c | --clean)	cleanup; exit 0;;
		-s | --seed)	shift; setSeed "$1" || exit 3;;
		*) echo -e "Unknown opt: $arg";;
	esac

	# next arg
	shift
	arg=$1
done

# init .csv file
if [ ! -f $fileName ]; then
	touch $fileName
	echo $(get video.csv_heading) > $fileName
fi

index=0
end=false
while [ "${#togo[@]}" -ne 0 ]; do

	# download pages
	while [ $threads -lt $max_threads ]; do
		# get next videoId
		get_next_videoId togo videoId
		$DEBUG && echo -e "Size: $video_slice_size, index: $video_slice_index"
		$DEBUG && echo -e "VideoId: $videoId"
		if [ -z $videoId ]; then break; fi

		# remove from togo
		unset togo[$videoId]

		# send id and link to pipe
		$DEBUG && echo -e "To download: $videoId"
		download $videoId ${link}$videoId &> downloader.log

		# add to completed
		completed[$videoId]=true
		threads=$(( threads + 1 ))
	done
	
	# store parsed pages
	if [ $(ls "$pages" | grep ".done" | wc -l) -gt 0 ]; then
		index=$(( index + 1 ))
		$VERBOSE && echo "$index"

		# get videoID from pages
		videoId=$(ls $pages | sort -r | grep -m 1 ".done" | cut -d "." -f 1)
		$DEBUG && echo "path: $pages"
		$DEBUG && echo "videoId: $videoId"
		process_video_json "${pages}${videoId}" 2> $log

		# remove files
		rm ${pages}${videoId}
		rm ${pages}${videoId}.done
		threads=$(( threads - 1 ))
	fi

	# exit
	if read -r -t 0.1 -n 1 string; then
		$DEBUG && echo -e "Read: $string"
		case $string in 
			q)	end=true;;
			*)  $VERBOSE && echo -e "Unknown command: $string";;
		esac
	fi
	if $end; then break; fi

	#break
done

$VERBOSE && echo -e "Done"

# END
