# 健人就是矯勤

## Concept Development

## Implementation Resources
- 軟體
  - [MediaPipe](https://google.github.io/mediapipe):由Google開發的影像辨識套件
  - [OpenCV](https://opencv.org/):用來做視覺相關影像處理
  - **Raspberry pi OS**(bullseye 11, 32bit):樹梅派的作業系統
- 硬體

|設備名稱|數量|
|-----|--------|
|~~Rasberry pi 3B~~|1       |
|~~picamera v1.3(含支架)~~ |1      |
|筆電VirtualMachine(Linux)|1|
|筆電的HD webcam| 1|

## Problem on Raspberry pi
- 在mediapipe和picamera上有矛盾，mediapipe(只支援在64bit),picamera(只支援在32bit)，一開始因為picamera指令和偵測不到的問題(可用```vcgencmd get_camera```偵測)所以將Raspberrypi的OS從64bit改到32bit，後來經過嘗試後發現mediapipe在32bit上會有許多trouble，**因此最後選擇在虛擬機Linux下去實作**

## Existing Source
- 主程式```PushUp.py```
  - [主程式參考網址](https://circuitdigest.com/microcontroller-projects/push-up-counter-using-raspberry-pi-4-and-mediapipe)
  - 根據上方網址的程式碼進行修改，並再實作仰臥起坐判別
## Implementation Process

- ```sudo apt install pip```(如果沒有內建的話)
- ```sudo pip install mediapipe```
- ```sudo pip install opencv-python```
