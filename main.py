from converter import Converter
import argparse


def main():
	parser = argparse.ArgumentParser(description='Youtube video downloader')
	parser.add_argument('--link', type=str, default=None, help='Video link to download.')
	parser.add_argument('--format', type=str, default='mp4', help='Format of the video to be downloaded. Default value is mp4.')
	parser.add_argument('--document', type=str, default=False, help='Read the links you want to download from a file. eg. musics.txt')
	parser.add_argument('--output', type=str, default='./', help='Location to which downloaded links will be outputted.')

	args = parser.parse_args()
	args.format = args.format.strip().strip('.').replace('.', "")

	converter = Converter(args.format)
	
	links = converter.read_doc(args.document) if args.document else [args.link]

	converter.download(links)

if __name__ == '__main__':
	main()
