import os
import sys
import multiprocessing
from yt_dlp import YoutubeDL

class Converter:
	def __init__(self, format: str) -> None:
		if format == 'mp4':
			self.ydl_opts = {
			'format': 'best',
			'quiet': True,
			'no_warnings': True,
			'outtmpl': f'downloaded_musics/%(title)s.mp4',
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
				'outtmpl': f'downloaded_musics/%(title)s.mp3',
			}
		else:
			print('Unsupported format')
			sys.exit()
	
	def downloader(self, link):
		with YoutubeDL(self.ydl_opts) as video:
			info_dict = video.extract_info(link, download=False)  # Extract video info
			video_title = info_dict.get('title', 'Unknown Title')

			print('\n\033[33m Downloading \033[32m' + video_title + '\033[0m')
			try:
				video.download([link])
			except:
				print(f'\n \033[31m There was an error downloading {video_title}.\033[0m')

	def read_doc(self,file_path):
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
		num_workers = min(len(links), multiprocessing.cpu_count())
		pool = multiprocessing.Pool(processes=num_workers)
		pool.map(self.downloader, [link for link in links])
		pool.close()
		pool.join()

