#!/bin/bash
# By Pytel

#DEBUG=true
DEBUG=false

#VERBOSE=true
VERBOSE=false

function printHelp () {
	echo -e "OPTIONS:"	
    echo -e "  -h, --help \t\t print this text"
	echo -e "  -d, --debug\t\t enable debug output"
	echo -e "  -v, --verbose\t\t increase verbosity"
    echo -e ""
	echo -e "COMMANDS:"	
    echo -e "  exit \t\t\t end the script"
    echo -e "  download <name> <url> \t download the url"
}

function download () {
    local name=$1
    local url=$2
    ./download_and_store.sh -s -f "pages" -n "$name" -l "$url" > /dev/null 2>&1 &
}

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
		*) echo -e "Unknown opt: $arg";;
	esac

	# next arg
	shift
	arg=$1
done

read command args
while true; do
    $DEBUG && echo -e "$command, $args"
    case $command in 
        exit)       exit 0;;
        download)   download $args;;
        *)          echo -e "Unknown command: $command";;
    esac
    read command args
done

# END
