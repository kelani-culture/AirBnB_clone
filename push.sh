#!/usr/bin/env bash
#this script automates the add commit and push flow

git add .

if [[ -n "$1" ]];
then
	git commit -m "$1"
else
	message=""
	while [[ -z "$message" ]];
	do
		echo -en "please provide a commit message :"
		read -r message
		if [[ -n "$message" ]];
		then
			break
		fi
	done
	git commit -m "$message"
fi
git push origin "$(git branch --show-current)"
