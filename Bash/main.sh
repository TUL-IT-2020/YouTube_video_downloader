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
		$DEBUG && echo "Adding: $ID to go."
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
		# remove from togo
		unset togo[$videoID]

		# send id and link to pipe
		$DEBUG && echo -e "Puting to pipe: $videoID"
		echo "download" $videoID ${link}$videoID > $pipe
		i=$(( i + 1 ))

		# add to completed
		completed[$videoID]=true

		if [ $i -gt $iter ]; then 
			$DEBUG && echo -e "Max itex."
			break
		fi
	done

	# wait for first download
	while [ $(ls "$pages" | grep -m 1 ".done" | wc -l) -eq 0 ]; do
		sleep 0.1
	done
	
	# parse pages
	while [ $(ls "$pages" | grep ".done" | wc -l) -gt 0 ]; do
		index=$(( index + 1 ))
		$VERBOSE && echo "$index"

		# get videoID from pages
		videoID=$(ls $pages | grep -m 1 ".done" | cut -d "." -f 1)
		$DEBUG && echo "path: $pages"
		$DEBUG && echo "videoID: $videoID"
		process_video_json "${pages}${videoID}" # 2> $log

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
# pars Json
# ISO 639 formát obsahuje metadata o vide včetně jazyka
# END
