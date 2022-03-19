import sys
import time
from menu import Menu, QApplication
from multiprocessing import Process, Pipe


class CloudpickleWrapper():
    def __init__(self, x):
        self.x = x
    
    def __getstate__(self):
        import cloudpickle
        return cloudpickle.dumps(self.x)
    
    def __setstate__(self, ob):
        import pickle
        self.x = pickle.loads(ob)

def worker(conn, menu_creator):

    app = QApplication(sys.argv)
    menu = menu_creator.x(conn=conn)
    menu.show()
    app.exec_()



if __name__ == "__main__":
    parent, child = Pipe()

    p = Process(target=worker, args=(child, CloudpickleWrapper(Menu)))

    p.daemon=True
    p.start()
 
    while True:

        print(parent.recv())

        parent.send({"目标分配结果" : [1,2,3,4]})
        parent.send({"目标行为理解" : [1,2,3,4]})
        parent.send({"决策时间" : [1,2,3,4]})

        time.sleep(1)

        parent.send({"目标分配结果" : [1,3,3,4]})
        parent.send({"目标行为理解" : [1,"需要",3,4]})
        parent.send({"决策时间" : [1,3,3,4]})



