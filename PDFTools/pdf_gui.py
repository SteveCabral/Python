import sys
import pymupdf as fitz
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QListWidgetItem, QHBoxLayout, QMessageBox,
    QSlider
)
from PySide6.QtGui import QPixmap, QImage, QIcon
from PySide6.QtCore import Qt, QSize

LETTER = (612, 792)
LEGAL = (612, 1008)

class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFTools Viewer - Letter/Legal Filter")
        self.resize(1200, 800)

        self.doc = None
        self.page_sizes = []
        self.zoom_factor = 1.0

        main_layout = QVBoxLayout()

        # Top buttons
        btn_layout = QHBoxLayout()
        self.btn_open = QPushButton("Open PDF")
        self.btn_filter_letter = QPushButton("Show Letter Pages")
        self.btn_filter_legal = QPushButton("Show Legal Pages")
        self.btn_filter_all = QPushButton("Show All Pages")

        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_filter_letter)
        btn_layout.addWidget(self.btn_filter_legal)
        btn_layout.addWidget(self.btn_filter_all)

        main_layout.addLayout(btn_layout)

        # Middle: thumbnails + zoom + preview
        middle_layout = QHBoxLayout()

        # Thumbnail grid
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setViewMode(QListWidget.IconMode)
        self.thumbnail_list.setIconSize(QSize(120, 160))
        self.thumbnail_list.setResizeMode(QListWidget.Adjust)
        self.thumbnail_list.setMovement(QListWidget.Static)
        self.thumbnail_list.setSpacing(10)
        middle_layout.addWidget(self.thumbnail_list, 1)

        # Right side: zoom + preview
        right_layout = QVBoxLayout()

        zoom_layout = QHBoxLayout()
        self.zoom_label = QLabel("Zoom:")
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(50)    # 50%
        self.zoom_slider.setMaximum(200)   # 200%
        self.zoom_slider.setValue(100)     # 100%
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)

        zoom_layout.addWidget(self.zoom_label)
        zoom_layout.addWidget(self.zoom_slider)
        right_layout.addLayout(zoom_layout)

        self.image_label = QLabel("Page preview will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.image_label, 1)

        middle_layout.addLayout(right_layout, 2)

        main_layout.addLayout(middle_layout)

        self.setLayout(main_layout)

        # Signals
        self.btn_open.clicked.connect(self.open_pdf)
        self.btn_filter_letter.clicked.connect(lambda: self.populate_pages("Letter"))
        self.btn_filter_legal.clicked.connect(lambda: self.populate_pages("Legal"))
        self.btn_filter_all.clicked.connect(lambda: self.populate_pages("All"))
        self.thumbnail_list.itemClicked.connect(self.show_page)
        self.zoom_slider.valueChanged.connect(self.update_zoom)

    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if not path:
            return

        try:
            self.doc = fitz.open(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open PDF:\n{e}")
            return

        self.analyze_page_sizes()
        self.populate_pages("All")

    def analyze_page_sizes(self):
        self.page_sizes = []
        for i, page in enumerate(self.doc):
            w = round(page.rect.width)
            h = round(page.rect.height)

            if (w, h) == LETTER:
                size = "Letter"
            elif (w, h) == LEGAL:
                size = "Legal"
            else:
                size = f"Other ({w}x{h})"

            self.page_sizes.append((i, size))

    def populate_pages(self, filter_type):
        self.thumbnail_list.clear()

        for index, size in self.page_sizes:
            if filter_type == "All" or size == filter_type:
                page = self.doc[index]
                pix = page.get_pixmap(dpi=30)  # low DPI for thumbnails

                # Determine correct aspect ratio scaling
                if size == "Letter":
                    scale = 0.78
                elif size == "Legal":
                    scale = 1.0
                else:
                    scale = 0.9

                w = pix.width
                h = pix.height
                thumb_h = int(160 * scale)
                thumb_w = int((w / h) * thumb_h)

                if pix.alpha:
                    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
                else:
                    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

                img = img.copy()
                pixmap = QPixmap.fromImage(img).scaled(
                    thumb_w, thumb_h,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                icon = QIcon(pixmap)

                item = QListWidgetItem(icon, f"{index+1}\n{size}")
                item.setData(Qt.UserRole, index)
                self.thumbnail_list.addItem(item)

    def show_page(self, item):
        index = item.data(Qt.UserRole)
        page = self.doc[index]

        pix = page.get_pixmap(dpi=150)

        if pix.alpha:
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGBA8888)
        else:
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

        img = img.copy()
        self.current_pixmap = QPixmap.fromImage(img)
        self.apply_zoom()

    def update_zoom(self, value):
        self.zoom_factor = value / 100.0
        self.apply_zoom()

    def apply_zoom(self):
        if not hasattr(self, "current_pixmap"):
            return

        w = int(self.image_label.width() * self.zoom_factor)
        h = int(self.image_label.height() * self.zoom_factor)

        scaled = self.current_pixmap.scaled(
            w, h,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

def main():
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
