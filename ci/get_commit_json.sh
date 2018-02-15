#!/usr/bin/env bash

# bitbucket-pipelines yaml can't handle this command

git log -1 --format='{ "hash": "%H", "date": "%ci", "committer": "%cn", "email":"%ce" }'
