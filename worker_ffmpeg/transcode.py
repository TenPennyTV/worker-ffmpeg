import ffmpeg
import logging
import argparse
import requests
import hashlib

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)


parser = argparse.ArgumentParser(description='Convert speech audio to text using Google Speech API')
parser.add_argument('in_filename', help='Input filename')
parser.add_argument('out_filename', help='Output filename')


def create_preview(url, output, length=60):
    video_file = download_file(url)

    ffmpeg.input(video_file, ss=0, t=length).output(
        output, s='854x480', vcodec='libx264', acodec='libfdk_aac', audio_bitrate=128000, speed=2, crf=23,
    ).overwrite_output().run()


def download_file(url):
    local_filename = url.split('/')[-1].split('?')[0]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=256000):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


def transcode_video(resolution='480p', type='full', url=None):
    filename = download_file(url)
    outfile = hashlib.sha256(filename.encode('utf-8')).hexdigest() + '.mp4'
    if type == 'preview':
        create_preview(filename, outfile)
    elif type == 'full':
        if resolution == '480p':
            create_480p_version(filename, outfile)
        else:
            create_720p_version(filename, outfile)


def create_480p_version(input, output):
    ffmpeg.input(input, ss=0).output(
        output, s='854x480', vcodec='libx264', video_bitrate=1200000, acodec='libfdk_aac', audio_bitrate=128000, speed=2, crf=30
    ).overwrite_output().run()


def create_720p_version(input, output):
    ffmpeg.input(input, ss=0).output(
        output, s='1280x720', vcodec='libx264', video_bitrate=2400000, acodec='libfdk_aac', audio_bitrate=128000, speed=2, crf=30
    ).overwrite_output().run()


if __name__ == '__main__':
    args = parser.parse_args()
    create_480p_version(args.in_filename, args.out_filename)
