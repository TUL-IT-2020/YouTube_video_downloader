#!/bin/bash
# By Pytel

DEBUG=true
#DEBUG=false

source ./video.sh
source ./lib.sh

strings=( 
    "FIWE0hjrDNE;It’s gonna be a massacre???;;en ;UCeeFfhMcJa1kjtfZAGskOCA" 
    "FIWE0hjrDNE;It’s gonna be a massacre!!!;;en zh-Hans fil fr de nl-NL es ;UCeeFfhMcJa1kjtfZAGskOCA" 
    "-NZ7ScAsGHI;Nazev;cs ;;"
    "-NZ7ScAsGHI;Novy nazev;cs ;;"
    "fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
    "MJ0m9fYs-l8;Ahoj;;;"
    "MJ0m9fYs-l8;' ';;;"
    ";;;;"
)

function test_get_videos_IDs () {
    local fileName="page.html"
    local page=$(cat $fileName)

    ret=$(get_videos_IDs "$page" | tr -d "\n")
    valid="a149ECUXPTkBlGalsye6pYEp1UiTUXdqkfbjFofNGHksfP2I2Le-AaggNDLwQWrEmMGvDQPiY3alcHH9IECFklJUIXcVNlxDSfENSqVyMlGJ6woOycqkr_kVYO6Kn4VXQczspHUHlZF7u10QpHcqT-pu2IQ4boHXXXzD8Si3MsFvFAxMTwTZaJ97d0YVPUK1qyIAy00R0539ARqUs9qia3hme3iw"
    if [ "$ret" != "$valid" ]; then
        echo "string: $string"
        echo "valid: $valid"
        return 1
    fi

    return 0
}

function test_to_string1 () {
    new video = Video

    sat video.id = "fbjFofNGHks"
    sat video.name = "Fossil Hybrid HR Q&A"
	sat video.language = ""
	sat video.captions = "en "
	sat video.channelId = "UCRyUxNpQZBXen_hgkAMRTWw"

    local valid="fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
    local string=$(rof video.to_string)
    if [ "$string" != "$valid" ]; then
        echo "string: $string"
        echo "valid: $valid"
        return 1
    fi
    delete video
    return 0
}

function test_to_string2 () {
    new video = Video

    video[id]="fbjFofNGHks"
    video[name]="Fossil Hybrid HR Q&A"
	video[language]=""
	video[captions]="en "
	video[channelId]="UCRyUxNpQZBXen_hgkAMRTWw"

    local valid="fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
    local string=$(rof video.to_string)
    if [ "$string" != "$valid" ]; then
        echo "string: $string"
        echo "valid: $valid"
        return 1
    fi
    delete video
    return 0
}

function test_get_video_metadata () {
    new video = Video
    local fileName="page.html"
    local page=$(cat $fileName)

    get_video_metadata video "$page"

    local valid="fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
    local string=$(rof video.to_string)
    if [ "$string" != "$valid" ]; then
        echo "string: $string"
        echo "valid: $valid"
        return 1
    fi
    delete video
    return 0
}

function test_store_to_csv () {
    local fileName="test_file.csv"
    touch $fileName

    for string in "${strings[@]}"; do
        store_to_csv "$string" $fileName
    done
    echo "file: $fileName"
    cat $fileName
    rm $fileName
    return 0
}

function test_from_string () {
    instance="video"

    for string in "${strings[@]}"; do
        $DEBUG && echo -e "String: $string"
        rof Video.from_string "$instance" "$string"
        
        $DEBUG && echo -e "To string: $(rof ${instance}.to_string)"
        if [ -z $(get ${instance}.csv_heading) ]; then
            return 1
        fi
        delete $instance
        $DEBUG && echo ""
    done
    return 0
}

function test_from_string_to_string () {
    for string in "${strings[@]}"; do
        $DEBUG && echo -e "String: $string"
        rof Video.from_string video "$string"
        
        $DEBUG && echo -e "To string: $(rof video.to_string)"
        if [ -z $(get video.csv_heading) ]; then
            return 1
        fi
        if [ "$(rof video.to_string)" != "$string" ]; then
            rof video.to_string
            echo "$string"
            return 2
        fi
        delete video
        $DEBUG && echo ""
    done
    return 0
}

function test_from_string_to_json () {
    instance="video"
    for string in "${strings[@]}"; do
        echo "String: $string"
        rof Video.from_string "$instance" "$string"
        
        echo -e "To string: $(rof ${instance}.to_string)"
        if [ -z $(get ${instance}.csv_heading) ]; then
            return 1
        fi
        rof video.to_json
        delete $instance
        echo ""
    done
    return 0
}

function from_string_over_json_to_string () {
    instance="video"
    for string in "${strings[@]}"; do
        echo "String: $string"
        rof Video.from_string "$instance" "$string"
        
        echo -e "To string: $(rof ${instance}.to_string)"
        if [ -z $(get ${instance}.csv_heading) ]; then
            return 1
        fi
        json=$(rof $instance.to_json)
        delete $instance

        Video.from_json "$instance" "$json"
        if [ "$(rof $instance.to_string)" != "$string" ]; then
            rof video.to_string
            echo "$string"
            return 2
        fi
        delete $instance
        echo ""
    done
    return 0
}