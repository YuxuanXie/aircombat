from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QApplication, QWidget, QLineEdit, QGridLayout
import sys
import time
from util import generate_pos, generate_pos_per_scene
import numpy as np
import random

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
targetInfo["坐标攻击"] = {}
targetInfo["随遇攻击"] = {}
targetInfo["反辐射攻击"] = {}


for value in targetInfo.values():
    targetInfo["混合目标"].update(value)
    targetInfo["坐标攻击"].update(value)
    targetInfo["随遇攻击"].update(value)
    targetInfo["反辐射攻击"].update(value)


def generate_scene():
    in_air = False if random.random() < 0.5 else True
    pos, target_pos = generate_pos_per_scene(4, in_air=in_air, mix=True)

    target_info = targetInfo["混合目标"]
    sample = np.random.randint(0, len(target_info), size=4)
    move = [False] * 4 
    threaten = []
    value = []
    
    for each in sample:
        t,v = list(target_info.values())[each]
        threaten.append(t)
        value.append(v)

    return pos, target_pos, move, threaten, value


class Menu(QMainWindow):
    def __init__(self, paranet=None, conn=None):
        super(QMainWindow,self).__init__(paranet)
        self.resize(400, 100)
        self.setWindowTitle("选择被攻击目标")
        self.buttonNames = ["地面基础设施", "地面移动目标", "海面目标", "空中目标", "混合目标"]
        self.scensNames = ["坐标攻击", "随遇攻击", "反辐射攻击"]

        self.buttonInstances = [QPushButton(s) for s in self.buttonNames]
        self.taskInstances = [QPushButton(s) for s in self.scensNames]
        self.agent_buttonInstances = [QPushButton(f"飞机{i+1}号") for i in range(4)]
        self.textInstances = [QLineEdit() for i in range(4)]
        self.attackInstances = [QLineEdit() for i in range(4)]
        self.gestureParseInstances = [QLineEdit() for i in range(4)]
        self.timeInstances = [QLineEdit() for i in range(4)]
        self.runAwayInstances = [QLineEdit() for i in range(4)]
        self.weaponInstances = [QLineEdit() for i in range(4)]
        self.radioInstances = [QLineEdit() for i in range(4)]

        self.conn=conn


        layout = QGridLayout()
        row = 0

        # First row : list of scens
        [layout.addWidget(each, row, id) for id, each in enumerate(self.buttonInstances)]
        [each.clicked.connect(self.onButtonClick) for each in self.buttonInstances]
        row += 1
        
        # Second row : list of scens
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.taskInstances)]
        [each.clicked.connect(self.onButtonClick) for each in self.taskInstances]
        row += 1

        # Third row : agent names
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.agent_buttonInstances)]
        row += 1

        # Fourth row : assigned target
        layout.addWidget(QPushButton("攻击优先级"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.attackInstances)] 
        row += 1

        # Fifth row : assigned target
        layout.addWidget(QPushButton("目标分配结果"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.textInstances)] 
        row += 1

        # Sixth row : gestureParse
        layout.addWidget(QPushButton("目标行为理解"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.gestureParseInstances)] 
        row += 1

        # 7th row : time
        layout.addWidget(QPushButton("决策时间"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.timeInstances)] 
        row += 1

        # 8th row : time
        layout.addWidget(QPushButton("是否规避"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.runAwayInstances)] 
        row += 1

        # 9th row : time
        layout.addWidget(QPushButton("武器投放"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.weaponInstances)] 
        row += 1

        # 10th row : time
        layout.addWidget(QPushButton("射频管控"), row, 0)
        [layout.addWidget(each, row, id+1) for id, each in enumerate(self.radioInstances)] 
        row += 1

        main_frame = QWidget()
        main_frame.setLayout(layout)
        self.setCentralWidget(main_frame)

        self.counter = 1

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


            # pos = menu.pos
            # target_pos = menu.target_pos
            # threaten = menu.threaten
            # move = menu.move
            # value = menu.value

        self.conn.send({
            "pos" : self.pos,
            "target_pos" : self.target_pos,
            "threaten" : self.threaten,
            "move" : self.move, 
            "value" : self.value
        })
        
        while True:
            if self.conn:
                info = self.conn.recv()
                print(info)

                key, data = [ (k,v) for k, v in info.items() ][0]

                # data = ['是' if each < 0 else '否' for each in data]
                data = [ str(each) for each in data]

                if key == "目标分配结果":
                    for i in range(len(self.textInstances)):
                        self.textInstances[i].setPlaceholderText(data[i])

                if key == "目标行为理解":
                    for i in range(len(self.gestureParseInstances)):
                        self.gestureParseInstances[i].setPlaceholderText(data[i])

                if key == "决策时间":
                    for i in range(len(self.timeInstances)):
                        self.timeInstances[i].setPlaceholderText(data[i]) 

                if key == "是否规避设置":
                    for i in range(len(self.timeInstances)):
                        self.timeInstances[i].setPlaceholderText(data[i]) 
                        
                time.sleep(0.5)
                QApplication.processEvents()

                # self.textInstances[0].setPlaceholderText(f'{self.counter}')
                # self.counter += 1
                # time.sleep(1.0)
        # self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    app.exec_()



