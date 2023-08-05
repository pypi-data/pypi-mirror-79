import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from vtgui.gui import *
import os
_root=os.path.dirname(__file__)
from wk import PointDict

class Event(PointDict):
    # target=None
    # data=None
    pass


def getWidgetData(widget):
    if isinstance(widget,(QLineEdit)):
        return widget.text()
    elif isinstance(widget,QComboBox):
        return widget.currentText()
    elif isinstance(widget,QCheckBox):
        return widget.isChecked()
    else:
        raise
def setWidgetData(widget,data):
    if isinstance(widget,(QLineEdit)):
        return widget.setText(data)
    elif isinstance(widget,QComboBox):
        return widget.setCurrentText(data)
    elif isinstance(widget,QCheckBox):
        return widget.setChecked(data)
    else:
        raise
def getSignalDataChanged(widget):
    if isinstance(widget,(QLineEdit)):
        return widget.textChanged
    elif isinstance(widget,QComboBox):
        return widget.currentTextChanged
    elif isinstance(widget,QCheckBox):
        return widget.stateChanged
    else:
        raise
class Field(VWidget):
    title = None
    description = None
    default = None
    convert_func = None
    onchange = None
    options=None
    range=None
    def __init__(self,name=None,title=None,description=None,default=None,convert_func=None,onchange=None,options=None,dtype=None,parent=None,**kwargs):
        if not convert_func:
            if default is not None:
                convert_func=type(default)
        convert_func = convert_func or (lambda x: x)
        self.name=name
        self.title=title
        self.description=description
        self.default=default
        self.convert_func=self.convert_func or convert_func
        self.options=options
        self.dtype=dtype
        for k,v in kwargs.items():
            setattr(self,k,v)
        self.make_widget()
        if onchange:
            self.setOnchange(onchange)
        else:
            if parent is not None and name is not None:
                def make(parent,name):
                    def func(e):
                        parent[name]=e.data
                    return func
                self.setOnchange(make(parent,name))
    def make_widget(self):
        self.inner_widget = self.make_inner_widget()
        self.widget = self.make_outter_widget()
    def make_outter_widget(self,widget=None):
        ws=[]
        if self.title:
            ws.append(QLabel(self.title))
        # if self.default:
        #     ws.append(QLabel(self.description))
        ws.append(widget or self.inner_widget)
        return VHBoxLayout()(
                *ws
            ).detach()
        # return VHBoxLayout()(
        #     VVBoxLayout()(
        #         *ws
        #     )
        # ).detach()
    def make_inner_widget(self):
        raise NotImplementedError
    def setData(self,data):
        setWidgetData(self.inner_widget,str(data))
    def getData(self):
        data=getWidgetData(self.inner_widget)
        try:
            return self.convert_func(data)
        except ValueError:
            return data


    def setOnchange(self,func):
        def make_func(target):
            def wrapper():
                e=Event(data=self.getData(), target=target)
                func(e)
            return wrapper
        getSignalDataChanged(self.inner_widget).connect(make_func(self))
class TextField(Field):
    def make_inner_widget(self):
        w=QLineEdit()
        w.setText(str(self.default) or '')
        return w
class IntField(TextField):
    convert_func = int
class FloatField(TextField):
    convert_func = float

class ListSelectField(Field):
    def make_inner_widget(self):
        w=QComboBox()
        w.addItems([str(x) for x in self.options])
        w.setCurrentText(str(self.default))
        return w
class FileChooserField(Field):
    def make_widget(self):
        lineEdit = QLineEdit()
        lineEdit.setText(self.default or '')
        btn = QPushButton('选择文件')
        def make_func(lineEdit):
            def func():
                path = QFileDialog().getOpenFileName(caption='选取文件', directory='./')[0]
                lineEdit.setText(path)
            return func
        btn.clicked.connect(make_func(lineEdit))
        self.inner_widget=lineEdit
        widget = VHBoxLayout()(
            btn, lineEdit
        )
        self.widget=self.make_outter_widget(widget)

class DirChooserField(Field):
    def make_widget(self):
        lineEdit = QLineEdit()
        lineEdit.setText(self.default or '')
        btn = QPushButton('选择文件夹')
        def make_func(lineEdit):
            def func():
                path = QFileDialog().getExistingDirectory(caption='选取文件夹', directory='./')
                lineEdit.setText(path)
            return func
        btn.clicked.connect(make_func(lineEdit))
        self.inner_widget=lineEdit
        widget = VHBoxLayout()(
            btn, lineEdit
        ).detach()
        self.widget=self.make_outter_widget(widget)


class BoolField(Field):
    def make_inner_widget(self):
        w=QCheckBox()
        w.setChecked(bool(self.default))
        return w
