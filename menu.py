from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QApplication, QWidget
import sys

"""
Name : Menu
Function : Render different classes of objects and send it to the remote aircraft by clicking
   
"""

targetInfo = {}
"字典{目标类型：字典{（威胁度，共计价值）}}"
targetInfo["地面基础设施"] = {
    "airport": (0, 10),
    "bridge": (0, 5),
    "oilery": (0, 20),
}

targetInfo["地面移动目标"] = {
    "tank": (5, 5),
    "radarCar": (10, 10),
    "missileCar": (20, 20),
}

targetInfo["海面目标"] = {
    "island": (5, 5),
    "freighter": (0, 10),
    "bodyguard": (10, 20),
}

targetInfo["空中目标"] = {
    "scoutPlane": (5, 10),
}


class Menu(QMainWindow):
    def __init__(self, paranet=None):
        super(QMainWindow,self).__init__(paranet)
        self.resize(400, 100)
        self.setWindowTitle("选择被攻击目标")
        self.buttonNames = ["地面基础设施", "地面移动目标", "海面目标", "空中目标", "混合目标"]
        self.buttonInstances = [QPushButton(s) for s in self.buttonNames]

        layout = QVBoxLayout()
        [layout.addWidget(each) for each in self.buttonInstances]
        [each.clicked.connect(self.onButtonClick) for each in self.buttonInstances]
        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

    def onButtonClick(self):
        # sender 是发送信号的对象，此处发送信号的对象是button1按钮
        sender = self.sender()
        print(sender.text() + ' 被按下了')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())