import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QPoint

class PaintBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white; border:2px solid #333;")
        self.setFixedSize(900, 350)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.drawing = False

        # ===== 画笔自定义参数 =====
        self.pen_color = Qt.black
        self.pen_size = 18
        self.pen_sizes = [8, 18, 28, 38]

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_size(self, size_index):
        self.pen_size = self.pen_sizes[size_index]

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.last_point = e.pos()
            self.drawing = True

    def mouseMoveEvent(self, e):
        if self.drawing and (e.buttons() & Qt.LeftButton):
            painter = QPainter(self.image)
            painter.setRenderHint(QPainter.Antialiasing)

            if hasattr(e, "pressure"):
                pressure = e.pressure()
                size = self.pen_size * pressure
            else:
                size = self.pen_size

            pen = QPen(self.pen_color, size, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, e.pos())
            self.last_point = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, e):
        pp = QPainter(self)
        pp.drawImage(self.rect(), self.image, self.rect())

    def clear(self):
        self.image.fill(Qt.white if self.palette().color(QPalette.Window).lightness() > 127 else Qt.black)
        self.update()

    def save_image(self):
        scaled = self.image.scaled(28, 28)
        scaled.save("digit_28x28.png")
        QMessageBox.information(self, "保存", "28×28 图片已保存")

    def get_28x28_image(self):
        return self.image.scaled(28, 28)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("手写数字识别系统")
        self.setFixedSize(1200, 900)
        self.is_dark = False

        self.paint_board = PaintBoard()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 结果显示
        self.result_label = QLabel("等待识别...")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("background-color:white; border:2px solid #333; font-size:30px")
        self.result_label.setFixedHeight(100)

        # 圆形按钮
        btn_style = """
        QPushButton {
            border-radius: 90px;
            background-color:#4285F4;
            color:white;
            font-size:22px;
        }
        """
        self.btn_clear = QPushButton("清除画布")
        self.btn_save = QPushButton("保存图片")
        self.btn_recog = QPushButton("识别数字")
        for b in [self.btn_clear, self.btn_save, self.btn_recog]:
            b.setFixedSize(180, 180)
            b.setStyleSheet(btn_style)

        # 颜色按钮
        self.color_buttons = {}
        colors = [("黑色", Qt.black), ("红", Qt.red), ("绿", Qt.green),
                  ("蓝", Qt.blue), ("黄", Qt.yellow), ("紫", Qt.magenta), ("青", Qt.cyan)]
        color_layout = QHBoxLayout()
        for name, col in colors:
            btn = QPushButton(name)
            btn.setStyleSheet(f"background-color:{name if name != '黑色' else '#333'}; color:white;")
            btn.clicked.connect(lambda checked, c=col: self.paint_board.set_pen_color(c))
            color_layout.addWidget(btn)
            self.color_buttons[name] = btn

        # 粗细档位
        self.size_buttons = []
        size_layout = QHBoxLayout()
        for i, text in enumerate(["细", "中", "粗", "极粗"]):
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, idx=i: self.paint_board.set_pen_size(idx))
            size_layout.addWidget(btn)
            self.size_buttons.append(btn)

        # 主题切换
        self.theme_btn = QPushButton("切换深色模式")
        self.theme_btn.clicked.connect(self.toggle_theme)

        # 布局
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        main_layout.addWidget(self.theme_btn)
        main_layout.addLayout(color_layout)
        main_layout.addLayout(size_layout)
        main_layout.addWidget(self.paint_board, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.result_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(40)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_recog)
        main_layout.addLayout(btn_layout)

        # 绑定
        self.btn_clear.clicked.connect(self.paint_board.clear)
        self.btn_save.clicked.connect(self.paint_board.save_image)
        self.btn_recog.clicked.connect(self.on_recognize)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.setStyleSheet("background-color:#222; color:white;")
            self.result_label.setStyleSheet("background-color:#333; color:white; border:2px solid #666; font-size:30px")
            self.paint_board.setStyleSheet("background-color:#111; border:2px solid #666;")
            self.theme_btn.setText("切换浅色模式")
        else:
            self.setStyleSheet("")
            self.result_label.setStyleSheet("background-color:white; border:2px solid #333; font-size:30px")
            self.paint_board.setStyleSheet("background-color:white; border:2px solid #333;")
            self.theme_btn.setText("切换深色模式")

    def on_recognize(self):
        print("clicked")
        img = self.paint_board.get_28x28_image()
        print("28×28 图像已准备就绪")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())