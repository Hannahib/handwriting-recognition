import sys
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QPoint  # 这里补上了QPoint

# ===================== 画板组件 =====================
class PaintBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white; border:2px solid #333;")
        self.setFixedSize(900, 350)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.drawing = False

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.last_point = e.pos()
            self.drawing = True

    def mouseMoveEvent(self, e):
        if self.drawing and e.buttons() & Qt.LeftButton:
            p = QPainter(self.image)
            pen = QPen(Qt.black, 22, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            p.setPen(pen)
            p.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, e):
        pp = QPainter(self)
        pp.drawImage(self.rect(), self.image, self.rect())

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def save_image(self):
        scaled = self.image.scaled(28, 28)
        scaled.save("digit_28x28.png")
        QMessageBox.information(self, "成功", "已保存 28×28 图片")

    def get_image(self):
        ptr = self.image.bits()
        ptr.setsize(self.image.byteCount())
        arr = np.frombuffer(ptr, np.uint8).reshape(self.image.height(), self.image.width(), 4)
        return arr[..., :3]

# ===================== 主界面 =====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("手写数字识别系统")
        self.setFixedSize(1200, 900)

        self.paint_board = PaintBoard()

        self.result_label = QLabel("等待识别...")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("background-color:white; border:2px solid #333;")
        self.result_label.setFixedSize(900, 100)
        font = QFont()
        font.setPointSize(30)
        self.result_label.setFont(font)

        btn_style = """
        QPushButton {
            border-radius: 90px;
            background-color:#4285F4;
            color:white;
            font-size:22px;
        }
        QPushButton:hover {
            background-color:#3367D6;
        }
        """
        self.btn_clear = QPushButton("清除画布")
        self.btn_clear.setFixedSize(180, 180)
        self.btn_clear.setStyleSheet(btn_style)

        self.btn_save = QPushButton("保存图片")
        self.btn_save.setFixedSize(180, 180)
        self.btn_save.setStyleSheet(btn_style)

        self.btn_recog = QPushButton("识别数字")
        self.btn_recog.setFixedSize(180, 180)
        self.btn_recog.setStyleSheet(btn_style)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(40)

        main_layout.addWidget(self.paint_board, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(50)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_recog)

        main_layout.addLayout(btn_layout)

        central = QWidget()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        self.btn_clear.clicked.connect(self.paint_board.clear)
        self.btn_save.clicked.connect(self.paint_board.save_image)
        self.btn_recog.clicked.connect(self.on_recognize)

    def on_recognize(self):
        print("clicked")
        self.result_label.setText("识别中...")
        img = self.paint_board.get_image()
        print("获取图像成功，形状：", img.shape)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())