import cv2
import numpy as np

def abs_sobel_thresh(image, orient='x', sobel_kernel=3, thresh=(0, 255)):
    """
    Calculate directional gradient
    Apply threshold
    
    Arguments:
        image - grayscale or otherwise single channel image
        orient - 'x' or 'y', determines which derivative to take.
        sobel_kernel - integer for kernel size
        thresh - tuple with a lower and an upper threshold; integer values 0-255.
    
    Returns:
        Thesholded image
    """
    # Calculate the derivative in the x-direction (the 1, 0 at the end denotes x-direction):
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    # Calculate the derivative in the y-direction (the 0, 1 at the end denotes y-direction):
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=sobel_kernel)

    if(orient == 'x'):
        sobel = sobelx
    else:
        sobel = sobely
        
    # Calculate the absolute value of the x-derivative:    
    abs_sobel = np.absolute(sobel)
    #Convert the absolute value image to 8-bit:
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))

    thresh_min = thresh[0]
    thresh_max = thresh[1]
    grad_binary = np.zeros_like(scaled_sobel)
    grad_binary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    
    return grad_binary

def mag_thresh(image, sobel_kernel=3, thresh=(30, 150)):
    """
    Calculate gradient magnitude
    Apply threshold
    
    Arguments:
        image - grayscale or otherwise single channel image
        sobel_kernel - integer for kernel size
        thresh - tuple with a lower and an upper threshold; integer values 0-255.
    
    Returns:
        Thesholded image
    """
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    sobelxy = np.sqrt(sobelx**2 + sobely**2)
    
    abs_sobelxy = np.absolute(sobelxy)
    
    scaled_sobel = np.uint8(255*abs_sobelxy/np.max(abs_sobelxy))
    
    thresh_min = thresh[0]
    thresh_max = thresh[1]
    mag_binary = np.zeros_like(scaled_sobel)
    mag_binary[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1
    
    return mag_binary

def dir_threshold(image, sobel_kernel=15, thresh=(0.7, 1.2)):
    """
    Calculate gradient direction
    Apply threshold
    
    Arguments:
        image - grayscale or otherwise single channel image
        sobel_kernel - integer for kernel size
        mag_thresh - tuple with a lower and an upper threshold; values 0-2pi.
    
    Returns:
        Thesholded image
    """
    sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    direction = np.arctan2(abs_sobely,abs_sobelx)
    dir_binary = np.zeros_like(direction)
    dir_binary[(direction >= thresh[0]) & (direction <= thresh[1])] = 1
    
    return dir_binary

def hls_select(image, thresh=None):
    """
    1) Convert an image to HLS color space
    2) If thresh is provided,
       apply a threshold to the S channel using the tuple thresh
    
    Returns a binary image or the saturation channel.
    """
    # 1) Convert to HLS color space
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    S = hls[:,:,2]
    if thresh == None:
        return S
    # 2) Apply a threshold to the S channel
    binary = np.zeros_like(S)
    binary[(S <= thresh[0]) | (S > thresh[1])] = 1
    # 3) Return a binary image of threshold result
    return binary
