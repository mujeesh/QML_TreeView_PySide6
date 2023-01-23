"""
####################################
PySide6 QML TreeView Example
###################################
Author: Mujeesh
email: mujeesh@gmail.com
date: 23-01-2023
"""
from __future__ import annotations
import sys
from typing import Dict, List, Union, Optional

import PySide6
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QAbstractItemModel, QByteArray, Qt, QObject, QModelIndex, Property, Signal, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


PORTFOLIO = [{"Company1": {"Project1": "Client1"}},
             {"Company2": {"Project2": "Client2"}},
             {"Company3": {"Project3": "Client3"}},
             {"Company4": {"Project4": "Client4"}},
             {"Company5": {"Project5": "Client5"}},]

EMPTY_STR: str = ""


class BaseItem(QObject):
    def __init__(self, name: str = EMPTY_STR, project: str = EMPTY_STR,
                 client: str = EMPTY_STR, parent: Optional[QObject] = None) -> None:
        super().__init__()
        self.children: List[QObject] = []  # type: ignore
        self.name: str = name
        self.project = project
        self.client = client
        self._parent = parent

    def add_child(self, child: QObject) -> None:
        """
        :param child: QObject
        """
        self.children.append(child)

    def parent(self) -> Optional[QObject]:
        return self._parent


class ClientItem(BaseItem):
    def __init__(self, client_name: str, parent: QObject) -> None:
        super().__init__(client=client_name, parent=parent)


class ProjectItem(BaseItem):
    def __init__(self, project_name: str, parent: QObject) -> None:
        super().__init__(project=project_name, parent=parent)


class CompanyItem(BaseItem):
    def __init__(self, company_name: str, parent: QObject) -> None:
        super().__init__(name=company_name, parent=parent)


class RootItem(QObject):
    def __init__(self):
        super().__init__(None)
        self.name = "ROOT"
        self.project = EMPTY_STR
        self.client = EMPTY_STR
        self.children = []

    def add_child(self, child):
        """
        :param child: TreeItem
        """
        self.children.append(child)


class TreeViewModel(QAbstractItemModel):
    name_role: int = Qt.UserRole + 1  # type: ignore
    project_role: int = Qt.UserRole + 2  # type: ignore
    client_role: int = Qt.UserRole + 3  # type: ignore

    def __init__(self) -> None:
        super(TreeViewModel, self).__init__(None)
        self.root = RootItem()
        self.set_up_tree_items()

    def roleNames(self) -> Dict[int, QByteArray]:
        roles = {
            TreeViewModel.name_role: QByteArray(b'name'),
            TreeViewModel.project_role: QByteArray(b'project'),
            TreeViewModel.client_role: QByteArray(b'client'),
        }
        return roles

    def set_up_tree_items(self) -> None:
        for company_details in PORTFOLIO:
            for company_name, project_details in company_details.items():
                company_item = CompanyItem(company_name=company_name, parent=self.root)
                self.root.add_child(company_item)
                for project_name, client_name in project_details.items():
                    project_item = ProjectItem(project_name=project_name, parent=company_item)
                    company_item.add_child(project_item)
                    client_item = ClientItem(client_name=client_name, parent=project_item)
                    project_item.add_child(client_item)

    def get_item(self, index: PySide6.QtCore.QModelIndex):  # type: ignore
        """
        :param index: QModelIndex
        :return: TreeItem
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item

        return self.root

    def index(self, row: int, column: int, parent: PySide6.QtCore.QModelIndex) -> PySide6.QtCore.QModelIndex:  # type: ignore
        """This is to provide index's to the views and delegates to use when accessing data.
           :param:row
           :param:column
           :param:parent
           :return:QModelIndex
        """

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        parent_item = self.get_item(parent)
        child_item = parent_item.children[row]

        if child_item:
            model_index = self.createIndex(row, column, child_item)
        else:
            model_index = QModelIndex()
        return model_index

    def rowCount(self, parent):  # type: ignore
        """
        :param parent: QModelIndex
        :return: int
        """
        if not parent.isValid():
            parent_item = self.root
        else:
            parent_item = parent.internalPointer()

        return len(parent_item.children)

    def columnCount(self, index=QModelIndex()):
        """ Returns the number of columns the model holds. """
        return 3

    def data(self, index, role=Qt.DisplayRole):
        """ Depending on the index and role given, return data. If not
            returning data, return None (PySide equivalent of QT's
            "invalid QVariant").
        """
        if not index.isValid():
            return "None"

        item = index.internalPointer()
        if not 0 <= index.row() < len(item.parent().children):
            return None

        if role == TreeViewModel.name_role:
            name = item.name
            return name
        elif role == TreeViewModel.project_role:
            return item.project
        elif role == TreeViewModel.client_role:
            return item.client

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            if section == 0:
                return "Company Name"
            elif section == 1:
                return "Project"
            elif section == 2:
                return "Client"

        return None

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        return True

    def setData(self, index, value, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given
            index and role.
        """
        return False

    def flags(self, index):
        """
        :param index: QModelIndex
        :return: int (flag)
        """
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index: QModelIndex):
        """
        Should return the parent of the item with the given QModelIndex

        :param index: QModelIndex
        :return: QModelIndex
        """
        item = self.get_item(index)
        parent_item = item.parent()

        if parent_item == self.root:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.children.index(item), 0, parent_item)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    model = TreeViewModel()
    engine.rootContext().setContextProperty("tree_view_model", model)

    url = QUrl.fromLocalFile('qml/tree_view.qml')
    engine.load(url)
    sys.exit(app.exec())
