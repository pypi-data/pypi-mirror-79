import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui,QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

_root = os.path.dirname(__file__)
from vtgui.gui import *
from vtgui.fields import *
from wk import PointDict
from wcf import models_names
import json
import typing
import random
import logging,sys

def split_list(lis,ratios,shuffle=False):
    if not lis:
        return None
    if len(lis)<len(ratios):
        raise Exception("List is not long enough to be split.")
    import numpy as np
    if shuffle:
        random.shuffle(lis)
    ratios=np.array(ratios)
    ratios=ratios/ratios.sum()
    nums=ratios*len(lis)
    nums=np.round(nums).astype(int)
    total=len(lis)
    splits=[]
    current_index=0
    for i,num in enumerate(nums):
        end_point=min(current_index+num,total)
        batch=lis[current_index:end_point]
        splits.append(batch)
        current_index=end_point
    return splits
models=[
    models_names.resnet10,
    models_names.resnet18,
    models_names.resnet50,
    models_names.shufflenet_v2_x0_5,
    models_names.shufflenet_v2_x1_0,
]

def make_layout(dic,dst,column=1):
    fields=[]
    for k,v in dic.items():
        if not isinstance(v,Field):
            if isinstance(v,VirtualField):
                v.update(parent=dst)
                v=make_field(**v)
            else:
                v=make_field(name=k,default=v,parent=dst)
        dst[v.name]=v.default
        fields.append(v)
    ratios=[len(fields)/column]*column
    columns=split_list(fields,ratios=ratios)
    cols=[]
    for column in columns:
        cols.append(VVBoxLayout()(*column))
    layout=VHBoxLayout(size_average=True)(*cols).detach()
    return layout

class VirtualField(PointDict):
    def __init__(self,name,title=None,field_type=None,description=None,default=None,options=None):
        super().__init__(name=name,title=title,field_type=field_type,description=description,default=default,options=options)

def make_field(name,parent,title=None,field_type=None,description=None,default=None,options=None):
    if title is None:
        title=name
    if field_type is None:
        if default is not None:
            field_type=type(default)
        else:
            field_type=str
    if isinstance(field_type,type):
        field_type=field_type.__name__
    type_dict={
        'union':ListSelectField,
        'bool':BoolField,
        'str':TextField,
        'int':IntField,
        'float':FloatField,
        'file':FileChooserField,
        'dir':DirChooserField,
    }
    field_type=type_dict[field_type]
    return field_type(name=name,title=title,description=description,default=default,options=options,parent=parent)



class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))
class WorkThread(QThread):
    # 自定义信号对象。参数str就代表这个信号可以传一个字符串
    trigger = pyqtSignal(str)

    def __init__(self,target):
        # 初始化函数
        super(WorkThread, self).__init__()
        self.target=target

    def run(self):
        #重写线程执行的run函数
        #触发自定义信号
       self.target()

def make_app(data,callback,dst={}):
    class MainWindow(QWidget):
        app= QApplication(sys.argv)
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # 设置窗口标题
            self.setWindowTitle('简易浏览器')
            # 设置窗口大小900*600
            self.resize(1300, 700)
            self.show()
            self.init()

        def outputWritten(self,text):
            cursor = self.textEdit.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertText(text)
            self.textEdit.setTextCursor(cursor)
            self.textEdit.ensureCursorVisible()
        def init(self):
            # 添加TextBrowser
            outputBox = QTextEdit()
            outputBox.setReadOnly(True)
            # 设置文本内容
            self.workThread = WorkThread(target=lambda :callback(dst))

            layout = VVBoxLayout()(
                make_layout(data,dst,3),
                VHBoxLayout()(
                    VPushButton('save',onclicked=lambda :self.workThread.start(), ),
                    VStretch(),
                ),
                VHBoxLayout()( outputBox),
            )
            self.setLayout(layout.detach())
            self.textEdit=outputBox
            sys.stdout = EmittingStream(textWritten=self.outputWritten)
            sys.stderr = EmittingStream(textWritten=self.outputWritten)

        def run(self):
            self.show()
            sys.exit(self.app.exec_())
    win=MainWindow()
    return win
if __name__ == '__main__':
    # make_app()
    pass
