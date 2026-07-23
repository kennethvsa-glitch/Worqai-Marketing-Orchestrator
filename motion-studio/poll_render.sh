#!/bin/bash
cd "C:/Users/kenne/motion-studio"
file="export-video/video_villain-v3-quantum-v2_2026-06-25.mp4"
echo "=== Polling render for 280 seconds ==="
for i in $(seq 1 14); do
    sleep 20
    if [ -f "$file" ]; then
        size=$(ls -l "$file" 2>/dev/null | awk '{print $5}')
        echo "T+$(($i*20))s: size=${size} bytes"
    else
        echo "T+$(($i*20))s: file not yet created"
    fi
done
echo "=== Final check ==="
if [ -f "$file" ]; then
    size=$(ls -l "$file" 2>/dev/null | awk '{print $5}')
    echo "File: $file"
    echo "Size: $size bytes"
    if [ "$size" -gt 5000000 ]; then
        echo "STATUS: COMPLETE"
    else
        echo "STATUS: IN_PROGRESS"
    fi
else
    echo "STATUS: NOT_FOUND"
fi
