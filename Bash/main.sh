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
	rm $pipe
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
		togo[$ID]=true
	done

	return 0
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

function process_video_link () { # ( path videoID )
	local path="$1"
	local videoID="$2"
	if [ -z $videoID ]; then 
		echo -e "ERROR: no videoID to process!" 1>&2
		return 1 
	fi
	local file="${path}${videoID}"
	$DEBUG && echo "file: $file"
	local page=$(cat $file)
	
	# remove from togo
	unset togo[$videoID]
	# get meta data
	get_video_metadata video "$page" || return 1
	$DEBUG && echo -e "$(rof video.to_string)"
	if [ "$(get video.id)" == "" ]; then
		echo -e "ERROR: invalid videoID!" 1>&2
		return 2
	fi

	# add to completed
	completed[$videoID]=true
	# store to csv
	store_to_csv "$(rof video.to_string)" "$fileName"

	# add new IDs
	IDs=$(get_videos_IDs "$page")
    $DEBUG && echo -e "$IDs"
	
	sort_and_store_videoIDs "$IDs"
	return 0
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

iter=100
pages="pages/"
pipe="pipe"
fileName="data.csv"
log="main.log"

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

# init page downloader
if [ ! -p $pipe ]; then
    mkfifo $pipe
fi
./page_downloader.sh < $pipe &> downloader.log &

index=0
while [ "${#togo[@]}" -ne 0 ]; do

	# download pages
	i=1
	for videoID in ${!togo[@]}; do
		# send id and link to pipe
		echo "download" $videoID ${link}$videoID > $pipe
		i=$(( i + 1 ))
		if [ $i -gt $iter ]; then 
			$DEBUG && echo -e "Max itex."
			break 
		fi
	done

	# wait for first download
	while [ $(ls "$pages" | grep -m 1 ".done" | wc -l) -eq 0 ]; do
		sleep 0.1
	done
	
	exit 0
	# parse pages
	while [ $(ls "$pages" | grep ".done" | wc -l) -gt 0 ]; do
		index=$(( index + 1 ))
		$VERBOSE && echo "$index"

		# get videoID from pages
		videoID=$(ls $pages | grep -m 1 ".done" | cut -d "." -f 1)
		$DEBUG && echo "videoID: $videoID"
		process_video_link $pages $videoID # 2> $log

		# remove files
		rm ${pages}${videoID}
		rm ${pages}${videoID}.done
	done

	echo "exit" > $pipe
	break
done

echo "exit" > $pipe
rm $pipe
$VERBOSE && echo -e "Done"

# TODO
# sed občas na něčem spadne
# pars Json
# ISO 639 formát obsahuje metadata o vide včetně jazyka
# END
