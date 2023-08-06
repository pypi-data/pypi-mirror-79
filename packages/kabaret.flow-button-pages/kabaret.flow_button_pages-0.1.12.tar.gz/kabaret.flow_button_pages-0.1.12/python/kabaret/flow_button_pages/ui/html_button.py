from __future__ import print_function

from qtpy import QtWidgets, QtGui, QtCore


class HtmlButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(HtmlButton, self).__init__(parent)

        self.clicked.connect(self._on_clicked)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

    def _on_context_menu(self):
        pass

    def _on_clicked(self):
        pass

    def set_html(self, html):
        text = QtGui.QTextDocument()
        text.setHtml(html)
        text.setTextWidth(text.size().width())

        pix = QtGui.QPixmap(text.size().width(), text.size().height())
        pix.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pix)
        text.drawContents(painter, QtCore.QRectF(pix.rect()))
        painter.end()

        icon = QtGui.QIcon(pix)
        self.setText("")
        self.setIcon(icon)
        self.setIconSize(pix.rect().size())

        margins = QtCore.QSize(10, 10)
        self.setFixedSize(pix.size() + margins)
