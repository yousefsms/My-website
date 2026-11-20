#!/bin/bash
# Ensure we have a local server running in the background
python3 -m http.server 8000 &
SERVER_PID=$1
# Wait for server to start
sleep 2

# Capture widescreen
firefox --headless --screenshot widescreen.png "http://localhost:8000/DataStream.html#dm04-container"

# Capture portrait/mobile (simulated via window size if possible, 
# but firefox --screenshot usually takes a full page or specified window size)
# For mobile we use the specified resolution
firefox --headless --window-size 844,390 --screenshot portrait.png "http://localhost:8000/DataStream.html#dm04-container"

# Kill server
kill $SERVER_PID
