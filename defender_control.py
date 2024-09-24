import os
import sys
import base64
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore  # 导入QtGui用于设置图标
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QImage

base64_icon = """
AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhEA25URAduWEh3blhJr25YSQduWEgfcmBEA15IUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADZlxEA3JUTANuWEhbblhJ225YS0duWEvzblhLo25YSqNuWEjnblhIF25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEgXblhJK25YSx9uWEvzblhL025YS59uWEv/blhL/25YS6tuWEofblhIX25YSANuWDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhIN25YSfNuWEu/blhL925YSvNuWElLblhKI25YS/9uWEv/blhL/25YS/duWErnblhIu25cSANuWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSEtuWEpfblhL725YS59uWEnnblhIT25YSANuWEn/blhL/25YS/9uWEv/blhL/25YS/9uWEtTblhJB25UTANyXEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEg3blhKU25YS/duWEtHblhJB25YRAduWEgDblhIA25YSf9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEtjblhI525YSANuWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDalhIG25YSgduWEvvblhLI25YSL9uWEQDblhMAAAAAANuWEgDblhJ/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEsrblhIn25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADclhMA2pYRANuWElrblhL125YSzduWEi/blhIA2pcRAAAAAAAAAAAA25YSANuWEn/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEq/blhIU25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhIj25YS1tuWEubblhI925YSANuWEQAAAAAAAAAAAAAAAADblhIA25YSf9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/duWEnTinRYA25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSBNuWEpfblhL625YScsh/AADblhIAAAAAAAAAAAAAAAAAAAAAANuWEgDblhJ/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS3tuWEinblhIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhI+25YS7duWErzblhIP25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEn/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YSlNuWEQPblhIAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA3JYTAtuWEp3blhL325YSTduWEgDclhMAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSf9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhLi25YSLNuWEgAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhIt25YS5duWEr/blhIO25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhJ/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhKA25YSANqWEgAAAAAAAAAAAAAAAAAAAAAA25YSANuWEmnblhL925YSYNuWEgDclxEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEn/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEsHblhIP25YSAAAAAAAAAAAAAAAAANuWEgDblhIE25YSpduWEurblhIr25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSf9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS89uWEkPblhIAAAAAAAAAAAAAAAAA25YSANuWEiDblhLg25YSuNqWEhralRIT2pUSFNqVEhTalRIU2pUSFNqVEhTalRIU2pUSFNqVEhHblhJ/25YS7tuWEuvblhLr25YS69uWEuvblhLr25YS69uWEuvblhLr25YS69uWEvfblhL/25YSa9uWEgAAAAAAAAAAAAAAAADblhIA25YSPNuWEvXblhLo25YS0NuWEtDblhLQ25YS0NuWEtDblhLQ25YS0NuWEtDblhLQ25YS0tuWEn/alhIt2pYSL9qWEi/alhIv2pYSL9qWEi/alhIv2pYSL9qWEi/alhIt25YSm9uWEv/blhKR25cSANuVEgAAAAAAAAAAANuWEgDblhJN25YS+tuWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YSf9uWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhJb25YS/9uWErvblhIJ25YSAAAAAAAAAAAA25YSANuWEmrblhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhJ/25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEkDblhL525YS2NuWEhnblhIAAAAAAAAAAADblhIA25YSfNuWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEn/blhIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSP9uWEvjblhLl25YSJNuWEgAAAAAAAAAAANuWEgDblhKH25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YSf9uWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhI725YS9duWEurblhIr25YSAAAAAAAAAAAA25YSANuWEoPblhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhJ/25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YSANuWEj7blhL325YS59uWEibblhIAAAAAAAAAAADblhIA25YSdtuWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEn/blhIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25YSP9uWEvjblhLc25YSG9uWEgAAAAAAAAAAANuWEgDblhJY25YS/NuWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YSf9uWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEgDblhJK25YS/NuWEsbblhIN25YSAAAAAAAAAAAA25YSANuWEkDblhL225YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhJ/25YSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANuWEQDblRID25YSBduWEnjblhL/25YSo9uWEQLblhIAAAAAAAAAAADblhIA25YSKtuWEufblhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEn/blhIAAAAAAAAAAADclxIA3JcRAtuWEhfblhI425YSctuWEqPblhK+25YS5NuWEv/blhJ025YSAAAAAAAAAAAAAAAAANuWEgDblhIK25YSnNuWEtbblhLj25YS9tuWEv/blhL/25YS/9uWEv/blhL/25YS/9uWEv/blhL/25YSf9uWEgDblhIA25YSCduWEjnblhKK25YS1tuWEvPblhL/25YS/tuWEvDblhLb25YSzNuWEkbblhIAAAAAAAAAAAAAAAAA25USANuVEQDblhIM25YSFtuWEiTblhJC25YSdduWEp7blhLV25YS/NuWEv/blhL/25YS/9uWEv/blhJ/2IcYANuWEkHblhKl25YS8duWEv/blhLt25YStNuWEorblhJY25YSMNuWEhrblhIR25YSBNuWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblhIA25cTAduWEh3blhJi25YSutuWEvjblhL/25YS/9uWEpfblhKF25YS7NuWEv/blhLb25YSf9uWEjbblhIH3JUSANuYEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA25YQANuWEgDblhIQ25YSVtuWEsjblhL825YS89uWEvzblhLp25YShtuWEiXdlxEB3JYSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANyXEQDXlBUA25YSGduWEoXblhLu25YSw9uWEjzclxID3JYSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADblRIA2pUSBtuWEkzblhIj2pYSANyWEgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA//g////wD///wAf//4AD//8CAf/+BgD//B4Af/w+AD/4fgAf8H4AH/D+AA/h/gAP4f4AD+P+AAfD/gAHwAAAB8AAAAfAAP/DwAD/w8AA/8PAAP/DwAD/w8AA/8PAAP/DwAD/A8AA8AfAAMAHwACAB/8AAf//4Af///gf///8f/8=
"""

class DefenderControlApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.version = "1.0.0"  # 设置版本号
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Windows Defender Control - {self.version}')  # 在标题栏中显示版本号


        icon_data = base64.b64decode(base64_icon)
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        # 设置窗口图标
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        # 缩小窗口尺寸到500x250
        self.setGeometry(500, 300, 500, 250)

        # 创建按钮并调整位置和大小
        disable_button = QtWidgets.QPushButton('禁用 Defender', self)
        disable_button.clicked.connect(self.disable_defender)
        disable_button.setGeometry(150, 50, 200, 50)  # 调整位置和大小

        enable_button = QtWidgets.QPushButton('启用 Defender', self)
        enable_button.clicked.connect(self.enable_defender)
        enable_button.setGeometry(150, 120, 200, 50)  # 调整位置和大小

        # 添加 "Powered by liliuwei" 替换为您的 GitHub 项目地址
        powered_label = QtWidgets.QLabel('<a href="https://github.com/liliuwei/defender-control">GitHub 项目地址</a>', self)
        powered_label.setGeometry(10, 220, 480, 20)  # 设置标签的位置和大小
        powered_label.setAlignment(QtCore.Qt.AlignCenter)  # 居中对齐
        powered_label.setStyleSheet('color: gray; font-size: 12px;')  # 设置样式
        powered_label.setOpenExternalLinks(True)  # 启用点击打开外部链接

    def disable_defender(self):
        try:
            # 将多个注册表修改命令写入批处理文件
            with open('disable_defender.bat', 'w') as f:
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableAntiSpyware" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableOnAccessProtection" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableBehaviorMonitoring" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableScanOnRealtimeEnable" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableIOAVProtection" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /v "DisableRealtimeMonitoring" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v "DisableBlockAtFirstSeen" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v "SubmitSamplesConsent" /t REG_DWORD /d 2 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /v "SubmitSamplesConsent" /t REG_DWORD /d 2 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableCloudProtection" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /v "DisableQuickScan" /t REG_DWORD /d 1 /f' + '\n')
                f.write(r'reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows Defender\Features" /v "DisableScheduledScan" /t REG_DWORD /d 1 /f' + '\n')
            # 运行批处理文件
            subprocess.run('disable_defender.bat', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove('disable_defender.bat')  # 删除批处理文件
            self.show_message("成功", "Windows Defender已禁用", QMessageBox.Information)
        except Exception as e:
            self.show_message("错误", f"操作失败: {e}", QMessageBox.Critical)

    def enable_defender(self):
        try:
            # 将多个注册表删除命令写入批处理文件
            with open('enable_defender.bat', 'w') as f:
                f.write(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender" /f' + '\n')
                f.write(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" /f' + '\n')
                f.write(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender\Spynet" /f' + '\n')

            # 运行批处理文件
            subprocess.run('enable_defender.bat', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove('enable_defender.bat')  # 删除批处理文件
            self.show_message("成功", "Windows Defender已启用", QMessageBox.Information)
        except Exception as e:
            self.show_message("错误", f"操作失败: {e}", QMessageBox.Critical)

    def show_message(self, title, message, icon):
        msg = QMessageBox(self)
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DefenderControlApp()
    window.show()
    sys.exit(app.exec_())
