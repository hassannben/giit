import sys
import vlc
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFrame, QListWidget, QListWidgetItem, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مشغل الفيديو")
        self.setGeometry(100, 100, 1200, 700)

        # VLC setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Layouts
        main_layout = QHBoxLayout(self)
        channel_layout = QVBoxLayout()
        video_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # قائمة القنوات
        self.channel_list_widget = QListWidget(self)
        self.channel_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                border-radius: 10px;
                padding: 5px;
                font-size: 16px;
            }
            QListWidget::item {
                padding: 12px 16px;
                margin-bottom: 6px;
                border-radius: 8px;
                background-color: #2a2d33;
            }
            QListWidget::item:hover {
                background-color: #3a3f47;
            }
            QListWidget::item:selected {
                background-color: #4a90e2;
                color: #ffffff;
            }
        """)
        self.channel_list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        channel_layout.addWidget(self.channel_list_widget)

        # حالة الفيديو (تم إخفاءها)
        self.status_label = QLabel(self)
        self.status_label.setStyleSheet("color: white; font-size: 14px; margin-top: 10px;")
        channel_layout.addWidget(self.status_label)

        # إطار الفيديو
        self.frame = QFrame(self)
        self.frame.setStyleSheet("background-color: black;")
        self.frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_layout.addWidget(self.frame)

        # أزرار التحكم
        self.play_button = QPushButton("تشغيل")
        self.pause_button = QPushButton("إيقاف مؤقت")
        self.stop_button = QPushButton("إيقاف")
        self.restart_button = QPushButton("إعادة التشغيل")

        # إعداد الأزرار
        buttons = [self.play_button, self.pause_button, self.stop_button, self.restart_button]
        colors = ["#4CAF50", "#FF9800", "#F44336", "#2196F3"]
        for btn, color in zip(buttons, colors):
            btn.setStyleSheet(f"background-color: {color}; color: white; padding: 10px; border-radius: 5px;")
            button_layout.addWidget(btn)

        video_layout.addLayout(button_layout)

        # دمج التخطيطات
        main_layout.addLayout(channel_layout, 1)
        main_layout.addLayout(video_layout, 3)

        # تحميل القنوات
        self.channels = self.parse_m3u_file(r"C:\Users\fmome\Desktop\pyapk\channels.m3u")
        for channel in self.channels:
            item = QListWidgetItem(channel["name"])
            item.setData(1, channel["url"])
            self.channel_list_widget.addItem(item)

        # ربط الوظائف
        self.channel_list_widget.itemClicked.connect(self.play_video)
        self.channel_list_widget.itemDoubleClicked.connect(self.play_fullscreen)

        self.play_button.clicked.connect(self.play_video_from_button)
        self.pause_button.clicked.connect(self.pause_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.restart_button.clicked.connect(self.restart_video)

        self.setStyleSheet("background-color: #121212;")
        self.setFocusPolicy(Qt.StrongFocus)

    def parse_m3u_file(self, path):
        channels = []
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    name = lines[i].split(",")[1].strip()
                    url = lines[i + 1].strip()
                    channels.append({"name": name, "url": url})
        return channels

    def play_video(self, item=None):
        if item:
            url = item.data(1)
        else:
            url = self.channels[0]["url"]

        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.set_hwnd(self.frame.winId())

        try:
            if self.player.play() == -1:
                self.status_label.setText("خطأ في التشغيل")
            else:
                # لا يتم تعيين النص هنا بعد الآن
                pass
        except Exception as e:
            # لا يتم تعيين النص هنا بعد الآن
            pass

    def play_video_from_button(self):
        self.play_video()

    def pause_video(self):
        if self.player.is_playing():
            self.player.pause()

    def stop_video(self):
        if self.player.is_playing():
            self.player.stop()

    def restart_video(self):
        if self.player.is_playing():
            self.player.stop()
        self.play_video()

    def play_fullscreen(self, item):
        self.channel_list_widget.hide()  # إخفاء قائمة القنوات
        self.play_button.hide()          # إخفاء أزرار التحكم
        self.pause_button.hide()         
        self.stop_button.hide()         
        self.restart_button.hide()       
        self.setWindowFlag(Qt.FramelessWindowHint, True)  # إزالة الحواف
        self.showFullScreen()  # وضع النافذة في ملء الشاشة
        self.play_video(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.channel_list_widget.show()  # إظهار قائمة القنوات
            self.play_button.show()           # إظهار الأزرار
            self.pause_button.show()
            self.stop_button.show()
            self.restart_button.show()
            self.setWindowFlag(Qt.FramelessWindowHint, False)  # استعادة الحواف
            self.showNormal()  # العودة إلى وضع النافذة العادية

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
