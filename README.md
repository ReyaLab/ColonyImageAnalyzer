# ColonyImageAnalyzer
Analyze black and white colony assay photos taken by microscope.

This program identifies the live and necrotic cell colonies in a colony assay, and calculates a ratio of necrosis for every colony in frame, as well as the total live vs dead area within the entire image.

It works using OpenCV2's find_threshhold functions. 

Required libraries are OpenCV2, Pandas, and NumPy.

Download the scripts, put them in the same folder, then run the GUI script. Enter the PATH of your greyscale TIFF image files and then run.
