import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QRadioButton, QFileDialog, QWidget, QMessageBox, QGroupBox
from converter import Converter  

class YouTubeDownloaderGUI(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("YouTube Downloader")

		self.group1 = QGroupBox()
		self.central_widget = QWidget()
		self.setCentralWidget(self.central_widget)
		self.layout = QVBoxLayout()
		self.central_widget.setLayout(self.layout)
		self.file_layout = QVBoxLayout()

		self.link_radio = QRadioButton("Download from Link:")
		self.link_radio.setChecked(True)
		self.file_layout.addWidget(self.link_radio)

		self.link_entry = QLineEdit()
		self.file_layout.addWidget(self.link_entry)

		self.file_radio = QRadioButton("Download from File:")
		self.file_radio.toggled.connect(self.single_multi_url)
		self.file_layout.addWidget(self.file_radio)

		self.file_button = QPushButton("Choose File")
		self.file_button.setEnabled(False)
		self.file_button.clicked.connect(self.choose_file)
		self.file_layout.addWidget(self.file_button)

		self.file_label = QLabel("File not chosen")
		self.file_label.setStyleSheet('')
		self.file_layout.addWidget(self.file_label)

		self.group1.setLayout(self.file_layout)
		self.layout.addWidget(self.group1)

		self.group2 = QGroupBox()
		self.format_label = QLabel("Select Format:")
		self.format_radio_mp4 = QRadioButton("MP4")
		self.format_radio_mp3 = QRadioButton("MP3")
		self.format_layout = QVBoxLayout()
		self.format_layout.addWidget(self.format_label)
		self.format_layout.addWidget(self.format_radio_mp4)
		self.format_layout.addWidget(self.format_radio_mp3)
		self.group2.setLayout(self.format_layout)
		self.layout.addWidget(self.group2)

		self.download_button = QPushButton("Download")
		self.download_button.clicked.connect(self.download_video)
		self.layout.addWidget(self.download_button)

		self.selected_file = None
		self.file_read = False

	def single_multi_url(self, checked):
		self.file_button.setEnabled(checked)
		self.link_entry.setEnabled(not checked)
		if checked:
			self.link_entry.clear()
		else:
			self.selected_file = None
			self.file_read = False
			self.file_label.setText('File not chosen')
			self.file_label.setStyleSheet('')
		
	def choose_file(self):
		self.selected_file, _ = QFileDialog.getOpenFileName(self, "Choose a file with links", "", "Text Files (*.txt);;All Files (*)")
		if self.selected_file:
			self.file_read = False
			self.file_label.setText("File chosen")
			self.file_label.setStyleSheet('color: yellow')

	def download_video(self):
		format = "mp4" if self.format_radio_mp4.isChecked() else "mp3"

		if self.link_radio.isChecked():
			link = self.link_entry.text()
			if link:
				self.download([link], format)
			else:
				QMessageBox.warning(self, "Missing Link", "Please enter a YouTube link.")

		elif self.file_radio.isChecked() and self.selected_file:
			links = self.read_links_from_file(self.selected_file)
			if links:
				self.file_read = True
				self.download(links, format)
			else:
				QMessageBox.warning(self, "File Error", "The selected file does not contain valid links.")

	def read_links_from_file(self, file_path):
		converter = Converter(format="mp4")  
		return converter.read_doc(file_path)

	def download(self, links, format):
		try:
			converter = Converter(format)
			converter.download(links)
			if self.file_read:
				self.file_label.setText("File read and processed")
			QMessageBox.information(self, "Download Complete", "Videos downloaded successfully!")
		except:
			QMessageBox.critical(self, "Error", "An error occurred while downloading the videos.")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = YouTubeDownloaderGUI()
	window.show()
	sys.exit(app.exec())

