#!/bin/bash
# By Pytel

DEBUG=true
#DEBUG=false

source ./video.sh
source ./lib.sh

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
    local strings=( 
        "FIWE0hjrDNE;It’s gonna be a massacre???;;en ;UCeeFfhMcJa1kjtfZAGskOCA" 
        "FIWE0hjrDNE;It’s gonna be a massacre!!!;;en zh-Hans fil fr de nl-NL es ;UCeeFfhMcJa1kjtfZAGskOCA" 
        "-NZ7ScAsGHI;Nazev;cs ;"
        "-NZ7ScAsGHI;Novy nazev;cs ;"
        "fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
        "MJ0m9fYs-l8;Ahoj"
        "MJ0m9fYs-l8;' '"
        ";;;;"
    )
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
    local strings=( 
        "FIWE0hjrDNE;It’s gonna be a massacre???;;en ;UCeeFfhMcJa1kjtfZAGskOCA" 
        "-NZ7ScAsGHI;Nazev;cs ;"
        "fbjFofNGHks;Fossil Hybrid HR Q&A;;en ;UCRyUxNpQZBXen_hgkAMRTWw"
        "MJ0m9fYs-l8;Ahoj"
        ";;;;"
    )

    instance="video"

    for string in "${strings[@]}"; do
        echo "String: $string"
        rof Video.from_string "$instance" "$string"
        
        echo -e "To string: $(rof ${instance}.to_string)"
        if [ -z $(get ${instance}.csv_heading) ]; then
            return 1
        fi
        delete $instance
        echo ""
    done
    return 0
}

function test_to_json () {
    new video = Video
    video[id]="123"
    video[name]="halo"

    get video.to_json
    rof video.to_json
    #return 1
    return 0
}