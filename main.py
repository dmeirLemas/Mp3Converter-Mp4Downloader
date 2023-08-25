#!/opt/homebrew/bin/python3

import os
import sys
import argparse
import multiprocessing
from yt_dlp import YoutubeDL

def download(link, options):
	with YoutubeDL(options) as video:
		info_dict = video.extract_info(link, download=False)  # Extract video info
		video_title = info_dict.get('title', 'Unknown Title')

		print('\n\033[33m Downloading \033[32m' + video_title + '\033[0m')
		try:
			video.download([link])
		except:
			print(f'\n \033[31m There was an error downloading {video_title}.\033[0m')

def read_doc(file_path):
	links = []
	with open(file_path, 'r') as f:
		current_links = []
		for line in f:
			if line.strip():  # Check if the line is not empty
				line_links = line.strip().split()
				current_links.extend(line_links)
			else:
				if current_links:
					links.append(current_links)
					current_links = []
		if current_links:  # Append the last set of links if there's no empty line after them
			links.append(current_links)
	links = [link for sublist in links for link in sublist]
	return links

def process_handler(links, options):
	num_workers = min(len(links), multiprocessing.cpu_count())
	pool = multiprocessing.Pool(processes=num_workers)
	pool.starmap(download, [(link, options) for link in links])
	pool.close()
	pool.join()

def main():
	parser = argparse.ArgumentParser(description='Youtube video downloader')
	parser.add_argument('--link', type=str, default=None, help='Video link to download.')
	parser.add_argument('--format', type=str, default='mp4', help='Format of the video to be downloaded. Default value is mp4.')
	parser.add_argument('--document', type=str, default=False, help='Read the links you want to download from a file. eg. musics.txt')
	parser.add_argument('--output', type=str, default='./', help='Location to which downloaded links will be outputted.')

	args = parser.parse_args()
	args.format = args.format.strip().strip('.').replace('.', "")

	if args.format == 'mp4':
		ydl_opts = {
			'format': 'best',
			'quiet': True,
			'outtmpl': f'downloaded_musics/%(title)s.mp4',
		}
	elif args.format == 'mp3':
		ydl_opts = {
			'format': 'm4a/bestaudio/best',
			'quiet': True,
			'postprocessors': [{  # Extract audio using ffmpeg
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
			}],
			'outtmpl': f'{args.output}/%(title)s.mp3',
		}
	else:
		print('\033[31m Unsupported output format. \033[0m')
		sys.exit()

	links = [args.link]

	if args.document:
		links = read_doc(args.document)


	process_handler(links, ydl_opts)

if __name__ == '__main__':
	main()

