Data Image Processing

	(1072)3/18-4/8影像處理作業，用python撰寫一個簡易的GUI並對灰階圖片實做出Gray level slicing, Bit-Plane images, smoothing/sharpening, Fast Fourier Transformed images, display phase/amplitude only image等功能。
	
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

	執行python3 hw2.py，Open File欄位輸入欲處理之檔案名稱再打開此圖片，若輸入錯誤找不到圖檔會跳出錯誤訊息，重新輸入即可，輸入成功則顯示於視窗上。若遇儲存照片，請先於Save File欄位輸入檔案名稱以及副檔名(ex. Abc.jpg)再點按save即可儲存，儲存成功失敗皆會有視窗提醒。
	1.Gray level slicing 使用者先輸入預先選定之範圍(0-255)，並點擊按鈕選擇未選定區域要顯示原本灰階值或是一律顯示黑色，最後按下show按鈕才會予以改變。
	2.Bit-Plane image 使用者自行選擇欲顯示之第幾個bitplane再點按show即可顯示圖片。
	3.Smoothing/Sharpening 使用者透過切換buttom來選擇要做smoothing or sharpening
	4.Fast Fourier Transformed image 點擊buttom即可顯示。
	5.Amplitude/Phase image 透過兩個buttom觀看其圖片之spectrum及其做inverse後所顯示的圖片。
	
Review

	第二次寫影像處理作業，因為第一次作業對pil使用上功能教侷限，因此這次全面改由opencv操作，相較於第一次，這次也寫得更上手，雖然很多都是call function的，但也讓我對影像處理的一些基本功能有更多的體會，除了老師教學以外，也透過自行上網查詢資料，讓自己更能在課堂中的到驗證，即便某些部份對我來說仍然不太容易，但幾次作業下來希望能更進步。
