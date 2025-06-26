from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
QFileDialog, QProgressBar, QTabWidget, QTextEdit, QSpinBox, QComboBox, QMessageBox

import r3d, os

class ConverterThread(threading.Thread):
    def __init__(self):
        pass


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("R3D → MP4 Converter")
        self.resize(700, 500)

        self.dir_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse)

        self.res_combo = QComboBox()
        for r in (1, 2, 4, 8):
            self.res_combo.addItem(str(r))

        self.concurrent = QSpinBox()
        self.concurrent.setRange(1, os.cpu_count() or 4)
        self.concurrent.setValue(1)

        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.start_export)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Source:"))
        controls.addWidget(self.dir_input)
        controls.addWidget(browse_btn)

        controls.addWidget(QLabel("Compression R:"))
        controls.addWidget(self.res_combo)

        controls.addWidget(QLabel("Workers:"))
        controls.addWidget(self.concurrent)
        controls.addWidget(export_btn)

        self.tabs = QTabWidget()

        self.progress_bar = QProgressBar()
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        p = QVBoxLayout()
        p.addWidget(self.progress_bar)
        p.addWidget(self.log)
        p_tab = QWidget()
        p_tab.setLayout(p)
        self.tabs.addTab(p_tab, "Progress")

        self.stats = QLabel("Files: 0/0\nData: 0 MB\nRate: 0 MB/s\nETA: 0s")
        s_layout = QVBoxLayout()
        s_layout.addWidget(self.stats)
        s_layout.addStretch(1)
        s_tab = QWidget()
        s_tab.setLayout(s_layout)
        self.tabs.addTab(s_tab, "Statistics")

        layout = QVBoxLayout()
        layout.addLayout(controls)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.thread = None

    def browse(self):
        d = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if d:
            self.dir_input.setText(d)

    def start_export(self):
        src = self.dir_input.text().strip()
        if not os.path.isdir(src):
            QMessageBox.critical(self, "Error", "Select a valid source directory")
            return
        res = int(self.res_combo.currentText())
        workers = self.concurrent.value()

        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(1)
        self.log.clear()
        self.stats.setText("Files: 0/0\nData: 0 MB\nRate: 0 MB/s\nETA: 0s")

        def update(p, total, mb, rate, eta):
            self.progress_bar.setMaximum(total)
            self.progress_bar.setValue(p)
            self.log.append(f"Processed {p}/{total}")
            self.stats.setText(
                f"Files: {p}/{total}\n"
                f"Data: {mb/(1024*1024):.2f} MB\n"
                f"Rate: {rate/(1024*1024):.2f} MB/s\n"
                f"Expected time of Completion: {eta:.1f}s"
            )

        def done():
            self.log.append("Conversion complete!")

        self.thread = ConverterThread(src, res, workers, update, done)
        self.thread.start()

    def closeEvent(self, event):
        if self.thread and self.thread.is_alive():
            self.thread.stop()
            self.thread.join()
        super().closeEvent(event)