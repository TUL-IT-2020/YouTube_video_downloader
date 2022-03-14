#!/bin/bash
# By Pytel

source ./lib.sh
source ./video.sh

#DEBUG=true
DEBUG=false

#VERBOSE=true
VERBOSE=false

function printHelp () {
	echo -e "OPTIONS:"	
    echo -e "  -h, --help \t\t print this text"
	echo -e "  -d, --debug\t\t enable debug output"
	echo -e "  -v, --verbose\t\t increase verbosity"
    echo -e "  -f, --folder \t\t folder to store the file"
    echo -e "  -n, --name \t\t file name"
    echo -e "  -l, --link \t\t web link to download"
    echo -e "  -s, --safe \t\t create *.done file after finishing"
	echo -e "  -p, --process \t\t pars data"
}

function setFolder () { # ( folder )
	# empty argument
	if [ -z "$1" ]; then
		echo -e "${RED}ERROR: ${NC}empty argument!" 1>&2
		return 1
	fi

	eval folder="$1"

	# do folder exist?
	if [ ! -d $folder ]; then
		$VERBOSE && echo "${RED}ERROR: ${Blue}$folder${NC} do not exist!" 1>&2
		return 2
	fi
	return 0
}

safe=false
process=false

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
        -f | --folder)  shift; setFolder "$1" || exit 3;;
        -n | --name)    shift; name=$1;;
        -l | --link)    shift; link=$1;;
        -s | --safe)    safe=true;;
		-p | --process)	process=true;;
		*) echo -e "Unknown parametr: $arg"; exit 1;;
	esac

	# next arg
	shift
	arg=$1
done

if [ -z $link ]; then 
    $DEBUG && echo -e "ERROR: link not set!"; exit 4
fi

if [ -z $name ]; then
    name=$( echo $link | cut -d "/" -f 3)
fi

if [ -z $folder ]; then 
    path=""
else
    path="$folder/"
fi

if $DEBUG; then
    echo "name: $name"
    echo "folder: $folder"
    echo "link: $link"
    echo "to: ${path}${name}"
fi

if [ ! -f "${path}${name}" ]; then
    $DEBUG && echo "creating new file: ${path}${name}"
fi

if $process; then
	page=$(get_page $link)
	# get meta data
	new video = Video
	get_video_metadata video "$page" || return 1
	sat video.videoIds = "$(get_videos_IDs "$page" | tr "\n" " ")"
	$DEBUG && echo -e "$(rof video.to_string)"
	if [ "$(get video.id)" == "" ]; then
		echo -e "ERROR: invalid videoID!" 1>&2
		return 2
	fi
	rof video.to_json > "${path}${name}"
	delete video
else
	get_page $link > "${path}${name}"
fi

if $safe; then
	touch "${path}${name}.done"
fi

$VERBOSE && echo "Done"
exit 0
# END