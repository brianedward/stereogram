import re
import subprocess
from PIL import Image
from os import listdir
from os.path import isfile, join
import os
import pprint

def createPairList():
    left_path =  os.getcwd()+'/L'
    right_path = os.getcwd()+'/R'
    left_images = [im for im in listdir(left_path) if isfile(join(left_path,im))]
    left_timestamps = [filename[14:20] for filename in left_images]
    right_images = [im for im in listdir(right_path) if isfile(join(right_path,im))]
    right_timestamps = [filename[14:20] for filename in right_images]
    pprint.pprint(left_timestamps)
    pprint.pprint(right_timestamps)
    pairs = []
    for lstamp in left_timestamps:
        for rstamp in right_timestamps:
            if abs(int(lstamp)-int(rstamp)) < 2:
                pairs.append([lstamp, rstamp])
    pprint.pprint(pairs)
    filename_pairs = []
    for pair in pairs:
        for im in listdir(left_path):
            if pair[0] in im:
                left_filename = im
        for im in listdir(right_path):
            if pair[1] in im:
                right_filename = im
        filename_pairs.append([left_filename,right_filename])
    pprint.pprint(filename_pairs)
    return filename_pairs

def stereogram(pair):

    out_left = cropHalf(str(pair[0]), 'L')
    out_right = cropHalf(str(pair[1]), 'R')
    out_name = pair[0][14:20]+'.JPG'
    sbs(out_left, out_right,out_name )

def imageDimensions(filename):
    with Image.open(filename) as im:
        width, height = im.size
        return width,height

def cropHalf(image,  side):
    image_path = side + '/' + image
    output_image = side + image
    [w,h] = imageDimensions(image_path)
    if side == 'L':
        x = 0
    if side == 'R':
        x = w/2
    y = 0
    crop_command = "crop="+str(w/2)+":"+str(h)+":"+str(x)+":"+str(y)+":"
    command = ["ffmpeg", "-i", image_path, "-vf", crop_command, "-y", output_image]
    subprocess.call(command)
    return output_image

def sbs(left, right, output_name):
    command = ["ffmpeg", "-i", left, "-i", right, "-filter_complex", "hstack", "-y", output_name]
    subprocess.call(command)


qualified_image_pairs = createPairList()
for image_pair in qualified_image_pairs:
    stereogram(image_pair)
