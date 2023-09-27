# _*_ coding: utf-8 _*_
# !/usr/bin/env python
"""
Description: This python script is used for converting a MP4 file into a YUV file
Usage: command line: python mp4toyuv.py input_file width height fps --output_file output_file(optional)
Author: YeYiqi
Date: 2023/9/17
"""


import cv2
import numpy as np
from numba import jit
import argparse
from tqdm import tqdm

AIM_WIDTH = 320
AIM_HEIGHT = 240
AIM_FPS = 15

@jit(nopython=True)
def frame_convertor(buffer_bytes, frame_idx, frame):
    """
    This function convert a frame of RGB into a YUV coding bytes string
    :param buffer_bytes: The result string
    :param frame_idx: the index of frame
    :param frame: ith frame
    :return: None
    """
    y_pos = int(frame_idx * 1.5 * AIM_WIDTH * AIM_HEIGHT)
    u_pos = y_pos + int(AIM_WIDTH * AIM_HEIGHT)
    v_pos = u_pos + int(AIM_WIDTH * AIM_HEIGHT / 4)
    for h_index in range(AIM_HEIGHT):
        for w_index in range(AIM_WIDTH):
            buffer_bytes[y_pos] = 0.299 * frame[h_index][w_index][2] + \
                                  0.587 * frame[h_index][w_index][1] + \
                                  0.114 * frame[h_index][w_index][0]
            y_pos += 1
            if h_index % 2 == 0 and w_index % 2 == 0:
                buffer_bytes[u_pos] = -0.169 * frame[h_index][w_index][2] + \
                                      -0.332 * frame[h_index][w_index][1] + \
                                      0.500 * frame[h_index][w_index][0] + 128
                buffer_bytes[v_pos] = 0.5000 * frame[h_index][w_index][2] + \
                                      -0.419 * frame[h_index][w_index][1] + \
                                      -0.0813 * frame[h_index][w_index][0] + 128
                u_pos += 1
                v_pos += 1


if __name__ == '__main__':
    # create a parser
    parser = argparse.ArgumentParser(description="This is a simple python script to convert mp4 to yuv file.")
    parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("width", help='The width of your yuv file.')
    parser.add_argument('height', help='The height of your yuv file.')
    parser.add_argument('fps', help='The FPS of your yuv file.(notice that >mp4 file\' fps)')
    parser.add_argument('--output_file', "-o", help='Path to the output file. (Default = same to the input file)')

    args = parser.parse_args()
    AIM_WIDTH = int(args.width)
    AIM_HEIGHT = int(args.height)
    AIM_FPS = int(args.fps)
    try:
        cap = cv2.VideoCapture(args.input_file)
    except FileNotFoundError:
        print('File not exist!')
        exit(1)

    if cap.isOpened():
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print('origin video:')
        print('width:{}\t height:{}\t frames:{}\t fps:{}\t'.format(width, height, frame_num, fps))
        interval = round(fps / AIM_FPS)
        frames = []
        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if count % interval == 0:
                resized_frame = cv2.resize(frame, (AIM_WIDTH, AIM_HEIGHT), interpolation=cv2.INTER_CUBIC)
                frames.append(resized_frame)
            else:
                pass
            count += 1
    else:
        print('File shut down!')
        exit(1)

    buffer_bytes = np.zeros(int(AIM_WIDTH * AIM_HEIGHT * 1.5 * len(frames)), dtype='uint16')
    for index in tqdm(range(len(frames)), desc='Processing'):
        frame_convertor(buffer_bytes, index, frames[index])
    buffer_bytes = np.clip(buffer_bytes, 0, 255)
    yuv_bytes_str = buffer_bytes.astype(dtype='uint8').tobytes()

    if args.output_file:
        output_path = args.output_file
    else:
        output_path = args.input_file[:-3] + 'yuv'

    with open(output_path, 'wb') as f:
        f.write(yuv_bytes_str)
        f.close()

    print("CONVERT FINISH!")
    print('converted video:')
    print('width:{}\t height:{}\t frames:{}\t fps:{}\t'.format(AIM_WIDTH, AIM_HEIGHT, len(frames), AIM_FPS))



