from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QApplication, QWidget
import sys
from util import generate_pos, generate_pos_per_scene
import numpy as np

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

targetInfo["混合目标"] = {}

for value in targetInfo.values():
    targetInfo["混合目标"].update(value)

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
        self.pos = None
        self.target_pos = None
        self.threaten = None
        self.value = None

    def onButtonClick(self):
        # sender 是发送信号的对象，此处发送信号的对象是button1按钮
        sender = self.sender()
        print(sender.text() + ' 被按下了')
        mix = True if "混合目标" in sender.text() else False
        in_air = True if "空中目标" in sender.text() else False

        self.pos, self.target_pos = generate_pos_per_scene(4, in_air=in_air, mix=mix)

        target_info = targetInfo[sender.text()]
        sample = np.random.randint(0, len(target_info), size=4)
        self.move = [True] * 4 if "移动" in sender.text() else [False] * 4
        self.threaten = []
        self.value = []
        
        for each in sample:
            t,v = list(target_info.values())[each]
            self.threaten.append(t)
            self.value.append(v)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    app.exec_()



