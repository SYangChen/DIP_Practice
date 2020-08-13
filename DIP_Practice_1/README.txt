Data Image Processing

	(1072)3/4-18影像處理作業，用python撰寫一個簡易的GUI並對灰階圖片調整亮暗/對比、放大縮小以及Histogram equalization等功能。
	
Getting Started

	環境準備：Ubuntu 16.04、Python 3.5.2
	使用套件：PIL<Image,ImageTk>、tkinter、numpy、matplotlib.pyplot
	事前下載：
		sudo apt-get install python3-pip
		pip3 install camelcase
		pip3 install numpy
		pip3 install opencv-python / python3 -m pip install opencv-python
		sudo apt-get install python3-matplotlib
		sudo pip3 install pillow –upgrade
		
Running the tests

	執行python3 hw1.py，Open File欄位輸入欲處理之檔案名稱再打開此圖片，若輸入錯誤找不到圖檔會跳出錯誤訊息，重新輸入即可，輸入成功則顯示於視窗上。若遇儲存照片，請先於Save File欄位輸入檔案名稱以及副檔名(ex. Abc.jpg)再點按save即可儲存，儲存成功失敗皆會有視窗提醒。
亮度/對比度按鈕顯示即是調整亮度/對比度，可透過點按調整功能，並選擇欲使用之方法為線性、exp或log的演算法，但僅有線性調整有鎖定對比度的a、b選擇，其餘自由調整ab來達成增加亮度或對比度的調整。
Zoom為調整放大縮小的拉桿，可根據數值調整為原始照片的放大或縮小倍率，若放大也提供拉桿調整圖片位置讓圖片沒有死角。
	Histogram按紐可調整灰階圖片並使其灰階程度平均分布，並同時輸出對比前後之差別圖片與histogram圖。
	
Review

	由於是第一次使用python做影像處理以及製作GUI介面，有許多東西都是從0開始上手，一步一步上網模擬別人的寫法，再加以改進，但仍由許多不精確的地方。最大的感受是PIL套件以及OpenCV的差異，原先以為Python Image Library看起來用有最簡單的方法以及最多的運用，但實際使用之後，發現較多的應用都是使用OpenCV來完成，PIL只是最容易上手，使用方法較簡單而已，也因為這樣，下次的作業決定從OpenCV下手。
	這次最大的收穫除了影像處理外，就是GUI介面，希望下次能更精確的使用OpenCV配合其他套件讓下次的影像處理作業更上手。
