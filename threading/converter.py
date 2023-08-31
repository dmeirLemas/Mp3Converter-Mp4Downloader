import os
import sys
import threading
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor


class Converter:
	def __init__(self, format, path):
		if format == 'mp4':
			self.ydl_opts = {
			'format': 'best',
			'quiet': True,
			'no_warnings': True,
			'outtmpl': f'{path}/download_musics/%(title)s.mp4',
			}
		elif format == 'mp3':
			self.ydl_opts = {
				'format': 'm4a/bestaudio/best',
				'quiet': True,
				'no_warnings': True,
				'postprocessors': [{  # Extract audio using ffmpeg
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
				}],
				'outtmpl': f'{path}/download_musics/%(title)s.mp3',
			}
		else:
			sys.exit()
	
	def downloader(self, link):
		with YoutubeDL(self.ydl_opts) as video:
			info_dict = video.extract_info(link, download=False)  # Extract video info
			video_title = info_dict.get('title', 'Unknown Title')

			try:
				video.download([link])
			except:
				sys.exit()

	def read_doc(self, file_path):
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
	
	def download(self, links):
		with ThreadPoolExecutor(max_workers=8) as executor:
			futures = [executor.submit(self.downloader, link) for link in links]

			for future in futures:
				future.result()
