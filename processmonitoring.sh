#!/bin/bash

ps aux | grep -i python | awk  -v date="$(date +"%Y-%m-%d %r")" {'print date, $13, $2'} | grep -vE 'python' > process_id.log
