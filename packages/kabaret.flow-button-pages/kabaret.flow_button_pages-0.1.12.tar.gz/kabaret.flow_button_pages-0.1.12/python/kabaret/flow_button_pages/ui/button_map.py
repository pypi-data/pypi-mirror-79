from kabaret.app.ui.gui.widgets.flow.flow_view import (
    CustomPageWidget,
    QtWidgets,
    QtCore,
)
from kabaret.app.ui.gui.widgets.flow_layout import FlowLayout

from .html_button import HtmlButton


class ItemButton(HtmlButton):
    def __init__(self, oid, page, button_height=100, thumbnail=None):
        super(ItemButton, self).__init__(page)
        self.page = page
        self.oid = oid

        html = """
        <center><img src="{pict}" height={height}></center>
        <hr>
        <h2>{name}</h2>
        """.format(
            **dict(
                pict=thumbnail, height=button_height, name=self.oid.rsplit("/", 1)[-1]
            )
        )
        self.set_html(html)

    def _on_clicked(self):
        self.page.page.goto(self.oid)


class ButtonMapPage(CustomPageWidget):
    def get_map(self):
        # This is quite ugly, we should not access actors in
        # the GUI part (it could be on another process...)
        # But I'm kind of fed up following that rule without
        # ever actually encountering a situation where it stands...
        map = self.session.get_actor("Flow").get_object(self.oid)
        return map

    def build(self):
        vlo = QtWidgets.QVBoxLayout()
        self.setLayout(vlo)
        layout = FlowLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        vlo.addLayout(layout)

        button_height = 200
        default_thumbnail = ("icons.gui", "bigb-reel-orange")

        for item in self.get_map().mapped_items():
            b = ItemButton(item.oid(), self, button_height, default_thumbnail)
            layout.addWidget(b)

        vlo.addSpacing(100)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_context_menu)

    def _on_context_menu(self):
        print("RMB")
