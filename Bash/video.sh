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
	echo "$(get $this.id);$(get $this.name);$(get $this.language);$(get $this.captions);$(get $this.channelId)";
		'
	[from_string]='
	# ( varibale csv_string );
	local instance=$1;
	shift; local string=$@;
	declare -gA $instance;
	new $instance Video;
	sat ${instance}.id = "$(echo "$string" | cut -d ";" -f 1)";
	sat ${instance}.name = "$(echo "$string" | cut -d ";" -f 2)";
	sat ${instance}.language = "$(echo "$string" | cut -d ";" -f 3)";
	sat ${instance}.captions = "$(echo "$string" | cut -d ";" -f 4)";
	sat ${instance}.channelid = "$(echo "$string" | cut -d ";" -f 5)";
		'
)

# END
