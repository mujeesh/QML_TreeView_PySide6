/*****************************************************************************

*****************  QML TreeView ************************

Author: Mujeesh
email: mujeesh@gmail.com
date: 23-01-2023
*****************************************************************************/
import QtQuick
import QtQml.Models
import QtQuick.Layouts
import QtQuick.Controls
import Qt.labs.qmlmodels


ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "TreeView"

    ColumnLayout {
        HorizontalHeaderView {
            id: horizontalHeader
            Layout.preferredHeight: 45
            Layout.preferredWidth: 900
            syncView: tree_view_id
            clip: true

            delegate: Rectangle {
                implicitHeight: horizontalHeader.height
                implicitWidth: 120

                Text {
                    text: display
                    anchors.centerIn: parent
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 13
                    font.bold: true
                }
            }
        }
        TreeView {
            id: tree_view_id
            Layout.preferredWidth: 600
            Layout.preferredHeight: 800

            columnSpacing: 1
            rowSpacing: 1
            clip: true
            boundsBehavior: Flickable.StopAtBounds
            model: tree_view_model
            delegate: chooser


            DelegateChooser {
                id: chooser

                DelegateChoice {
                    column: 0
                    id: treeDelegate

                    delegate: Rectangle {
                        id: nameId

                        implicitWidth: 120
                        implicitHeight: 35
                        readonly property real indent: 20
                        readonly property real padding: 5

                        // Assigned to by TreeView:
                        required property TreeView treeView
                        required property bool isTreeNode
                        required property bool expanded
                        required property int hasChildren
                        required property int depth
                        required property bool selected


                        function leftMouseButtonClicked() {
                            treeView.toggleExpanded(row)
                            var elementIndex = tree_view_id.modelIndex(row, 0)

                            treeView.currentRow = row
                            treeView.currentColumn = column
                        }

                        Text {
                            id: indicator
                            visible: nameId.isTreeNode && nameId.hasChildren
                            x: padding + (nameId.depth * nameId.indent)
                            padding: 5
                            anchors.verticalCenter: nameId.verticalCenter
                            text: "▸"
                            font{
                                pixelSize: 18
                                bold: true
                            }

                            rotation: nameId.expanded ? 90 : 0

                        }
                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton

                            onClicked: function(mouse)
                            {
                                if (mouse.button === Qt.LeftButton)
                                {
                                    leftMouseButtonClicked()
                                }
                            }
                        }
                        Text {
                            id: label
                            x: padding + (nameId.isTreeNode ? (nameId.depth + 1) * nameId.indent : 0)
                            width: nameId.width - nameId.padding - x
                            clip: true
                            text: model.name
                            anchors.verticalCenter: nameId.verticalCenter
                        }
                    }
                }
                DelegateChoice {
                    column: 1
                    id:projectChoice

                    delegate: Rectangle {
                        id: projectDelegate
                        implicitWidth: 120
                        implicitHeight: 35
                        Label{
                            id:projectLabel
                            objectName: "projectLabel"
                            anchors.centerIn: parent
                            text: model.project
                        }
                    }
                }
                DelegateChoice {
                    column: 2
                    id:clientChice

                    delegate: Rectangle {
                        id: clientDelegate
                        implicitWidth: 120
                        implicitHeight: 35
                        Label{
                            id:clientLabel
                            objectName: "clientLabel"
                            anchors.centerIn: parent
                            text: model.client
                        }
                    }
                }

            }
        }
    }


}
