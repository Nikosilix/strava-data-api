#!/bin/bash

# Navigate to the project directory
cd ~/Desktop/strava-data-LuiGPT || {
  echo "Directory not found!"
  exit 1
}

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Run the Python script
echo "Running main.py..."
python3 main.py

# Check if the Python script ran successfully
if [ $? -eq 0 ]; then
  echo "main.py executed successfully."

  # Add changes to git
  git add cached_data.json

  # Commit changes
  git commit -m "new data"

  # Push to GitHub
  git push origin main
else
  echo "Python script failed. Aborting git operations."
  exit 1
fi
