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
)

# END
