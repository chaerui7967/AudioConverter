import sys
import os
import subprocess
import ctypes
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QListWidget, QLabel, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QIcon
from pycaw.pycaw import AudioUtilities
import comtypes

# 윈도우 작업표시줄 아이콘 개별 표시를 위한 설정
try:
    myappid = 'my.audio.switcher.v1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass

class AudioSwitcher(QWidget):
    def __init__(self, icon:str, nircmd_path:str):
        super().__init__()
        try: comtypes.CoInitialize()
        except: pass
        
        # 1. 변수 초기화 
        self.history = []
        self.current_active_device = None  # 현재 활성화된 장치 저장 변수
        self.icon = icon
        self.nircmd_path = nircmd_path
        
        self.initUI()
        self.refresh_devices()
        
        # 2. 시작 시 현재 기본 장치가 무엇인지 찾아두기
        self.set_initial_device()

    def initUI(self):
        self.setWindowTitle('Audio Converter')
        self.setFixedSize(360, 450)
        self.setStyleSheet("background-color: #ffffff;")

        # 아이콘 설정 (icon.ico 파일이 같은 폴더에 있어야 함)
        if os.path.exists(self.icon):
            self.setWindowIcon(QIcon(self.icon))

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.label = QLabel('🔊 Audio Devices')
        self.label.setStyleSheet("font-size: 13px; font-weight: bold; color: #333;")
        layout.addWidget(self.label)

        # 리스트 위젯 및 스크롤바 통합 스타일
        self.device_list = QListWidget()
        self.device_list.setStyleSheet("""
            QListWidget { 
                border: 1px solid #e0e0e0; 
                border-radius: 4px; 
                font-size: 12px;
                background-color: white;
            }
            QListWidget::item { 
                padding: 2px 8px;
                border-bottom: 1px solid #f9f9f9;
                color: #000000;
            }
            QListWidget::item:hover {
                background-color: #f2f2f2;
            }
            QListWidget::item:selected { 
                background-color: #0078d4; 
                color: #ffffff; 
            }
            
            /* --- 스크롤바 스타일 설정 --- */
            QScrollBar:vertical {
                border: none;
                background: #f1f1f1;
                width: 8px; /* 스크롤바 너비 슬림하게 */
                margin: 0px 0px 0px 0px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #ccc; /* 스크롤 핸들 색상 */
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #aaa; /* 마우스 올렸을 때 더 진하게 */
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px; /* 화살표 버튼 제거 */
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none; /* 배경 트랙 투명하게 */
            }
        """)
        layout.addWidget(self.device_list)

        # 전환 버튼
        self.btn_change = QPushButton('선택 장치로 전환')
        self.btn_change.clicked.connect(self.change_device)
        self.btn_change.setStyleSheet("""
            QPushButton { 
                background-color: #0078d4; color: white; padding: 10px; 
                border-radius: 4px; font-weight: bold; font-size: 13px; 
            }
            QPushButton:hover { background-color: #005a9e; }
        """)
        layout.addWidget(self.btn_change)

        # 하단 버튼부
        sub_layout = QHBoxLayout()
        self.btn_undo = QPushButton('되돌리기')
        self.btn_undo.clicked.connect(self.undo_device)
        self.btn_undo.setEnabled(False)
        
        self.btn_refresh = QPushButton('목록 새로고침')
        self.btn_refresh.clicked.connect(self.refresh_devices)

        sub_btn_style = """
            QPushButton { 
                padding: 6px; background: #fdfdfd; border: 1px solid #ccc; 
                border-radius: 4px; font-size: 11px;
            }
            QPushButton:hover { background: #f0f0f0; }
        """
        self.btn_undo.setStyleSheet(sub_btn_style)
        self.btn_refresh.setStyleSheet(sub_btn_style)

        sub_layout.addWidget(self.btn_undo)
        sub_layout.addWidget(self.btn_refresh)
        layout.addLayout(sub_layout)

        self.setLayout(layout)

    def set_initial_device(self):
        try:
            # 윈도우 멀티미디어 장치 열거
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
            
            # 현재 '기본'으로 설정된 스피커 객체 직접 가져오기
            devices = AudioUtilities.GetSpeakers()
            # 이 객체의 실제 인터페이스를 통해 이름을 확인
            self.current_active_device = devices.FriendlyName
            self.refresh_ui()
        except:
            # 실패 시 목록의 첫 번째를 임시로 잡음
            if self.device_list.count() > 0:
                self.current_active_device = self.device_list.item(0).text()

    def refresh_devices(self):
        
        self.btn_refresh.setText("🔄 불러오는 중...")
        self.btn_refresh.setEnabled(False) # 중복 클릭 방지
        self.device_list.setWindowOpacity(0.5) # 리스트를 살짝 흐리게 
        
        QApplication.processEvents() 

        # 실제 목록 갱신 작업
        self.device_list.clear()
        try:
            from pycaw.pycaw import AudioUtilities
            devices = AudioUtilities.GetAllDevices()
            unique_names = []
            
            for device in devices:
                name = device.FriendlyName
                if name:
                    # 마이크/입력장치 제외 필터링
                    if any(x in name.lower() for x in ["microphone", "마이크", "input", "line in"]):
                        continue
                    if name not in unique_names:
                        unique_names.append(name)
            
            for name in sorted(unique_names):
                self.device_list.addItem(name)
                
        except Exception as e:
            self.device_list.addItem(f"오류 발생: {e}")

        # 0.3s delay
        import time
        time.sleep(0.3)

        self.device_list.setWindowOpacity(1.0) # 다시 선명
        self.btn_refresh.setText("목록 새로고침")
        self.btn_refresh.setEnabled(True)
        
        # device 동기화
        self.set_initial_device()

    def change_device(self):
        selected = self.device_list.currentItem()
        if not selected: return
        
        target_name = selected.text()
        
        # 경로 설정
        if getattr(sys, 'frozen', False):
            nircmd_path = os.path.join(sys._MEIPASS, self.nircmd_path)
        else:
            nircmd_path = os.path.abspath(self.nircmd_path)

        try:
            # 히스토리 기록
            if self.current_active_device:
                self.history.append(self.current_active_device)
                self.btn_undo.setEnabled(True)
            
            simple_name = target_name.split('(')[0].strip()
            subprocess.run([nircmd_path, 'setdefaultsounddevice', simple_name, '1'], check=True)

            self.current_active_device = target_name
            self.refresh_ui()

        except Exception as e:
            QMessageBox.critical(self, "전환 실패", f"NirCmd가 장치를 찾지 못함:\n{e}")

    def undo_device(self):
        if not self.history: return
        
        # 히스토리에서 '직전 장치' 꺼내기
        prev_device = self.history.pop()
        simple_name = prev_device.split('(')[0].strip()
        
        try:
            subprocess.run([self.nircmd_path, 'setdefaultsounddevice', simple_name, '1'], check=True)
            
            # 현재 상태를 되돌린 장치로 업데이트
            self.current_active_device = prev_device
            
            if not self.history:
                self.btn_undo.setEnabled(False)
            
            self.refresh_ui()

        except Exception as e:
            QMessageBox.warning(self, "오류", f"되돌리기 실패: {e}")


    def refresh_ui(self):

        if len(self.current_active_device) >= 20:
            self.label.setText(f"현재: {self.current_active_device[:20]}...") 
        else:
            self.label.setText(f"현재: {self.current_active_device}")

        for i in range(self.device_list.count()):
            if self.device_list.item(i).text() == self.current_active_device:
                self.device_list.setCurrentRow(i)
                break
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioSwitcher(icon='../source/icon.ico', nircmd_path='../source/nircmd.exe')
    ex.show()
    sys.exit(app.exec())