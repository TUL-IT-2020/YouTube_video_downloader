#!/bin/bash
# By Pytel

source ~/Shell/tools/class/class.sh

declare -A Video

Video=( 
	[id]=''
	[name]=''
	[language]=''
	[captions]=''
	[channelId]=''
	[csv_heading]='id;name;language;captions;channelid'
	[to_string]='
	echo -e "$(get $this.id);$(get $this.name);$(get $this.language);$(get $this.captions);$(get $this.channelId)";
		'
	# ( varibale csv_string )
	[from_string]='
	local instance=$1;
	shift; local string=$@;
	new $instance = Video;
	
	sat ${instance}.id = "$(echo "$string" | cut -d ";" -f 1)";
	sat ${instance}.name = "$(echo "$string" | cut -d ";" -f 2)";
	sat ${instance}.language = "$(echo "$string" | cut -d ";" -f 3)";
	sat ${instance}.captions = "$(echo "$string" | cut -d ";" -f 4)";
	sat ${instance}.channelId = "$(echo "$string" | cut -d ";" -f 5)";
		'
	# return json formated string
	[to_json]='
	jq --null-input 
  		--arg id "$(get $this.id)"
  		--arg name "$(get $this.name)"
  		"{"id": \$id, "name": \$name}"
		'
	[to_json_old]='
	jq --null-input 
  		--arg id "$(get $this.id)"
  		--arg name "$(get $this.name)"
  		--arg language "$(get $this.language)"
  		--arg captions "$(get $this.captions)"
  		--arg channelId "$(get $this.channelId)"
  		"{"id": \$id, "name": \$name, "language": language, "captions": captions, "channelId": channelId }"
		'
)

# END
