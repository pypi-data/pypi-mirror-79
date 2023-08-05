import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore
import os

_root = os.path.dirname(__file__)
from vtgui.gui import *
from vtgui.fields import *
from wk import PointDict
import json
import typing
import random
import logging, sys
from .utils import split_list,KillableThread






def make_layout(dic, dst, column=1):
    fields = []
    for k, v in dic.items():
        if not isinstance(v, Field):
            if isinstance(v, VirtualField):
                v.update(parent=dst)
                v.update(name=k)
                v = make_field(**v)
            else:
                v = make_field(name=k, default=v, parent=dst)
        dst[v.name] = v.default
        fields.append(v)
    ratios = [len(fields) / column] * column
    columns = split_list(fields, ratios=ratios)
    cols = []
    for column in columns:
        cols.append(VVBoxLayout()(*column))
        cols.append(VSpacing(50))
    layout = VHBoxLayout(size_average=True)(*cols).detach()
    return layout


class VirtualField(PointDict):
    def __init__(self, title=None, field_type=None, description=None, default=None, options=None):
        if options and field_type is None:
            field_type = 'union'
        super().__init__(title=title, field_type=field_type, description=description, default=default, options=options)


class SelectDir(VirtualField):
    def __init__(self, default=None, title=None, description=None):
        if default is None:
            default = ''
        super().__init__(default=default, title=title, description=description, field_type='dir')


class SelectFile(VirtualField):
    def __init__(self, default=None, title=None, description=None):
        if default is None:
            default = ''
        super().__init__(default=default, title=title, description=description, field_type='file')


def make_field(name, parent, title=None, field_type=None, description=None, default=None, options=None):
    if title is None:
        title = name
    if field_type is None:
        if default is not None:
            field_type = type(default)
        else:
            field_type = str
    if isinstance(field_type, type):
        field_type = field_type.__name__
    type_dict = {
        'union': ListSelectField,
        'bool': BoolField,
        'str': TextField,
        'int': IntField,
        'float': FloatField,
        'file': FileChooserField,
        'dir': DirChooserField,
    }
    field_type = type_dict[field_type]
    return field_type(name=name, title=title, description=description, default=default, options=options, parent=parent)






def make_app(data, callback, dst=None, columns=3):
    if dst is None:
        dst = {}

    class MainWindow(QWidget):
        app = QApplication(sys.argv)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # 设置窗口标题
            self.setWindowTitle('简易浏览器')
            # 设置窗口大小900*600
            self.resize(1300, 700)
            self.show()
            self.init()

        def init(self):
            # 添加TextBrowser
            console=VConsole()
            self.console=console
            target=lambda: callback(dst)
            layout = VVBoxLayout()(
                make_layout(data, dst, columns),
                VHBoxLayout()(
                    VPushButton('run', onclicked=lambda: KillableThread.start_new_thread(target=target,name='test')),
                    VPushButton('stop', onclicked=lambda: KillableThread.kill_thread_by_name('test')),
                    VStretch(),
                ),
                VHBoxLayout()(console),
            )
            self.setLayout(layout.detach())
            console.serve_as_std()

        def run(self):
            self.show()
            sys.exit(self.app.exec_())

    win = MainWindow()
    return win


if __name__ == '__main__':
    # make_app()
    pass
