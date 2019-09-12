for i in *.mp4; do ffmpeg -i "$i" -vf scale=640:480 "${i%.*}_small.mp4"; done
