import ffmpeg
import logging
import argparse
import requests
import os

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


parser = argparse.ArgumentParser(description='Convert speech audio to text using Google Speech API')
parser.add_argument('in_filename', help='Input filename')
parser.add_argument('out_filename', help='Output filename')


def create_preview(url, output, length=60):
    if os.path.isfile(output):
        return output
    video_file = download_file(url)
    ffmpeg.input(video_file, ss=0, t=length).output(
        output,
        vf="scale='w=if(gt(a,16/9),854,-2):h=if(gt(a,16/9),-2,480)'",
        vcodec='libx264',
        video_bitrate=1200000,
        acodec='aac',
        audio_bitrate=128000, speed=2, crf=24,
        pix_fmt='yuv420p',
        preset='fast',
    ).global_args('-nostdin').overwrite_output().run()
    return output


def download_file(url):
    local_filename = url.split('/')[-1].split('?')[0]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256000):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def create_480p_version(url, output):
    if os.path.isfile(output):
        return output
    video_file = download_file(url)
    ffmpeg.input(video_file, ss=0).output(
        output,
        vf="scale='w=if(gt(a,16/9),854,-2):h=if(gt(a,16/9),-2,480)'",
        vcodec='libx264',
        video_bitrate=1200000,
        acodec='aac',
        audio_bitrate=128000, speed=2, crf=24,
        pix_fmt='yuv420p',
        preset='fast',
    ).global_args('-nostdin').overwrite_output().run()
    return output


def create_720p_version(url, output):
    if os.path.isfile(output):
        return output
    video_file = download_file(url)
    ffmpeg.input(video_file, ss=0).output(
        output,
        vf="scale='w=if(gt(a,16/9),1280,-2):h=if(gt(a,16/9),-2,720)'",
        vcodec='libx264',
        video_bitrate=2400000,
        acodec='aac',
        audio_bitrate=128000,
        speed=2, crf=24,
        pix_fmt='yuv420p',
        preset='fast',
    ).global_args('-nostdin').overwrite_output().run()
    return output


if __name__ == '__main__':
    args = parser.parse_args()
    create_480p_version(args.in_filename, args.out_filename)
