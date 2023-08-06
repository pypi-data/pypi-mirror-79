#!/usr/bin/env python

import click
from moviepy.editor import *
import os
import numpy as np

# 最小fps
MIN_FPS = 10
# 最小颜色数量
MIN_COLORS = 40
# 最小图片尺寸（最长边的长度）
MIN_DIMENSION = 160

# 生成的gif文件尺寸限制
LIMIT_SIZE = 10 * 1024 * 1024


def getClipWidth(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 1)


def getClipHeight(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 0)


def getClipSide(clip):
    # Return the dimension with the smallest value.
    if getClipWidth(clip) < getClipHeight(clip):
        return 'width'
    else:
        return 'height'


def getClipDimension(clip):
    return min(getClipWidth(clip), getClipHeight(clip))


def getClipFramesCount(clip):
    return int(clip.fps * clip.duration)


def getFileSize(path):
    return os.path.getsize(path)


def showOrigInfo(width, height, frames_count, fps, duration, colors, size):
    print('  Dimension: %d * %d' % (width, height))
    print('  Frames Count: %(fr)d (%(fps)d fps *  %(du).2f s)' %
          {'fr': frames_count, 'fps': fps, 'du': duration})
    print('  File Size: %d KB\n' % (size / 1000))


def showChangedInfo(width, height, frames_count, fps, duration, colors, size,
                    orig_width, orig_height, orig_frames_count,
                    orig_fps, orig_duration, orig_size):
    print(
        '  Dimension: %(orig_wid)d * %(orig_hei)d -> %(curr_wid)d * %(curr_hei)d' %
        {'curr_wid': width, 'curr_hei': height, 'orig_wid': orig_width,
         'orig_hei': orig_height})
    print(
        '  Frames Count: %(orig_fr)d (%(orig_fps)d fps *  %(orig_du).2f s) -> %(curr_fr)d (%(curr_fps)d fps *  %(curr_du).2f s)' %
        {'orig_fr': orig_frames_count, 'orig_fps': orig_fps,
         'orig_du': orig_duration,
         'curr_fr': frames_count, 'curr_fps': fps, 'curr_du': duration})
    print('  Colors Count: %d' % colors)
    print('  Size: %(orig)d KB -> %(curr)d KB\n' %
          {'orig': (orig_size / 1000), 'curr': (size / 1000)})


def compressClip(clip_path,
                 min_fps=MIN_FPS,
                 min_dimension=MIN_DIMENSION,
                 min_colors=MIN_COLORS,
                 limit_size=LIMIT_SIZE):
    # Output file name and path setting.

    file_name, file_extension = os.path.splitext(clip_path)
    output_filename = file_name + '.gif'

    temp_dir = os.path.join(os.getcwd(), 'output/')
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, output_filename)

    clip = VideoFileClip(clip_path)

    # Store original clip information
    shortest_side = getClipSide(clip)
    original_dimension = getClipDimension(clip)
    original_width = getClipWidth(clip)
    original_height = getClipHeight(clip)
    original_fps = clip.fps
    original_duration = clip.duration
    original_framesCount = getClipFramesCount(clip)
    original_size = getFileSize(clip_path)

    print('\nOriginal Info:')
    showOrigInfo(original_width, original_height, original_framesCount,
                 original_fps, original_duration, 0, original_size)

    # PRE-COMPRESSION
    # Change color count.
    current_colors_count = 64

    # Set a variable for changing dimension.
    if original_dimension > 300:
        current_dimension = 300
    else:
        current_dimension = original_dimension

    # Change dimension based on the shortest side.
    if shortest_side == 'width':
        temp_clip = clip.resize(width=current_dimension)
    else:
        temp_clip = clip.resize(height=current_dimension)

    # Change fps.
    if original_fps > 15:
        current_fps = 15
    else:
        current_fps = original_fps

    # Compress to a gif file.
    temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                        colors=current_colors_count, tempfiles=True)

    temp_clip = VideoFileClip(temp_path)
    current_size = getFileSize(temp_path)
    current_framesCount = getClipFramesCount(temp_clip)
    current_duration = temp_clip.duration
    print('\n\n1-time compression finished.')
    showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                    current_framesCount, temp_clip.fps, current_duration,
                    current_colors_count, current_size, original_width,
                    original_height, original_framesCount, original_fps,
                    original_duration, original_size)

    # COMPRESSION
    compression_counter = 1
    real_counter = 1

    while True:
        if (current_size < limit_size) or \
                (current_fps <= min_fps
                 and current_dimension <= min_dimension
                 and current_colors_count <= min_colors):
            # os.rename(temp_path, output_path)
            print('Ouput file saved to %s\n' % temp_path)
            break

        # Compression settings
        if compression_counter == 0:
            if original_dimension > 300:
                current_dimension = 300
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 1:
            if original_dimension > 260:
                current_dimension = 260
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 2:
            if original_fps > 12:
                current_fps = 12
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 3:
            current_colors_count = 56
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 4:
            if original_dimension > 220:
                current_dimension = 220
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 5:
            current_colors_count = 48
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 6:
            if original_dimension > 200:
                current_dimension = 200
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 7:
            current_colors_count = 40
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 8:
            if original_fps > 10:
                current_fps = 10
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 9:
            if original_dimension > 160:
                current_dimension = 160
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue

        # Execute the compression
        # Change dimension based on the shortest side.
        if shortest_side == 'width':
            temp_clip = clip.resize(width=current_dimension)
        else:
            temp_clip = clip.resize(height=current_dimension)

        # Compress to a gif file.
        temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                            colors=current_colors_count, tempfiles=True)

        temp_clip = VideoFileClip(temp_path)
        current_size = getFileSize(temp_path)
        current_framesCount = getClipFramesCount(temp_clip)
        current_duration = temp_clip.duration
        print('\n\n%d-time compression finished.' % (real_counter))
        showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                        current_framesCount, temp_clip.fps, current_duration,
                        current_colors_count, current_size, original_width,
                        original_height, original_framesCount, original_fps,
                        original_duration, original_size)


@click.command()
@click.argument('gif_path')
@click.option('--min_fps', default=MIN_FPS, help='最小fps')
@click.option('--min_colors', default=MIN_FPS, help='最小fps')
@click.option('--min_dimension', default=MIN_DIMENSION, help='最小图片尺寸（最长边的长度）')
@click.option('--limit_size', default=LIMIT_SIZE, help='生成的gif文件尺寸限制')
def compress(gif_path, min_fps, min_colors, min_dimension, limit_size):
    compressClip(clip_path=gif_path,
                 min_fps=min_fps,
                 min_colors=min_colors,
                 min_dimension=min_dimension,
                 limit_size=limit_size)


if __name__ == '__main__':
    compress()
