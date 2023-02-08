import sys
import os
from PIL.ImageQt import ImageQt, QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QPushButton, QFileDialog, QListWidget, QLabel, QMessageBox
from libs.xmlparser import xmlparser
from ui import Ui_MainWindow

class WindowClass(QMainWindow):
    def __init__(self):
        super(WindowClass, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())
        self.file = ""
        self.xml: xmlparser
        self.imgs = None
        self.areas = {}
        self.setWindowTitle("XMLConverter")
        self.setWindowIcon(QIcon("icon.png"))
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setEnabled(False)
        self.ui.Import.clicked.connect(self.ImportAction)
        self.ui.Export.clicked.connect(self.ExportAction)
        self.ui.listWidget.itemSelectionChanged.connect(self.ImageLoad)

    def ImportAction(self):
        self.ui.progressBar.setValue(0)
        self.file = QFileDialog.getOpenFileName(None, "Select a XML File:", os.getcwd(), "XML File (*.xml)")[0]
        self.Fileload()
        self.ui.progressBar.setValue(100)
    
    def ExportAction(self):
        self.ui.progressBar.setValue(0)
        self.file = QFileDialog.getSaveFileName(None, "Export a XML File:", os.getcwd(), "XML File (*.xml)")[0]
        self.FileSave()
        self.ui.progressBar.setValue(100)
    
    def FileSave(self):
        if not self.file:
            return
        with open(self.file, 'w+', encoding='utf-8-sig') as f:
            f.write(self.xml.convert())
            f.close()

        QMessageBox.about(None, "File Export", "File Export Success!")
    
    def ImageLoad(self):
        item = self.listWidget.selectedItems()

        area = self.areas[item[0].text()+'_position']

        width = area[2]-area[0]
        height = area[3]-area[1]

        self.infolabel.setText(f"x:{area[0]}, y:{area[1]}\nwidth:{width}, height:{height}")

        if not self.imgs:
            return

        war = width / height
        har = height / width

        qim = ImageQt(self.imgs[item[0].text()].resize((round(war * 80), round(har* 80))))

        pix = QPixmap.fromImage(qim)

        self.label.setPixmap(pix)

        
        
    def Fileload(self):
        if not self.file:
            return
        self.ui.progressBar.setValue(1)
        self.xml = xmlparser(self.file)
        self.ui.progressBar.setValue(50)
        try:
            self.imgs = self.xml.imageparse(QFileDialog.getOpenFileName(None, "Select a SpriteSheet File:", os.getcwd(), "Image File (*.png)")[0])
            self.areas = {
                k: v for k, v in self.imgs.items() if list(self.imgs).index(k) % 2 != 0 and k.endswith("_position")
            }
        except AttributeError as e:
            self.imgs = None
            for i in self.xml.parse()['TextureAtlas']['SubTexture']:
                areas = {k: int(v) for k, v in dict(filter(lambda a: a[0] != "@name", i.items())).items()}
                self.areas[i['@name']+"_position"] = (areas['@x'], areas['@y'], areas['@x']+areas['@width'], areas['@y']+areas['@height'])

        self.ui.listWidget.clear()

        self.ui.listWidget.insertItems(0, [i[:-9] for i in self.areas])
        self.ui.progressBar.setValue(99)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    sys.exit(app.exec_())