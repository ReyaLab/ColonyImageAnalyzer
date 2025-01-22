# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:50:34 2025

@author: mchva
"""



def point_in_rect(x,y, bounds):
    if len(bounds) < 4:
        return(False)
    elif ((bounds[0] <= x <= bounds[2]) and (bounds[1] <= y <= bounds[3])):
        return(True)
    else:
        return(False)
    
def main(args):
    import numpy as np
    import cv2
    path = args[3]
    file = args[4]
    filename = path+file
    size_cap = args[0]
    size_min = args[1]
    circ_min = args[2]
    LQP_cutoff = args[5]
    necrotic_px_std_cutoff = args[6]
    necrotic_circ_min = args[7]
    live_px_std_cutoff = args[8]
    lowest_pix_max = args[9]
    
    import pandas as pd
    Parameters = pd.DataFrame(columns=['Size Cap','Size Min','Circularity cutoff','Lowest Quartile Pixel Cutoff', "Necrotic circularity cutoff", "Nec Pixel Std > cutoff", "Live Pixel Std < cutoff", "Colony lowest pixel max"])
    Parameters.loc[0]= [size_cap, size_min, circ_min, LQP_cutoff, necrotic_circ_min, necrotic_px_std_cutoff, live_px_std_cutoff, lowest_pix_max]
    

    img = cv2.imread(filename)
    
    img = cv2.GaussianBlur(img, (5,5), 0)
    
    #add an arbitrary white border around image so colonies on edge of image aren't cut off
    img = cv2.copyMakeBorder(img,top=10, bottom=10,left=10,right=10, borderType=cv2.BORDER_CONSTANT,  value=[255, 255, 255])  
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    
    thresh_colonies = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 1)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours1 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        perimeter = cv2.arcLength(contour, True)

        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]    
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area > size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):  
            filtered_contours1.append(contour)
    filtered_contours1 = tuple(filtered_contours1)
    
    
    thresh_colonies = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 101, 5)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours2 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        perimeter = cv2.arcLength(contour, True)
    
        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]    
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area > size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):  
            filtered_contours2.append(contour)
    filtered_contours2 = tuple(filtered_contours2)
    
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours1, -1, (255, 255, 255), thickness=cv2.FILLED)
    filtered_contours2B =[]
    for contour in filtered_contours2:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            filtered_contours2B.append(contour)
    filtered_contours2B = tuple(filtered_contours2B)
    filtered_contours2B = filtered_contours2B + filtered_contours1
    del filtered_contours1, filtered_contours2
    
    
    ret,thresh_colonies = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours3 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        perimeter = cv2.arcLength(contour, True)
    
        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]    
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area >size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):  # Close to 1 for a circular shape
            filtered_contours3.append(contour)
    filtered_contours3 = tuple(filtered_contours3)
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours2B, -1, (255, 255, 255), thickness=cv2.FILLED)
    filtered_contours3B =[]
    for contour in filtered_contours3:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            filtered_contours3B.append(contour)
    filtered_contours3B = tuple(filtered_contours3B)
    
    filtered_contours3B = filtered_contours3B + filtered_contours2B
    del filtered_contours2B, filtered_contours3
    
    
    ret,thresh_colonies = cv2.threshold(gray,115,255,cv2.THRESH_BINARY)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours4 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        perimeter = cv2.arcLength(contour, True)
    
        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]    
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area >size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):  # Close to 1 for a circular shape
            filtered_contours4.append(contour)
    filtered_contours4 = tuple(filtered_contours4)
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours3B, -1, (255, 255, 255), thickness=cv2.FILLED)
    filtered_contours4B =[]
    for contour in filtered_contours4:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            filtered_contours4B.append(contour)
    filtered_contours4B = tuple(filtered_contours4B)
    
    filtered_contours4B = filtered_contours4B + filtered_contours3B
    del filtered_contours4, filtered_contours3B
    
    # cv2.drawContours(img, final_contours, -1, (0,0,255), 2)
    
    # cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('custom window', img)
    # cv2.resizeWindow('custom window', 600, 600)
    # cv2.waitKey(0)
    
    ret,thresh_colonies = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours5 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        perimeter = cv2.arcLength(contour, True)
    
        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]    
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area >size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):  # Close to 1 for a circular shape
            filtered_contours5.append(contour)
    filtered_contours5 = tuple(filtered_contours5)
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours4B, -1, (255, 255, 255), thickness=cv2.FILLED)
    filtered_contours5B =[]
    for contour in filtered_contours5:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            filtered_contours5B.append(contour)
    filtered_contours5B = tuple(filtered_contours5B)
    
    filtered_contours5B = filtered_contours5B + filtered_contours4B
    del filtered_contours5, filtered_contours4B
    
    img2 = cv2.imread(filename)
    img2 = cv2.GaussianBlur(img2, (5,5), 0)
    #add an arbitrary dark border around image so colonies on edge of image aren't cut off
    img2 = cv2.copyMakeBorder(img2,top=10, bottom=10,left=10,right=10, borderType=cv2.BORDER_CONSTANT,  value=[60, 60, 60])  
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    thresh_colonies = cv2.adaptiveThreshold(gray2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 11)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    del gray2, thresh_colonies
    filtered_contours6 = []
    for contour in contours_colonies:
        if not cv2.isContourConvex(contour):
            # Calculate the arc length of the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust 0.02 as needed
            approx = cv2.approxPolyDP(contour, epsilon, True)  # True for closed contours
            # Optional: Replace the original contour with the approximated one
            contour = approx
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img2, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img2[mask == 255]
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area >size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):
            filtered_contours6.append(contour)
    filtered_contours6 = tuple(filtered_contours6)
    del img2
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours5B, -1, (255, 255, 255), thickness=cv2.FILLED)
    filtered_contours6B =[]
    for contour in filtered_contours6:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            filtered_contours6B.append(contour)
    filtered_contours6B = tuple(filtered_contours6B)
    
    filtered_contours6B = filtered_contours6B + filtered_contours5B
    del filtered_contours5B, filtered_contours6
    
    thresh_colonies = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 11)
    contours_colonies,h = cv2.findContours(thresh_colonies, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    filtered_contours7 = []
    for contour in contours_colonies:
        area = cv2.contourArea(contour)
        if (area < .4*size_min):
            continue
        if not cv2.isContourConvex(contour):
            # Calculate the arc length of the contour
            #epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust 0.02 as needed
            #approx = cv2.approxPolyDP(contour, epsilon, True)  # True for closed contours
            # Optional: Replace the original contour with the approximated one
            approx = cv2.convexHull(contour)

            contour = approx
            area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Avoid division by zero and ensure valid contour area
        if perimeter == 0 or area == 0:
            continue
        # Calculate circularity
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        mask = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = img[mask == 255]
        # Calculate the variance of pixel intensities
        # Threshold for circularity (adjust as needed)
        pix_var = np.std(pixels_inside_contour)
        if pix_var < live_px_std_cutoff:
            continue
        if (circularity > circ_min) and (area >size_min)  and (area <size_cap) and np.any(pixels_inside_contour <= lowest_pix_max) and (np.percentile(pixels_inside_contour,25)<LQP_cutoff):
            filtered_contours7.append(contour)
    filtered_contours7 = tuple(filtered_contours7)
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, filtered_contours6B, -1, (255, 255, 255), thickness=cv2.FILLED)
    final_contours =[]
    for contour in filtered_contours7:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            final_contours.append(contour)
    final_contours = tuple(final_contours)
    
    final_contours = final_contours + filtered_contours6B
    del filtered_contours6B, filtered_contours7
    
    
    ret,thresh_necrosis = cv2.threshold(gray,55,255,cv2.THRESH_BINARY)
    contours_necrosis,h = cv2.findContours(thresh_necrosis, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts_app =[]
    for i, contour in enumerate(contours_necrosis):
        if not cv2.isContourConvex(contour):
            # Calculate the arc length of the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust 0.02 as needed
            approx = cv2.approxPolyDP(contour, epsilon, True)  # True for closed contours
            # Optional: Replace the original contour with the approximated one
            contour = approx
        mask = np.zeros_like(gray, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        
        # Get the pixel values inside the contour
        pixels_inside_contour = gray[mask == 255]
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if (perimeter == 0):
            continue
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        # Check if any pixel meets the threshold conditions
        if np.any(pixels_inside_contour >= 125) or (np.std(pixels_inside_contour)>necrotic_px_std_cutoff) or (np.mean(pixels_inside_contour) >85) or (area<300) or (circularity< necrotic_circ_min):
            continue
        else: 
            cnts_app.append(contour)  
    contours_necrosis = tuple(cnts_app)
    
    ret,thresh_necrosis = cv2.threshold(gray,72,255,cv2.THRESH_BINARY)
    contours_necrosis2,h = cv2.findContours(thresh_necrosis, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts_app =[]
    for i, contour in enumerate(contours_necrosis2):
        if not cv2.isContourConvex(contour):
            # Calculate the arc length of the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust 0.02 as needed
            approx = cv2.approxPolyDP(contour, epsilon, True)  # True for closed contours
            # Optional: Replace the original contour with the approximated one
            contour = approx
        mask = np.zeros_like(gray, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = gray[mask == 255]
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if (perimeter == 0):
            continue
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        # Check if any pixel meets the threshold condition
        if np.any(pixels_inside_contour >= 125) or (np.std(pixels_inside_contour)>necrotic_px_std_cutoff) or (np.mean(pixels_inside_contour) >85) or (area<300) or (circularity< necrotic_circ_min):
            continue
        else:
            cnts_app.append(contour)  
    contours_necrosis2 = tuple(cnts_app)
    
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, contours_necrosis, -1, (255, 255, 255), thickness=cv2.FILLED)
    contours_necrosis2B =[]
    for contour in contours_necrosis2:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            contours_necrosis2B.append(contour)
    contours_necrosis2B = tuple(contours_necrosis2B)
    contours_necrosis = contours_necrosis + contours_necrosis2B
    del contours_necrosis2B

    ret,thresh_necrosis = cv2.threshold(gray,78,255,cv2.THRESH_BINARY)
    contours_necrosis3,h = cv2.findContours(thresh_necrosis, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnts_app =[]
    for i, contour in enumerate(contours_necrosis3):
        if not cv2.isContourConvex(contour):
            # Calculate the arc length of the contour
            epsilon = 0.02 * cv2.arcLength(contour, True)  # Adjust 0.02 as needed
            approx = cv2.approxPolyDP(contour, epsilon, True)  # True for closed contours
            # Optional: Replace the original contour with the approximated one
            contour = approx
        mask = np.zeros_like(gray, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)
        # Get the pixel values inside the contour
        pixels_inside_contour = gray[mask == 255]
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        if (perimeter == 0):
            continue
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        # Check if any pixel meets the threshold condition
        if np.any(pixels_inside_contour >= 125) or (np.std(pixels_inside_contour)>necrotic_px_std_cutoff) or (np.mean(pixels_inside_contour) >85) or (area<300) or (circularity< necrotic_circ_min):
            continue
        else:
            cnts_app.append(contour)  
    contours_necrosis3 = tuple(cnts_app)
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, contours_necrosis, -1, (255, 255, 255), thickness=cv2.FILLED)
    contours_necrosis3B =[]
    for contour in contours_necrosis3:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            continue
        else:
            contours_necrosis3B.append(contour)
    contours_necrosis3B = tuple(contours_necrosis3B)
    contours_necrosis = contours_necrosis + contours_necrosis3B
    del contours_necrosis3B, contours_necrosis3
    
    #temp
    # img2 = img.copy()
    # cv2.drawContours(img2, contours_necrosis, -1, (0, 0, 255), 2)
    # cv2.namedWindow(file, cv2.WINDOW_KEEPRATIO)
    # cv2.imshow(file, img2)
    # cv2.resizeWindow(file, 600, 600)
    # cv2.waitKey(0)
    # del img2
    #temp end
    

    Colonies = pd.DataFrame(columns=['Area','Mean Intensity','Necrosis Area','Bounds','Centroid', "Lower Quartile Pixel", "Percent Necrosis", "Contour"])
    for i in range(len(final_contours)):
        area = cv2.contourArea(final_contours[i])
        M = cv2.moments(final_contours[i])
        if M["m00"] != 0:  # Avoid division by zero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
         # Calculate mean intensity inside the contour
        x, y, w, h = cv2.boundingRect(final_contours[i])
        mean_intensity = cv2.mean(img[y:y+h, x:x+w])[0]
        min_pix = np.percentile(img[y:y+h, x:x+w], 25)
        Colonies.loc[len(Colonies)] = [area, mean_intensity, 0, [x,y,x+w, y+h], [cX, cY], min_pix, 0, final_contours[i]]
        del area, M, cX, cY, mean_intensity, x, y, w, h, min_pix
    del final_contours
    
    Colonies = Colonies[Colonies["Lower Quartile Pixel"] < LQP_cutoff]
    Colonies.index = range(len(Colonies.index))
    Colonies2 = pd.DataFrame(columns=['Area','Mean Intensity','Necrosis Area','Bounds','Centroid', "Lower Quartile Pixel", "Percent Necrosis", "Contour"])
    for i in range(len(Colonies)):
        external = True
        for j in range(len(Colonies)):
            if i == j:
                continue
            if point_in_rect(Colonies["Centroid"][i][0], Colonies["Centroid"][i][1], Colonies["Bounds"][j]):
                if (Colonies["Area"][i] < Colonies["Area"][j]):
                    external = False
                    break
        if external == True:
            Colonies2.loc[len(Colonies2)] = Colonies.loc[i]
        else:
            continue
    Colonies = Colonies2
    del Colonies2
    Colonies = Colonies.sort_values(by=['Area'], ascending=False)
    Colonies.index = range(len(Colonies.index))
    
    mask = np.zeros_like(img, dtype=np.uint8)
    cv2.drawContours(mask, Colonies["Contour"], -1, (255, 255, 255), thickness=cv2.FILLED)
    contours_necrosis_f =[]
    for contour in contours_necrosis:
        mask2 = np.zeros_like(img, dtype=np.uint8)
        cv2.drawContours(mask2, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
        overlap_mask = cv2.bitwise_and(mask, mask2)
        # If the overlap mask has any non-zero pixels, the contours overlap
        if np.any(overlap_mask):
            contours_necrosis_f.append(contour)
        else:
            continue
    contours_necrosis_f = tuple(contours_necrosis_f)
    del contours_necrosis, mask, mask2, approx, circularity, cnts_app, contour, contours_colonies,epsilon, i, overlap_mask
    del perimeter, ret, pixels_inside_contour, thresh_necrosis, gray
    
    
    for i in range(len(contours_necrosis_f)):
        M = cv2.moments(contours_necrosis_f[i])
        if M["m00"] != 0:  # Avoid division by zero
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        for j in range(len(Colonies)):
            if point_in_rect(cX, cY, Colonies["Bounds"][j]):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                mask1 = np.zeros_like(gray, dtype=np.uint8)
                mask2 = np.zeros_like(gray, dtype=np.uint8)

                # Draw the outer contour on the mask and fill it
                cv2.drawContours(mask1,[Colonies["Contour"][j]], -1, 255, thickness=-1)
                cv2.drawContours(mask2,[contours_necrosis_f[i]], -1, 255, thickness=-1)
                
                overlap_mask = cv2.bitwise_and(mask1, mask2)
                filtered_contour = [point for point in contours_necrosis_f[i] if overlap_mask[point[0][1], point[0][0]] == 255]
                if len(filtered_contour) < 1:
                    break
                filtered_contour = np.array(filtered_contour)

                area = cv2.contourArea(filtered_contour)

                # Calculate the area
                Colonies["Necrosis Area"][j] = Colonies["Necrosis Area"][j] + area
                Colonies["Percent Necrosis"][j] = Colonies["Necrosis Area"][j]/Colonies["Area"][j]
                cv2.drawContours(img, [filtered_contour], -1, (0, 0, 255), 2)
                break
    try:
        del i,j, M, cX, cY
    except:
        pass
    
    for i in range(len(Colonies)): 
        cv2.drawContours(img, [Colonies["Contour"][i]], -1, (0, 255, 0), 2)
        cv2.putText(img, str(Colonies.index[i]+1), tuple(Colonies["Centroid"][i]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
    try:
        del area, i
    except:
        pass
    
    total_area_dark = sum(Colonies["Necrosis Area"])
    total_area_light = sum(Colonies["Area"])
    ratio = total_area_dark/(abs(total_area_light)+1)
    print("total area dark: "+str(total_area_dark))
    print("total area light: "+str(total_area_light))
    print("ratio: "+str(ratio))
    
    caption = np.ones((150, 2068, 3), dtype=np.uint8) * 255  # Multiply by 255 to make it white
    cv2.putText(caption, "Total area necrotic: "+str(total_area_dark)+ ", Total area living: "+str(total_area_light)+", Ratio: "+str(ratio), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
    cv2.putText(caption, "Max size cutoff: "+str(size_cap)+ ", Min size cutoff: "+str(size_min)+", Circularity cutoff: "+str(circ_min), (40, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    try:
        f = open(path + "All_Mari_Imaging_results.csv", mode="r")
        f = open(path + "All_Mari_Imaging_results.csv", mode="a")
        f.write(file+","+str(total_area_light)+","+str(total_area_dark)+","+str(ratio)+"\n")
        f.close()   
    except:
        f= open(path + "All_Mari_Imaging_results.csv", mode="w")
        f.write("Picture name, Living colony area, Necrotic area, Necrotic/Living\n")
        f.write(file+","+str(total_area_light)+","+str(total_area_dark)+","+str()+"\n")
        f.close()
    del f
    
    Colonies = Colonies.drop('Contour', axis=1)
    Colonies.insert(loc=0, column="Colony Number", value=[str(x) for x in range(1, len(Colonies)+1)])
    Colonies.loc[len(Colonies)] = ["Total", total_area_light, None, total_area_dark, None, None, None, ratio]
    

    with pd.ExcelWriter(path + file+"_results.xlsx") as writer:
        Colonies.to_excel(writer, sheet_name="Colony data", index=False)
        Parameters.to_excel(writer, sheet_name="Parameters", index=False)

    cv2.imwrite(path+file+'.jpg', np.vstack((img, caption)))
    cv2.namedWindow(file, cv2.WINDOW_KEEPRATIO)
    cv2.imshow(file, np.vstack((img, caption)))
    cv2.resizeWindow(file, 600, 600)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

