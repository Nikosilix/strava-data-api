#!/bin/bash

# Go to the script folder
cd ~/Desktop/strava-data-LuiGPT

# Run the Python script
python3 main.py

# If it succeeds, push the update
if [ $? -eq 0 ]; then
  git add cached_data.json
  git commit -m "Update Strava data"
  git push origin main
else
  echo "Python script failed. Aborting git operations."
fi
