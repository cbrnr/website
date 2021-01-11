#!/bin/sh

# stop on error
set -e

printf "\033[0;32mDeploying website to GitHub Pages...\033[0m\n"

# build the website
hugo

# add commits (public is a submodule)
cd public
git add .
msg="rebuilding site on $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# push to GitHub Pages
git push origin main
