import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
#from PyQt5.QtGui import VLine


def final_lst(x):
    listing = []
    ext = ['mp4', 'wav']
    for i in x:
        i = i.lower()
        extension = i[-3:]
        four_char = i[-4:]
        if extension in ext or four_char in ext:
            listing.append(i)        
    return listing

class player(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.userplaylist = []
        self.playlist = []
        # adding menubar
        #open file
        openFile = QAction("&Open Video", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open video')
        openFile.triggered.connect(self.openVideo)
        #open folder
        openFolder = QAction("&Open Folder", self)
        openFolder.setShortcut("Ctrl+F")
        openFolder.setStatusTip('Open folder')
        openFolder.triggered.connect(self.openFolders)
        # exit
        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+X')
        exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        # For MacOS users, places menu bar in main window
        menu_bar.setNativeMenuBar(False)
        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(openFile)
        file_menu.addAction(openFolder)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)
        # creating media player object
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # creating a video widget object
        self.videoWidget = QVideoWidget()
        self.videoWidget.setStyleSheet("background-color:black;")

        # adding playlist button
        self.playlistButton = QPushButton()
        self.playlistButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.playlistButton.setStyleSheet("max-width: 20px;")
        self.playlistButton.clicked.connect(self.playlistPlay)

        # adding play button
        self.playButton = QPushButton()
            #self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet("max-width: 20px;")
        self.playButton.setShortcut("P")
        self.playButton.clicked.connect(self.startPlay)
 
        # adding pause button
        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pauseButton.setStyleSheet("max-width: 20px;")
        self.pauseButton.setShortcut("Space")
        self.pauseButton.clicked.connect(self.pausePlay)

        # adding stop button
        self.stopButton = QPushButton()
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.setStyleSheet("max-width: 20px;")
        self.stopButton.setShortcut("s")
        self.stopButton.clicked.connect(self.stopPlay)

        # adding skip backward
        self.skipButton = QPushButton()
        self.skipButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.skipButton.setStyleSheet("max-width: 20px;")
        self.skipButton.setShortcut("Ctrl+Left")
        self.skipButton.clicked.connect(self.skipPlay)

        # adding seek backword
        self.seekButton = QPushButton()
        self.seekButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))
        self.seekButton.setStyleSheet("max-width: 20px;")
        self.seekButton.setShortcut("Left")
        self.seekButton.clicked.connect(self.seekPlay)

        # adding skip forward
        self.skipfButton = QPushButton()
        self.skipfButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.skipfButton.setStyleSheet("max-width: 20px;")
        self.skipfButton.setShortcut("Ctrl+Right")
        self.skipfButton.clicked.connect(self.skipfPlay)

        # adding seek forward
        self.seekfButton = QPushButton()
        self.seekfButton.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.seekfButton.setStyleSheet("max-width: 20px;")
        self.seekfButton.setShortcut("Right")
        self.seekfButton.clicked.connect(self.seekfPlay)

        # adding volume
        self.volumeButton = QPushButton()
        self.volumeButton.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeButton.setStyleSheet("max-width: 20px;")
        self.volumeButton.setShortcut("Up")
        self.volumeButton.clicked.connect(self.volumePlay)

        # adding volume control
        '''self.volumeControl = QAudio()
        self.volumeControl.VolumeScale'''
        # adding volume slider
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setStyleSheet("max-width: 100px;")
        self.volumeSlider.setMouseTracking(True)
        self.volumeSlider.setValue(0)
        self.volumeSlider.setCursor(QCursor(Qt.PointingHandCursor))
        self.volumeSlider.setSingleStep(1)
        self.volumeSlider.setPageStep(10)
        self.volumeSlider.sliderMoved.connect(self.setVolumed)

        # adding position slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setMouseTracking(True)
        self.positionSlider.setCursor(QCursor(Qt.PointingHandCursor))
        self.positionSlider.sliderMoved.connect(self.setPosition)
        # adding layouts
        widget = QWidget(self)
        self.setCentralWidget(widget)
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playlistButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.pauseButton)
        controlLayout.addWidget(self.stopButton)
        controlLayout.addWidget(self.skipButton)
        controlLayout.addWidget(self.seekButton)
        controlLayout.addWidget(self.seekfButton)
        controlLayout.addWidget(self.skipfButton)
        controlLayout.setAlignment(Qt.AlignLeft)

        controlLayout2 = QHBoxLayout()
        controlLayout2.setContentsMargins(0, 0, 0, 0)
        controlLayout2.addWidget(self.volumeSlider)
        controlLayout2.addWidget(self.volumeButton)
        '''controlLayout2.addWidget(self.seekButton)
        controlLayout2.addWidget(self.seekfButton)
        controlLayout2.addWidget(self.skipfButton)'''
        controlLayout2.setAlignment(Qt.AlignRight)

        controlLayout3 = QHBoxLayout()
        controlLayout3.addLayout(controlLayout)
        #controlLayout3.addWidget(VLine())
        controlLayout3.addLayout(controlLayout2)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout3)
        layout.addWidget(self.positionSlider)
 
        widget.setLayout(layout)
        self.player.setVideoOutput(self.videoWidget)
        self.player.stateChanged.connect(self.mediaStateChanged)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.volumeChanged.connect(self.volumeChanged)
        self.player.error.connect(self.handleError)
        
    def playlistPlay(self):
        print("ls")
        print(self.playlist)

    def openFolders(self):
        print("folder")
        self.folder = QFileDialog().getExistingDirectory(self, 'Open File', '')
        print(self.folder)
        self.path_list = os.listdir(self.folder)
        self.playlist = final_lst(self.path_list)
        print(self.playlist)

    def openVideo(self, mediafile=None):
        print(mediafile)
        mediafile = mediafile
        if mediafile is False:
            name = QFileDialog.getOpenFileName(self, 'Open File')
            self.name = name[0]
        else:
            print("working100")
            self.name = mediafile
        print(self.name)
        print(type(self.name))
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.name)))
        
    def startPlay(self):
        print("playing")
        self.player.play()
    
    def pausePlay(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            print("stoping")
            self.player.pause()

    def stopPlay(self):
        if self.player.state() == QMediaPlayer.PlayingState or self.player.state() == QMediaPlayer.PausedState:
            self.openVideo(self.name)

    def skipPlay(self):
        print("working skip")
    
    def seekPlay(self):
        print("working seek")
        print(self.position)
        #self.positionSlider.setValue(self.position)
        self.player.setPosition(self.position - 10000)

    def skipfPlay(self):
        print("working skipf")

    def seekfPlay(self):
        print("working seekf")
        print(self.position)
        self.player.setPosition(self.position + 10000)
    
    def volumePlay(self):
        print("volume")
        print(self.player.volume())
    def mediaStateChanged(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pauseButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def volumeChanged(self):
        self.volumeSlider.setRange(0, 100)

    def setVolumed(self, positiond):
        self.player.setVolume(positiond)
        self.player.setValue(positiond)

    def positionChanged(self, position):
        self.position = position
        #print(self.position)
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self, position):
        self.player.setPosition(position)
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.player.errorString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    videoplayer = player()
    videoplayer.resize(640, 480)
    videoplayer.show()
    sys.exit(app.exec_())
