# 健人就是矯勤

## Concept Development
**到底是平價的徒手健身吸引人，還是奢華的影像辨識輔助健身令人嚮往**
- 健身時動作的正確性十分重要，**正確的姿勢**可以讓健身事半功倍
- 實作的目的就是為了讓使用者能全神貫注在動作本身，透過影像辨識確認動作的準確性，同時讓使用者知道**正確做了多少組數**和**消耗大卡**
- 達到該組數會有**小火車獎勵** :train: :train: :train: 等待時間可作為**組間休息**


**相信在輔助健身的幫助並持之以恆下，人人都可以是范馬勇次郎**
![](https://i.imgur.com/RoK1cNw.png)

~~適度健身吸引異性，過度健身吸引同性~~
## Implementation Resources
- 軟體
  - [MediaPipe](https://google.github.io/mediapipe):由Google開發的影像辨識套件(使用其中的pose estimation)
  - [OpenCV](https://opencv.org/):用來做視覺相關影像處理
  - **Raspberry pi OS**(bullseye 11, 32bit):樹莓派的作業系統(可用```cat /etc/os-release```確認)
- 硬體

|設備名稱|數量|
|-----|--------|
|~~Rasberry pi 3B~~|1       |
|~~picamera v1.3(含支架)~~ |1      |
|Laptop VM(Linux)|1|
|Laptop HD webcam| 1|

!在虛擬機開攝像頭注意事項
**VM版本要改成6.1.40版本**才可以

## Problem on Raspberry pi
- 在mediapipe和picamera上有矛盾，mediapipe(支援在64bit),picamera(支援在32bit)，一開始因為picamera指令和偵測不到的問題(可用```vcgencmd get_camera```偵測和查看有沒有```/dev/video0```)所以將Raspberrypi的OS從64bit改到32bit，後來經過嘗試後發現mediapipe在32bit上會有許多trouble
- 有找到在32bit上的Unofficial但無法使用  :cry:(https://pypi.org/project/mediapipe-rpi4/)
- 受限於時間緊迫，**因此最後選擇在Ubuntu虛擬機下去實作**

## Existing Source
- 主程式```pushup.py``` ```sitout.py```
  - [主程式參考網址](https://circuitdigest.com/microcontroller-projects/push-up-counter-using-raspberry-pi-4-and-mediapipe)
  - 根據上方網址的程式碼進行修改，並再實作仰臥起坐判別
- mediapipe的```PoseModule```
  - 參考freecodecamp(**YT可以找到**)並修改

## Pose node in MediaPipe
![](https://i.imgur.com/Kdp0rM7.png)
- 可借鑑去實作其他動作判別(距離or角度)

## Implementation Process
### 主程式
**python version: 3.8.10**(Linux中內建)
- ```sudo pip install cowsay```(有隨機驚喜，沒有要用拿掉即可)
- ```sudo apt install pip```(如果沒有內建的話)
- ```sudo pip install mediapipe```
- ```sudo pip install opencv-python```(要更完整版可以```sudo pip install opencv-contrib-python```)

**先建立opencv與mediapipe的Pose Module**,
**Pose Module**包含:
- ```init function```: mediapipe pose solutions跟mediapipe畫圖工具
- ```findPose```: 找mediapipe Pose的33個landmarks
- ```findPosition```: 把33個landmarks的(x,y)座標算出來
- ```calculateAngle```: 算出三個landmarks之間的角度
- ```calculateY_axisDis```: 算出兩點之間的Y軸距離
- ```calculateX_axisDis```: 算出兩點之間的X軸距離

**PusuUp counter**: 
- ```pushup.py```用cv2跟Pose Module，然後用左肩跟左手肘的Y軸距離去做判斷伏地挺身的次數

### GUI
目前只實作在伏地挺身```pushup.py```上，仰臥起坐```sitout.py```尚未完工
- 先下載 ```sudo apt-get install tkinter```才能使用python的GUI
- 可以設定1分鐘到90分鐘(**可作為組間休息**)，以及要做幾下push ups
- ![](https://i.imgur.com/KjSVVOw.png)
- 做完設定的Push ups後會跳出小火車 :train: 

## Useage
- Step1:安裝所有需要的檔案
- Step2:執行```python3 cutdown.py```時間到了會去呼叫```pushup.py```
- Step3:大功告成

## Knowledge From Lecture
- Ubuntu虛擬機環境
- GUI會跑出小火車(sl)

## job Assignment
- ```陳竣哲```:題目發想、材料購買、程式研擬、raspi研究、影片、github
- ```何智立```:程式研擬&彙整、raspi研究、影片、github
- ```吳楚熙```:GUI、GUI結合程式、github
- ```陳麒益```:程式研擬、raspi研究、ppt
- ```林昱翔```:勞力活、ppt

## Future Prospects
- 可以將整體弄成更完善的健身系統
- 加上提示音效、健身音樂等等...

## References
### 線上資源
- [實作參考教程](https://circuitdigest.com/microcontroller-projects/push-up-counter-using-raspberry-pi-4-and-mediapipe)
- [確認相機模組](https://raspberrytips.com/troubleshooting-camera-module/)
- 參考轉換不同python version:
https://www.youtube.com/watchv=QdlopCUuXxw&ab_channel=SamWestbyTech
- install OpenCV:
https://www.youtube.com/watch?v=QzVYnG-WaM4&ab_channel=SamWestbyTech
- 多個stackoverflow和github上的issues

### 線下詢問
- MOLi一些助教的無私幫忙

## Demo Video
[Demo影片在這](https://drive.google.com/file/d/1hYK0VFFGBiLi75ySgKQAsHuctIxgKAOE/view?usp=share_link)
