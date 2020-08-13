from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
#from tkinter import ttk

window = tk.Tk()					# create window
window.title( 'B063040061 hw3' )	# name title

flagOpen = False					# file open flag
flagOB = False						# preserve/black flag
flagSS = False						# smoothing/sharpening
rL = tk.DoubleVar()				# gray level slicing varible
rH = tk.DoubleVar()				# ''
c = tk.DoubleVar()				# gray level slicing varible
d0 = tk.DoubleVar()				# ''
colorVar = tk.IntVar()				# bit plane image varible
HSIVar = tk.IntVar()				# bit plane image varible


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
			#imageOri = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB ) 
			
			if ( o.get() == "Fig0460a.tif" ) :
				image = cv.resize( imageOri, ( 192,300 ),interpolation = cv.INTER_CUBIC )
			else :
				image = cv.resize( imageOri, ( 300,300 ),interpolation = cv.INTER_CUBIC )
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
		
def HomoF() :
	# as user input
	rL_ = rL.get()
	rH_ = rH.get()
	c_ = c.get()
	d0_ = d0.get()
	# as user input
	I = cv.cvtColor( imageOri, cv.COLOR_BGR2GRAY )
	#I = cv2.imread( 'Fig0460a.tif', cv2.IMREAD_GRAYSCALE )#[:, :, 0]
	'''
	plt.imshow( np.uint8(I) )
	plt.show()
	'''
	# step 1, 取log(x+1)
	I_log = np.log1p(np.array(I, dtype="float"))
	
	# step 2, DFT
	I_fft = np.fft.fft2(I_log)

	# step 3, caculate H(u,v) = ( rh-rl )[1-e^(cD^2(u,v)/D0^2)+rl // textbook #4-174
	I_shape = I_fft.shape
	P = I_shape[0]/2
	Q = I_shape[1]/2
	H = np.zeros(I_shape)
	U, V = np.meshgrid(range(I_shape[0]), range(I_shape[1]), sparse=False, indexing='ij')
	Duv = np.sqrt((((U-P)**2+(V-Q)**2))).astype(float)
	H = np.exp((-c_*(Duv**2)/(d0_**2)))
	#H = 1 - H
	H = (rH_-rL_)*(1-H)+rL_
	'''
	plt.imshow( np.uint8(H) )
	plt.show()
	'''
	H = np.fft.fftshift(H)
	I_filtered = H*I_fft

	# step 4, (DFT)^-1
	I_filt = np.fft.ifft2(I_filtered)
	
	# step 5, 取exp(x)+1
	I = np.exp(np.real(I_filt))-1
	I = np.uint8( I )
	
	# Histogram equalization
	equ = cv.equalizeHist( I )
	#I = np.hstack((I, equ))
	
	# show at left panel with image Homo filter
	imgHomo = cv.resize( I, ( 192,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgHomo )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	#return np.uint8(I)
	#cv2.imshow( np.uint8(I) )
	
	# show at right panel with image Homo filter and histogram equalization
	imgHomoHis = cv.resize( equ, ( 192,300 ), interpolation = cv.INTER_CUBIC )
	imgRender2 = Image.fromarray( imgHomoHis )
	#edged = Image.fromarray( edged )
	imgRender2 = ImageTk.PhotoImage( imgRender2 )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelR.config( image = imgRender2 )
	imgPanelR.image = imgRender2 ;
	
def ShowRGB() :

	imgRGB = imageOri.copy()
	if colorVar.get() == 1 :
		# set blue and green channels to 0
		imgRGB[ :, :, 0 ] = 0
		imgRGB[ :, :, 1 ] = 0
	elif colorVar.get() == 2 :
		# # set blue and red channels to 0
		imgRGB[ :, :, 0 ] = 0
		imgRGB[ :, :, 2 ] = 0
	else :
		# set green and red channels to 0
		imgRGB[ :, :, 1 ] = 0
		imgRGB[ :, :, 2 ] = 0
	imgRGB = cv.cvtColor( imgRGB, cv.COLOR_BGR2RGB )
	imgRGB = cv.resize( imgRGB, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgRGB )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def ShowHSI() :

	imgHSI = cv.cvtColor( imageOri, cv.COLOR_BGR2HSV )
	# get HSI component
	if HSIVar.get() == 1 :
		imgHSI = imgHSI[:,:,0]
	elif HSIVar.get() == 2 :
		imgHSI = imgHSI[:,:,1]
	else :
		imgHSI = imgHSI[:,:,2]
	
	imgHSI = cv.resize( imgHSI, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgHSI )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def ColorComplement() :
	
	imgCPL = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB )
	# RGB color complement with 255-x
	imgCPL[:,:,0] = 255-imgCPL[:,:,0]
	imgCPL[:,:,1] = 255-imgCPL[:,:,1]
	imgCPL[:,:,2] = 255-imgCPL[:,:,2]
	
	imgCPL = cv.resize( imgCPL, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgCPL )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
def Smoothing() :
	
	imgOri = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB )
	# smoothing with 5x5 kernel
	kernel = np.ones( ( 5, 5 ), np.float32 )/25
	imgSm = cv.filter2D( imgOri, -1, kernel )
	
	# image different with opencv substract
	imgDiff = cv.subtract( imgOri, imgSm )
	
	imgSm = cv.resize( imgSm, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgSm )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
	imgDiff = cv.resize( imgDiff, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender2 = Image.fromarray( imgDiff )
	#edged = Image.fromarray( edged )
	imgRender2 = ImageTk.PhotoImage( imgRender2 )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelR.config( image = imgRender2 )
	imgPanelR.image = imgRender2 ;
	
def Sharpening() :

	imgOri = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB )
	#imgSh = cv.Laplacian( imgOri, ddepth = cv.CV_16S, ksize = 5 )
	#imgSh = imgOri+np.uint8(imgSh)
	# sharpening with laplacian kernel
	kernel = np.array([[-1,-1,-1],
					   [-1, 8,-1],
					   [-1,-1,-1]])
	ori = np.array([[0,0,0],
					[0,1,0],
					[0,0,0]])
	imgSh = cv.filter2D( imgOri, -1, kernel+ori )
	
	# image different with opencv substract
	imgDiff = cv.subtract( imgOri, imgSh )
	
	imgSh = cv.resize( imgSh, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgSh )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
	
	imgDiff = cv.resize( imgDiff, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender2 = Image.fromarray( imgDiff )
	#edged = Image.fromarray( edged )
	imgRender2 = ImageTk.PhotoImage( imgRender2 )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelR.config( image = imgRender2 )
	imgPanelR.image = imgRender2 ;
	
def FeatherSlicing() :
	
	imgHSI = cv.cvtColor( imageOri, cv.COLOR_BGR2HSV )
	imgOri = cv.cvtColor( imageOri, cv.COLOR_BGR2RGB )
	# slicing hue in the main
	from_HSI = ( 100, 0, 0 )
	to_HSI = ( 170, 255, 255 )
	mask = cv.inRange( imgHSI, from_HSI, to_HSI )
	result = cv.bitwise_and( imgOri, imgOri, mask = mask )
	
	# slicing with the darkness feather 
	from_B = ( 100, 150, 0 )
	to_B = ( 170, 255, 255 )
	maskB = cv.inRange( imgHSI, from_B, to_B )
	resultB = cv.bitwise_and( imgOri, imgOri, mask = maskB )

	final_mask = mask-maskB			# mask minus = image xor
	final_result = cv.bitwise_and( imgOri, imgOri, mask = final_mask )
	
	imgFeather = cv.resize( final_result, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgFeather )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelL.config( image = imgRender )
	imgPanelL.image = imgRender ;
	
	imgFR = cv.resize( result, ( 300,300 ), interpolation = cv.INTER_CUBIC )
	imgRender = Image.fromarray( imgFR )
	#edged = Image.fromarray( edged )
	imgRender = ImageTk.PhotoImage( imgRender )
	#edged = ImageTk.PhotoImage( edged )

	imgPanelR.config( image = imgRender )
	imgPanelR.image = imgRender ;
	
	
	plt.subplot( 2, 2, 1 )
	plt.imshow( imgOri )
	plt.title('original'), plt.xticks([]), plt.yticks([])
	
	plt.subplot( 2, 2, 2 )
	plt.imshow( result )
	plt.title('slicing hue'), plt.xticks([]), plt.yticks([])

	plt.subplot( 2, 2, 3 )
	plt.imshow( resultB )
	plt.title('slicing hue+saturation'), plt.xticks([]), plt.yticks([])

	plt.subplot( 2, 2, 4 )
	plt.imshow( final_result )
	plt.title('arithmetic xor'), plt.xticks([]), plt.yticks([])
	
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
					 
lblHomo = tk.Label( window, text = 'Homomorphic', width = 15, height = 1 )
lblRL = tk.Label( window, text = 'rL : ', width = 5, height = 1 )
lblRH = tk.Label( window, text = 'rH : ', width = 5, height = 1 )
lblC = tk.Label( window, text = 'c : ', width = 5, height = 1 )
lblD0 = tk.Label( window, text = 'D0 : ', width = 5, height = 1 )
spinboxRL = tk.Spinbox( window, width = 10, from_ = 0, to = 255,
						  textvariable = rL )
spinboxRH = tk.Spinbox( window, width = 10, from_ = 0, to = 255, 
						  textvariable = rH )
spinboxC = tk.Spinbox( window, width = 10, from_ = 0, to = 255,
						  textvariable = c )
spinboxD0 = tk.Spinbox( window, width = 10, from_ = 0, to = 255, 
						  textvariable = d0 )
btnShowHomo = tk.Button( window, width = 10, height = 1, text = 'show', command = HomoF )

lblRGB = tk.Label( window, text = 'R/G/B', width = 15, height = 1 )
radiobtnR = tk.Radiobutton( window, text = 'Red', variable = colorVar, value = 1 ) 
radiobtnG = tk.Radiobutton( window, text = 'Green', variable = colorVar, value = 2 ) 
radiobtnB = tk.Radiobutton( window, text = 'Blue', variable = colorVar, value = 3 ) 
btnShowRGB = tk.Button( window, width = 10, height = 1, text = 'show',command = ShowRGB )

lblHSI = tk.Label( window, text = 'H/S/I', width = 15, height = 1 )
radiobtnH = tk.Radiobutton( window, text = 'Hue', variable = HSIVar, value = 1 ) 
radiobtnS = tk.Radiobutton( window, text = 'Saturation', variable = HSIVar, value = 2 ) 
radiobtnI = tk.Radiobutton( window, text = 'Intensity', variable = HSIVar, value = 3 ) 
btnShowHSI = tk.Button( window, width = 10, height = 1, text = 'show',command = ShowHSI )

lblComplement = tk.Label( window, text = 'color complement', width = 15, height = 1 )
btnComplement = tk.Button( window, width = 10, height = 1, text = 'complement',command = ColorComplement )

lblSMSH = tk.Label( window, text = 'smooth/sharpen', width = 15, height = 1 )
btnSM = tk.Button( window, width = 10, height = 1, text = 'smoothing',command = Smoothing )
btnSH = tk.Button( window, width = 10, height = 1, text = 'sharpening',command = Sharpening )

lblSliF = tk.Label( window, text = 'slicing', width = 15, height = 1 )
btnSliF = tk.Button( window, width = 10, height = 1, text = 'show feather',command = FeatherSlicing )

# ------------------------------------------------

imgPanelL.place( x = 120, y = 40 )
imgPanelR.place( x = 450, y = 40 )
oName.place( x = 30, y = 5 )
sName.place( x = 360, y = 5 )
o.place( x = 120, y = 5 )
s.place( x = 450, y = 5 )
btnOpen.place( x = 10 , y = 40 ) 
btnSave.place( x = 10 , y = 80 ) 

lblHomo.place( x = 10, y = 350 )
lblRL.place( x = 120, y = 350 )
lblRH.place( x = 240, y = 350 )
lblC.place( x = 360, y = 350 )
lblD0.place( x = 480, y = 350 )
spinboxRL.place( x = 150, y = 350 )
spinboxRH.place( x = 270, y = 350 )
spinboxC.place( x = 390, y = 350 )
spinboxD0.place( x = 510, y = 350 )
btnShowHomo.place( x = 655, y = 350 )

lblRGB.place( x = 10, y = 390 )
radiobtnR.place( x = 120, y = 390 ) 
radiobtnG.place( x = 240, y = 390 ) 
radiobtnB.place( x = 360, y = 390 ) 
btnShowRGB.place( x = 655, y = 390 )

lblHSI.place( x = 10, y = 430 )
radiobtnH.place( x = 120, y = 430 ) 
radiobtnS.place( x = 240, y = 430 ) 
radiobtnI.place( x = 360, y = 430 ) 
btnShowHSI.place( x = 655, y = 430 )

lblComplement.place( x = 10, y = 470 )
btnComplement.place( x = 120, y = 470 )

lblSMSH.place( x = 10, y = 510 )
btnSM.place( x = 120, y = 510 )
btnSH.place( x = 240, y = 510 )

lblSliF.place( x = 10, y = 550 )
btnSliF.place( x = 120, y = 550 )

#--------------------using tkinter GUI-----------------------

window.geometry( "800x600" )
window.mainloop()

