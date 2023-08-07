import argparse
from yt_dlp import YoutubeDL

def download(link, options):
    with YoutubeDL(options) as video:
    video.download([link])


def main():
    parser = argparse.ArgumentParser(description='Yotube video downloader')
    parser.add_argument('link', type=str, help='Video link to download.')
    parser.add_argument('--format', type=str, default='mp4', help='Format of the video to be downloaded. Default value is mp4.')
    
    args = parser.parse_args()
    args.format = args.format.strip().strip('.').replace('.', "")
    if args.format == 'mp3': 
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    elif args.format == 'mp4': 
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'%(title)s.mp4',
        }
    else:
        print('Unsupported download format.')

    download(args.link, ydl_opts)

if __name__ == '__main__':
    main()
