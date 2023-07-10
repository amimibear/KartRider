#!/bin/bash

# 修改这个值为您想要的开始整数N

number_file="img/_.txt"

# 指定Mac上保存截图的目录
destination_folder="img"

# 每隔1秒截图
while true; do
  current_number=$(cat "$number_file")
  # adb shell screencap -p /sdcard/screenshot.png
  # adb pull /sdcard/screenshot.png "$destination_folder/$current_number.png"
  # adb shell rm /sdcard/screenshot.png

  # adb exec-out screencap -p > "$destination_folder/$current_number.png"
  
  # 家wifi
  # adb -s 192.168.1.22:5555 exec-out screencap -p > "$destination_folder/$current_number.png"
  
  # 图书馆wifi
  # adb -s 192.168.1.5:5555 exec-out screencap -p > "$destination_folder/$current_number.png"
  # adb -s 192.168.101.135:5555 exec-out screencap -p > "$destination_folder/$current_number.png"
  # adb -s 192.168.101.245:5555 exec-out screencap -p > "$destination_folder/$current_number.png"
  
  adb -s H8B4C19716005860 exec-out screencap -p > "$destination_folder/$current_number.png"


  next_number=$((current_number + 1))
  echo $next_number > "$number_file"
  echo $next_number

  sleep 2
done
