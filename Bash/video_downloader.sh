#!/bin/bash
# By Pytel
# Stahne podle video (jako .waw) a titulky v pozadovanem jazyce

source ./video.sh
source ./lib.sh

#DEBUG=true
DEBUG=false

VERBOSE=true
#VERBOSE=false

function download_subtitles () { # ( language format id )
    local lang=$1
    local format=$2
    local id=$3
    youtube-dl --write-sub --sub-lang $lang --sub-format $format --skip-download $link$id
}

function download_audio () { # ( format id )
    local format=$1
    local id=$2
    youtube-dl -x --audio-format $format $link$id
}

link="https://www.youtube.com/watch?v="
id="JQKgTnukx7Q"

download_subtitles 

: '
youtube-dl --list-subs
youtube-dl --write-sub --sub-lang en --sub-format vtt --skip-download https://www.youtube.com/watch?v=m_PmLG7HqbQ
youtube-dl -x --audio-format wav https://www.youtube.com/watch?v=m_PmLG7HqbQ
'
# awk vyhledani jazyka titulek
#awk 'BEGIN{FS=";"} $4 ~ /[; ]cs[; ]/'
