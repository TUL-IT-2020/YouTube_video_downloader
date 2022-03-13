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
	# ( varibale csv_string )
	[from_string]='
	local instance=$1;
	shift; local string=$@;
	echo -e "$instance \n";
	echo -e "$string" \n;
	declare -gA $instance;
	new $instance = Video;
	
	sat ${instance}.id = "$(echo "$string" | cut -d ";" -f 1)";
	sat ${instance}.name = "$(echo "$string" | cut -d ";" -f 2)";
	sat ${instance}.language = "$(echo "$string" | cut -d ";" -f 3)";
	sat ${instance}.captions = "$(echo "$string" | cut -d ";" -f 4)";
	sat ${instance}.channelid = "$(echo "$string" | cut -d ";" -f 5)";
	
	get ${instance}.id;
	get ${instance}.name;
		'
	# return json formated string
	[to_json]='
	echo $(get $this.id);
	jq --null-input \
  		--arg id "$(get $this.id)" \
  		--arg name "$(get $this.name)" \
  		{"id": \$id, "name": \$name}
		'
)

# END
