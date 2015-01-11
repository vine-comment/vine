import os
import sys
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from subprocess import Popen, PIPE

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))

class Screenshot(QMainWindow):
    def __init__(self):
        self.app = QApplication(sys.argv)
        QMainWindow.__init__(self)
        #self.resize(1024, 768)
        self.web_view = QWebView()
        self.setCentralWidget(self.web_view)
        self._loaded = False
        self.web_view.loadFinished.connect(self._loadFinished)

    def capture(self, url, output_file):
        self.web_view.load(QUrl(url))
        self.wait_load()
        # set to webpage size
        page = self.web_view.page()
        frame = page.mainFrame()
        #self.web_view.page().setViewportSize(frame.contentsSize())
        page.setViewportSize(QSize(1024, 768))
        page.mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        page.mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        # render image
        image = QImage(self.web_view.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)

    def wait_load(self, delay=0):
        # process app events until page loaded
        while not self._loaded:
            self.app.processEvents()
            time.sleep(delay)
        self._loaded = False

    def _loadFinished(self, result):
        self._loaded = True

#s = Screenshot()
#s.capture('http://tengmanpinglun.com', 'website.png')
#s.capture('http://webscraping.com/blog', 'blog.png')

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)

def do_crop(params):
    print "Croping captured image.."
    command = [
        'convert',
        params['screen_path'],
        '-crop', '%sx%s+0+0' % (params['width'], params['height']),
        params['crop_path']
    ]
    execute_command(' '.join(command))


def do_thumbnail(params):
    print "Generating thumbnail from croped captured image.."
    command = [
        'convert',
        params['crop_path'],
        '-filter', 'Lanczos',
        '-thumbnail', '%sx%s' % (params['width'], params['height']),
        params['thumbnail_path']
    ]
    execute_command(' '.join(command))

def get_screen_shot(**kwargs):
    url = kwargs['url']
    width = int(kwargs.get('width', 1024)) # screen width to capture
    height = int(kwargs.get('height', 768)) # screen height to capture
    filename = kwargs.get('filename', 'screen.png') # file name e.g. screen.png
    path = kwargs.get('path', ROOT) # directory path to store screen

    crop = kwargs.get('crop', False) # crop the captured screen
    crop_width = int(kwargs.get('crop_width', width)) # the width of crop screen
    crop_height = int(kwargs.get('crop_height', height)) # the height of crop screen
    crop_replace = kwargs.get('crop_replace', False) # does crop image replace original screen capture?

    thumbnail = kwargs.get('thumbnail', False) # generate thumbnail from screen, requires crop=True
    thumbnail_width = int(kwargs.get('thumbnail_width', width)) # the width of thumbnail
    thumbnail_height = int(kwargs.get('thumbnail_height', height)) # the height of thumbnail
    thumbnail_replace = kwargs.get('thumbnail_replace', False) # does thumbnail image replace crop image?

    screen_path = abspath(path, filename)
    crop_path = thumbnail_path = screen_path

    if thumbnail and not crop:
        raise Exception, 'Thumnail generation requires crop image, set crop=True'

    do_screen_capturing(url, screen_path, width, height)

    if crop:
        if not crop_replace:
            crop_path = abspath(path, 'crop_'+filename)
        params = {
            'width': crop_width, 'height': crop_height,
            'crop_path': crop_path, 'screen_path': screen_path}
        do_crop(params)

        if thumbnail:
            if not thumbnail_replace:
                thumbnail_path = abspath(path, 'thumbnail_'+filename)
            params = {
                'width': thumbnail_width, 'height': thumbnail_height,
                'thumbnail_path': thumbnail_path, 'crop_path': crop_path}
            do_thumbnail(params)
    return screen_path, crop_path, thumbnail_path

if __name__ == '__main__':
    '''
        Requirements:
        install imageMagick

    url = 'http://tengmanpinglun.com'
    screen_path, crop_path, thumbnail_path = get_screen_shot(
        url=url, filename='sof.png',
        crop=True, crop_replace=False,
        thumbnail=True, thumbnail_replace=False,
        thumbnail_width=200, thumbnail_height=150,
    )
    '''
    s = Screenshot()
    s.capture('http://www.baidu.com', 'website.png')

