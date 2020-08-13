from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
#from tkinter import ttk

window = tk.Tk()					# create window
window.title( 'B063040061 hw2' )	# name title

flagOpen = False					# file open flag
flagOB = False						# preserve/black flag
flagSS = False						# smoothing/sharpening
glsvar1 = tk.IntVar()				# gray level slicing varible
glsvar2 = tk.IntVar()				# ''
bpivar = tk.IntVar()				# bit plane image varible


def WarningMessage() :
	# warning message show if image name not found
	a = tk.messagebox.showwarning( 'Warning', 'File Not Found!\nPlease try again!' )
	
def ShowInfo() :
	# successful message saved
	a = tk.messagebox.showinfo( 'Success', 'File Saved!' )
	
def ShowWarning() :
	# successful message saved
	a = tk.messagebox.showwarning( 'Failed', 'Unknowed type' )

def oCBOpen() :
	# open or reset the image
	global imageOri, flagOpen
	if flagOpen == False :
		
		try :
			# load the image from directory
			# detect edges in it
			imageOri = cv.imread( o.get() )
			imageOri = cv.cvtColor( imageOri, cv.COLOR_BGR2GRAY ) 
			image = cv.resize( imageOri, ( 300,300 ), interpolation = cv.INTER_CUBIC )
			edged = cv.Canny( imageOri, 50, 100 )
		
			# OpenCV represents images in BGR order ; 
			# however PIL represents images in RGB order, so we need to swap the channels
			imgRender = cv.cvtColor( image, cv.COLOR_BGR2RGB )
	
			# convert the images to PIL format
			imgRender = Image.fromarray( imgRender )
			edged = Image.fromarray( edged )
			imgRender = ImageTk.PhotoImage( imgRender )
			edged = ImageTk.PhotoImage( edged )
	
			imgPanelL.config( image = imgRender )
			imgPanelL.image = imgRender ;
			imgPanelR.config( image = imgRender )
			imgPanelR.image = imgRender ;
			
			scaleSS.config( command = Smoothing_Sharpening )
		
		except Exception :		# or IOError
			# when something wrong with image
			WarningMessage()
		
		
def oCBSave() :
	# save current image
	try :
		cv.imwrite( s.get(), imgCur )
		ShowInfo()
	except Exception :
		ShowWarning()
		
def oCBchangeOB() :
	# buttom to change preserve/black
	global flagOB
	if flagOB == False :
		flagOB = True
		btnOorB.config( text = 'Preserve' )
	else :
		flagOB = False
		btnOorB.config( text = 'Black' )
		
def oCBchangeSS() :
	# buttom to change sharpening/smoothing
	global flagSS
	if flagSS == False :
		flagSS = True
		btnSS.config( text = 'Sharpening' )
		scaleSS.config( from_ = 0 )
	else :
		flagSS = False
		btnSS.config( text = 'Smoothing' )
		scaleSS.config( from_ = 1 )
		
def Gray_Level_Slicing() :
	# change the selected range to 255
	global imgCur
	row,col = imageOri.shape
	imgGLS = np.zeros((row, col),dtype = 'uint8')
	min_range = glsvar1.get()
	max_range = glsvar2.get()
	# get from user input of range
	for i in range ( row ) :
		for j in range ( col ) :
			if imageOri[i,j] > min_range and imageOri[i,j] < max_range :
				imgGLS[i,j] = 255
			else :
				if flagOB == False :	# change to black
					imgGLS[i,j] = 0
				else :					# preserve unchoose value
					imgGLS[i,j] = imageOri[i,j]
	imgCur = imgGLS
	imgGLS = cv.resize( imgCur, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgGLS )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def Bit_Plane_Image() :
	# slice bit wise for bit #0 to bit #8
	global imgCur
	row,col = imageOri.shape
	imgBPI = np.zeros((row, col),dtype = 'uint8')	# initial
	level = np.power( 2, bpivar.get()-1 )			# 2^n-1
	# slicing bit level to white and black
	for i in range ( row ) :
		for j in range ( col ) :
			if imageOri[i,j] & level == 0 :
				imgBPI[i,j] = 0
			else :
				imgBPI[i,j] = 255
	imgCur = imgBPI
	imgBPI = cv.resize( imgCur, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgBPI )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def Smoothing_Sharpening(v) :
	# smoothing or sharpening funtion from user input of buttom
	global imgCur
	if flagSS == False :	# smoothing
		imgSmoo = cv.blur(imageOri, (int(v),int(v)))
		imgCur = imgSmoo
		imgSmoo = cv.resize( imgCur, ( 300,300 ), interpolation = cv.INTER_CUBIC )
		imgRender = Image.fromarray( imgSmoo )
	else :					# sharpening
		kernel = np.array([[-1,-1,-1],
						   [-1, 8,-1],
						   [-1,-1,-1]])
		ori = np.array([[0,0,0],
						[0,1,0],
						[0,0,0]])
		imgSharp = cv.filter2D( imageOri, -1, kernel*int(v)/5+ori )
		imgCur = imgSharp
		imgSharp = cv.resize( imgCur, ( 300,300 ), interpolation = cv.INTER_CUBIC )
		imgRender = Image.fromarray( imgSharp )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def FFT() :
	# Fast Fourier Transform
	global imgCur
	imgFFT = np.fft.fft2( imageOri )
	imgFFT = np.fft.fftshift(imgFFT)	# shift to right way
	imgFFT = 20*np.log( np.abs( imgFFT )+1 )
	# remap by log
	imgCur = imgFFT
	imgFFT = cv.resize( imgCur, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgFFT )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def Phase_Image() :
	# show phase image by invert fft2 phase spectrum
	f = np.fft.fft2( imageOri )
	fshift = np.fft.fftshift( f )
	fre = np.abs(fshift)
	fre = fre.clip( min=1 )
	phase = fshift/fre	# phase = fshift/np.abs(fshift) # np.angle( fshift )
	imgPhase = np.fft.ifft2(np.fft.ifftshift(phase))
	imgPhase = np.abs( imgPhase )
	phase = phase.clip( min=0 )
	
	plt.subplot(121),plt.imshow( np.log10( np.abs(phase)+0.1 ), cmap = 'gray')
	plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow( np.log10( imgPhase+0.01 ), cmap = 'gray')
	plt.title('Phase Image'), plt.xticks([]), plt.yticks([])
	plt.show()
	
def Amplitude_Image() :
	# show amplitude image by invert fft2 amplitude spectrum
	f= np.fft.fft2( imageOri )
	fshift = np.fft.fftshift( f )
	amplitude = np.abs( fshift )
	imgAmplitude = np.fft.ifft2(np.fft.ifftshift(amplitude))
	imgAmplitude = np.abs( imgAmplitude )
	
	plt.subplot(121),plt.imshow( 20*np.log ( amplitude+1 ), cmap = 'gray')
	plt.title('Amplitude Spectrum'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow( 20*np.log( imgAmplitude+1 ), cmap = 'gray')
	plt.title('Amplitude Image'), plt.xticks([]), plt.yticks([])
	plt.show()
	
#--------------------using tkinter GUI-----------------------

imgPanelL = tk.Label( window, width = 300, height = 300 )
imgPanelR = tk.Label( window, width = 300, height = 300 )
oName = tk.Label( window, text = 'Open File : ', width = 10, height = 1 )
sName = tk.Label( window, text = 'Save File : ', width = 10, height = 1 )
o = tk.Entry( window )
s = tk.Entry( window )
btnOpen = tk.Button( window, width = 10, height = 1, 
					 text = 'open / reset', command = oCBOpen )
btnSave = tk.Button( window, width = 10, height = 1,
					 text = 'save', command = oCBSave )
labelGLS = tk.Label( window, text = 'Gray-level slicing', width = 15, height = 1 )
labelBPI = tk.Label( window, text = 'Bit-Plane images', width = 15, height = 1 )
btnSS = tk.Button( window, width = 10, height = 1, 
					 text = 'Smoothing', command = oCBchangeSS )
labelrange1 = tk.Label( window, text = 'range from : ',
						width = 10, height = 1, fg = 'gray35' )
labelrange2 = tk.Label( window, text = 'to : ', width = 10, height = 1, fg = 'gray35' )
labelOB = tk.Label( window, text = 'unselected area : ',
					width = 15, height = 1, fg = 'gray35' )
btnOorB = tk.Button( window, width = 10, height = 1, 
					 text = 'Black', command = oCBchangeOB )
btnGLSshow = tk.Button( window, width = 10, height = 1,
						text = 'show', command = Gray_Level_Slicing ) 
btnBPIshow = tk.Button( window, width = 10, height = 1, 
						text = 'show', command = Bit_Plane_Image ) 
spinboxGLS1 = tk.Spinbox( window, width = 10, from_ = 0, to = 255,
						  textvariable = glsvar1 )
spinboxGLS2 = tk.Spinbox( window, width = 10, from_ = 0, to = 255, 
						  textvariable = glsvar2 )
labelshowbpi = tk.Label( window, text = 'show bit-plane : ',
						width = 15, height = 1, fg = 'gray35' )
radiobtn1 = tk.Radiobutton( window, text = '1', variable = bpivar, value = 1 ) 
radiobtn2 = tk.Radiobutton( window, text = '2', variable = bpivar, value = 2 ) 
radiobtn3 = tk.Radiobutton( window, text = '3', variable = bpivar, value = 3 ) 
radiobtn4 = tk.Radiobutton( window, text = '4', variable = bpivar, value = 4 ) 
radiobtn5 = tk.Radiobutton( window, text = '5', variable = bpivar, value = 5 ) 
radiobtn6 = tk.Radiobutton( window, text = '6', variable = bpivar, value = 6 ) 
radiobtn7 = tk.Radiobutton( window, text = '7', variable = bpivar, value = 7 ) 
radiobtn8 = tk.Radiobutton( window, text = '8', variable = bpivar, value = 8 ) 
scaleSS = tk.Scale( window, orient = tk.HORIZONTAL, length = 630, width = 10, showvalue = 0, from_ = 1, to = 10 ) 
labelFFT = tk.Label( window, text = 'FFT image', width = 15, height = 1 )
labelAP = tk.Label( window, text = 'Amplitude/Phase', width = 15, height = 1 )
btnFFTshow = tk.Button( window, width = 20, height = 1, 
						text = 'Display FFT image', command = FFT ) 
btnAmplitudeshow = tk.Button( window, width = 20, height = 1, 
						text = 'Display Amplitude image', command = Amplitude_Image ) 
btnPhaseshow = tk.Button( window, width = 20, height = 1, 
						text = 'Display Phase image', command = Phase_Image ) 


imgPanelL.place( x = 120, y = 40 )
imgPanelR.place( x = 450, y = 40 )
oName.place( x = 30, y = 5 )
sName.place( x = 360, y = 5 )
o.place( x = 120, y = 5 )
s.place( x = 450, y = 5 )
btnOpen.place( x = 10 , y = 40 ) 
btnSave.place( x = 10 , y = 80 ) 
labelGLS.place( x = 10, y = 350 )
labelBPI.place( x = 10, y = 390 )
btnSS.place( x = 10, y = 430 )
labelrange1.place( x = 120, y = 350 )
labelrange2.place( x = 270, y = 350 )
labelOB.place( x = 420, y = 350 )
btnOorB.place( x = 540, y = 350 )
btnGLSshow.place( x = 655, y = 350 )
btnBPIshow.place( x = 655, y = 390 )
spinboxGLS1.place( x = 200, y = 350 )
spinboxGLS2.place( x = 320, y = 350 )
labelshowbpi.place( x = 120, y = 390 )
radiobtn1.place( x = 220, y = 390 )
radiobtn2.place( x = 260, y = 390 )
radiobtn3.place( x = 300, y = 390 )
radiobtn4.place( x = 340, y = 390 )
radiobtn5.place( x = 380, y = 390 )
radiobtn6.place( x = 420, y = 390 )
radiobtn7.place( x = 460, y = 390 )
radiobtn8.place( x = 500, y = 390 )
scaleSS.place ( x = 120, y = 430 )
labelFFT.place( x = 10, y = 470 )
labelAP.place( x = 10, y = 510 )
btnFFTshow.place( x = 120, y = 470 )
btnAmplitudeshow.place( x = 120, y = 510 )
btnPhaseshow.place( x = 300, y = 510 )

#--------------------using tkinter GUI-----------------------

window.geometry( "800x600" )
window.mainloop()

