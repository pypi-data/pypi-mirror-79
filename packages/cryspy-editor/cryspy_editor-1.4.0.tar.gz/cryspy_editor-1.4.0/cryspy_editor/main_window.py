# -*- coding: utf-8 -*-
__author__ = 'ikibalin'
__version__ = "2020_08_21"

import os
import os.path
import sys

from typing import NoReturn
from PyQt5 import QtCore, QtGui, QtWidgets

import json

from cryspy import GlobalN, file_to_globaln, RhoChi

from cryspy_editor.widgets.w_panel import WPanel, \
    find_tree_item_position, L_GLOBAL_CLS
from cryspy_editor.widgets.w_methods import WMethods
from cryspy_editor.widgets.w_baseobj import WBaseObj
from cryspy_editor.widgets.w_dockarea import WDockArea
from cryspy_editor.widgets.w_console import WConsole
from cryspy_editor.widgets.w_function import WFunction

# import importlib
# dir_additional_libraries = d_setup['directory_additional_libraries']


class MyThread(QtCore.QThread):
    """Thread class."""

    signal_start = QtCore.pyqtSignal()
    signal_end = QtCore.pyqtSignal()
    signal_refresh = QtCore.pyqtSignal()
    signal_take_attributes = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.message = None
        self.function = None
        self.arguments = None
        self.output = None

    def run(self):
        """Run."""
        self.signal_start.emit()

        # wpanel = (self.parent()).wpanel

        func = self.function
        arg = self.arguments

        # if isinstance(wpanel, QtWidgets.QTreeWidget):
        #     arg_new = []
        #     for _arg in arg:
        #         flag_arg = False
        #         if isinstance(_arg, str):
        #             l_arg = _arg.split(",")
        #             s_0 = l_arg[0]
        #             level_item_count = w_cpanel.topLevelItemCount()
        #             for _i in range(level_item_count):
        #                 qtree_widget_item = w_cpanel.topLevelItem(_i)
        #                 s_item = str(qtree_widget_item.text(0))
        #                 if (s_item.lower() == s_0.lower()):
        #                     arg_new.append(qtree_widget_item._object)
        #                     flag_arg = True
        #                     break
        #         if not flag_arg:
        #             arg_new.append(_arg)
        # else:
        #     arg_new = arg
        arg_new = arg

        # out = func(*arg_new)
        try:
            out = func(*arg_new)
        except SyntaxError:
            out = "Check the syntax of function"
        except ArithmeticError:
            out = "Arithmetic error"
        except ValueError:
            out = "Error in the input values raised"
        except Exception:
            out = "An unspecified error occurred while function executing."
        self.output = out
        self.signal_end.emit()


class CBuilder(QtWidgets.QMainWindow):
    """
    Builder class.

    Attributes
    ----------
        - f_dir_prog
        - f_dir_data
        - f_file
        - thread
        - wfunction
        - wpanel
        - wconsole
        - object
        - wbaseobj
        - wdockarea
        - wcb_for_stackedwidget
        - wstackwidget
    """

    def __init__(self, f_dir_data=os.path.dirname(__file__)):
        super(CBuilder, self).__init__()

        self.f_dir_prog = os.path.dirname(__file__)
        self.index_curent_item = None

        self.def_actions()
        self.init_widget()

        self.mythread = MyThread(self)
        self.mythread.signal_start.connect(self.start_of_calc_in_thread)
        self.mythread.signal_end.connect(self.end_of_calc_in_thread)
        self.mythread.signal_refresh.connect(self.form_wpanel)

        self.wpanel.set_func_object_clicked(self.onItemClicked)

        self.wmethods.set_wfunction(self.wfunction)
        self.wmethods.set_thread(self.mythread)

        self.wdockarea.set_thread(self.mythread)
        self.wbaseobj.set_thread(self.mythread)

        self.f_dir_data = f_dir_data
        self.f_file = None
        self.wpanel.object = None
        if os.path.isfile(f_dir_data):
            self.f_file = f_dir_data
            self.f_dir_data = os.path.dirname(f_dir_data)

        self.setWindowTitle('CrysPy editor')

        if self.f_file is not None:
            self.setWindowTitle(f'CrysPy editor: {self.f_file:}')
            self.load_globaln()
        else:
            # self.wpanel.object = GlobalN.make_container((), (), "global")
            self.wpanel.object = RhoChi()
            self.form_wpanel()
            self.form_wstackedwidget(self.wpanel.object)
        self.show()

    def def_actions(self):
        """Define actions."""
        f_dir_prog = self.f_dir_prog
        f_dir_prog_icon = os.path.join(f_dir_prog, 'f_icon')
        self.setWindowIcon(
            QtGui.QIcon(os.path.join(f_dir_prog_icon, 'icon.png')))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        self.toolbar = self.addToolBar("Open")

        new_action = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'new.png')), '&New', self)
        new_action.setStatusTip('New')
        new_action.triggered.connect(self.new)
        fileMenu.addAction(new_action)
        self.toolbar.addAction(new_action)

        open_action = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'open.png')), '&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open file')
        open_action.triggered.connect(self.open)
        fileMenu.addAction(open_action)
        self.toolbar.addAction(open_action)

        save_action = QtWidgets.QAction(QtGui.QIcon(
            os.path.join(f_dir_prog_icon, 'save.png')), '&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save')
        save_action.triggered.connect(self.save)

        fileMenu.addAction(save_action)
        self.toolbar.addAction(save_action)

        save_as_action = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(f_dir_prog_icon, 'save_as.png')),
            'Save &as...', self)
        save_as_action.setStatusTip('Save as ...')
        save_as_action.triggered.connect(self.save_as)

        fileMenu.addAction(save_as_action)
        self.toolbar.addAction(save_as_action)

        # refresh_wind = QtWidgets.QAction(
        #     QtGui.QIcon(os.path.join(f_dir_prog_icon, 'refresh.png')),
        #     'Refresh', self)
        # refresh_wind.setStatusTip('Refresh')
        # refresh_wind.triggered.connect(self.form_wpanel)
        # self.toolbar.addAction(refresh_wind)

        open_folder = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(f_dir_prog_icon, 'open_folder.png')),
            'Open folder', self)
        open_folder.setStatusTip('Open folder')
        open_folder.triggered.connect(self.open_folder)
        self.toolbar.addAction(open_folder)

        # flip_action = QtWidgets.QAction(
        #     QtGui.QIcon(os.path.join(f_dir_prog_icon, 'flip.png')),
        #     'Flip representation', self)
        # flip_action.setStatusTip('Flip presentation')
        # flip_action.triggered.connect(self.flip_presenation)
        # self.toolbar.addAction(flip_action)

        fileMenu = menubar.addMenu('&Object manipulations')
        manip_action = QtWidgets.QAction('Switch to global', fileMenu)
        manip_action.object = GlobalN
        manip_action.triggered.connect(self.transfer)
        fileMenu.addAction(manip_action)
        for item_cls in L_GLOBAL_CLS:
            manip_action = QtWidgets.QAction(
                f'Switch to {item_cls.PREFIX:}', fileMenu)
            manip_action.object = item_cls
            manip_action.triggered.connect(self.transfer)
            fileMenu.addAction(manip_action)

        self.statusBar()

    def transfer(self):
        """Transfer GlobalN object to any one."""
        sender = self.sender()
        cls_item = sender.object
        item_old = self.wpanel.object
        if cls_item is GlobalN:
            item_new = cls_item.make_container(
                (), tuple(set([type(item) for item in item_old])), "global")
        else:
            item_new = cls_item()
        item_new.add_items(item_old.items)
        self.wpanel.object = item_new
        self.form_wpanel()
        self.form_wstackedwidget(self.wpanel.object)

    def flip_presenation(self) -> NoReturn:
        """Flip presentation."""
        ind = 1-self.wstackedwidget.currentIndex()
        self.wstackedwidget.setCurrentIndex(ind)

    def init_widget(self) -> NoReturn:
        """Initilize widget."""
        self.location_on_the_screen()

        widget_main = QtWidgets.QWidget(self)
        layout_main = QtWidgets.QVBoxLayout()
        self.wfunction = WFunction(widget_main)

        # First
        layout_main.addWidget(self.wfunction)

        width_m_1 = self.info_width / 6.
        width_m_2 = (3 * self.info_width) / 6.
        width_v_1 = self.info_height * 0.75
        width_v_2 = self.info_height * 0.25

        # Second
        wsplitter = QtWidgets.QSplitter(widget_main)

        # Panel from left site
        self.wpanel = WPanel(wsplitter)
        wsplitter.addWidget(self.wpanel)

        # Central widget constracted from three widgets
        wsplitter_centr = QtWidgets.QSplitter(wsplitter)
        wsplitter_centr.setOrientation(QtCore.Qt.Vertical)

        # 1.
        self.wstackedwidget = QtWidgets.QStackedWidget(wsplitter_centr)
        self.wbaseobj = WBaseObj(self.wstackedwidget)
        self.wdockarea = WDockArea(self.wstackedwidget)
        self.wstackedwidget.addWidget(self.wbaseobj)
        self.wstackedwidget.addWidget(self.wdockarea)
        wsplitter_centr.addWidget(self.wstackedwidget)

        # 2.
        self.wconsole = WConsole(wsplitter_centr)
        wsplitter_centr.addWidget(self.wconsole)

        wsplitter_centr.setSizes([width_v_1, width_v_2])
        wsplitter.addWidget(wsplitter_centr)

        # Panel from right site
        self.wmethods = WMethods(wsplitter)
        wsplitter.addWidget(self.wmethods)

        wsplitter.setSizes([width_m_1, width_m_2, 0])

        layout_main.addWidget(wsplitter)
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)

    def location_on_the_screen(self) -> NoReturn:
        """Location on the screen."""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.setMinimumSize(screen.width() * 1 / 4, screen.height() * 1 / 4)
        self.info_width = screen.width() * 8. / 10.
        self.info_height = screen.height() * 14. / 16.
        self.move(screen.width() / 10, screen.height() / 20)
        self.resize(screen.width() * 8. / 10., screen.height() * 14. / 16.)

    def calc_is_finished(self) -> NoReturn:
        """After calculations."""
        m_box = QtWidgets.QMessageBox(self)
        m_box.setIcon(QtWidgets.QMessageBox.Information)
        m_box.setText("Calculations are finished")
        m_box.setWindowTitle("Message")
        m_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        m_box.exec()

        # self.load_globaln()
    def load_globaln(self) -> NoReturn:
        """Read globaln from file."""
        obj = file_to_globaln(self.f_file)
        self.wpanel.object = obj
        self.form_wpanel()
        self.form_wstackedwidget(obj)
        self.wmethods.get_methods(obj)

    def new(self) -> NoReturn:
        """Define new object."""
        obj = RhoChi()
        self.wpanel.object = obj
        self.form_wpanel()
        self.form_wstackedwidget(obj)
        self.wmethods.get_methods(obj)

    def save(self) -> NoReturn:
        """Save."""
        f_name = self.f_file
        obj = self.wpanel.object
        if type(obj) is RhoChi:
            obj.save_to_file(f_name)
        else:
            with open(f_name, "w") as fid:
                fid.write(str(obj))

    def save_as(self) -> NoReturn:
        """Save as."""
        f_name, okPressed = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Select a file:', self.f_dir_data, "Rcif files (*.rcif)")
        if not (okPressed):
            return None
        self.f_file = f_name
        self.setWindowTitle(f'CrysPy editor: {f_name:}')

        self.f_dir_data = os.path.dirname(f_name)
        os.chdir(os.path.dirname(f_name))
        self.save()

    def open_folder(self) -> NoReturn:
        """Open folder."""
        os.startfile(self.f_dir_data)

    def open(self) -> NoReturn:
        """Open."""
        f_name, okPressed = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Select a cif file:', self.f_dir_data, "All files (*.*)")
        if not (okPressed):
            return None
        self.f_file = f_name
        self.setWindowTitle(f'CrysPy editor: {f_name:}')
        self.f_dir_data = os.path.dirname(f_name)
        os.chdir(os.path.dirname(f_name))
        self.load_globaln()

        f_setup = os.path.join(os.path.dirname(__file__), 'setup.json')
        if os.path.isfile(f_setup):
            d_setup = json.load(open(f_setup, 'r'))
        else:
            d_setup = {}
        d_setup["last_directory"] = f_name
        s_cont = json.dumps(d_setup, sort_keys=True, indent=4)
        with open(f_setup, "w") as fid:
            fid.write(s_cont)

    # @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, QtWidgets.QTreeWidgetItem)
    def onItemClicked(self, it, col):
        """On item clicked."""
        if it is not None:
            self.form_wstackedwidget(it.object)

    def start_of_calc_in_thread(self):
        """Start calculations in thread."""
        cur_item = self.wpanel.currentItem()
        self.index_curent_item = tuple(find_tree_item_position(
            self.wpanel, cur_item))

        ls_out = ["The calculations are running.\n"]
        self.wconsole.setText("\n".join(ls_out))

    def end_of_calc_in_thread(self):
        """End calculations in thread."""
        self.wfunction.calculation_finished()

        thread = self.mythread
        function = thread.function
        function_name = function.__name__
        output = thread.output
        ls_out = []
        ls_out.append(
            f"The function '{function_name:}' is perfomed.\n\nResult is \n")
        ls_out.append(str(output))
        self.wconsole.setText("\n".join(ls_out))

        self.form_wpanel()
        # self.form_wstackedwidget(self.wpanel.object)
        # self.wmethods.get_methods(self.wpanel.object)

        previous_item = self.index_curent_item

        if previous_item is not None:
            wpanel = self.wpanel
            n_main = previous_item[0]
            if n_main < wpanel.columnCount():
                w_item = wpanel.itemAt(n_main, 0)
                if len(previous_item) > 1:
                    for n_ind in previous_item[1:]:
                        if n_ind < w_item.childCount():
                            w_item = w_item.child(n_ind)
                        else:
                            break
        else:
            w_item = self.wpanel.topLevelItem(0)
        self.wpanel.setCurrentItem(w_item)
        self.form_wstackedwidget(w_item.object)
        self.wmethods.get_methods(w_item.object)

        # self.calc_is_finished()

    def form_wpanel(self):
        """Form wpanel."""
        self.wpanel.set_object_global()

    def form_wstackedwidget(self, obj):
        """From stackwidget."""
        self.wbaseobj.set_object(obj)
        self.wdockarea.set_object(obj)
        if self.wdockarea.count() == 0:
            self.wstackedwidget.setCurrentIndex(0)
        else:
            self.wstackedwidget.setCurrentIndex(1)
        self.wmethods.get_methods(obj)


def main_w(l_arg=[]):
    """Make main window."""
    app = QtWidgets.QApplication(l_arg)
    # app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
    app.setStartDragDistance(100)
    f_setup = os.path.join(os.path.dirname(__file__), 'setup.json')
    if len(l_arg) >= 2:
        f_dir_data = os.path.abspath(l_arg[1])
    elif os.path.isfile(f_setup):
        d_setup = json.load(open(f_setup, 'r'))
        f_dir_data = d_setup["last_directory"]
        if not(os.path.isdir(f_dir_data) | os.path.isfile(f_dir_data)):
            f_dir_data = os.getcwd()
            d_setup["last_directory"] = f_dir_data
            s_cont = json.dumps(d_setup, sort_keys=True, indent=4)
            with open(f_setup, "w") as fid:
                fid.write(s_cont)
    else:
        f_dir_data = os.getcwd()
    wobj = CBuilder(f_dir_data)
    sys.exit(app.exec_())


if __name__ == '__main__':
    l_arg = sys.argv
    main_w(l_arg)
