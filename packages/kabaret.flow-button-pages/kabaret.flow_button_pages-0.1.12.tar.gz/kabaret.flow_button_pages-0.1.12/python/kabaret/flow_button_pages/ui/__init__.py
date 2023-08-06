from qtpy import QtWidgets, QtGui, QtCore

from kabaret.app.ui.gui.widgets.flow.flow_view import CustomPageWidget
from kabaret.app.ui.gui.widgets.flow_layout import FlowLayout
from kabaret.app import resources

from .html_button import HtmlButton

from ..button_home import IconChoice, ColorChoice


class ProjectButton(HtmlButton):
    @classmethod
    def get_default_thumbnail(cls):
        return resources.get(
            "icons.fbp",
            "{}-{}".format(
                IconChoice.default(),
                ColorChoice.default(),
            ),
        )

    def __init__(
        self, home_page, name, info, button_height=100, default_thumbnail=None
    ):
        super(ProjectButton, self).__init__(home_page)
        self.home_page = home_page
        self.name = name
        self.info = info

        settings = self.get_settings_object()
        settings = settings.as_dict()
        thumbnail = settings.get("thumbnail")
        color = settings.get("color")

        html = (
            "<center>" "<font size=+3><b>" "{}" "</font></b>" "</center>".format(name)
        )

        status = info["status"]
        if status is not None:
            if status == "Archived":
                status = "OOP"
            status_pict = resources.get("icons.status", status)
            html += (
                "<hr><center>"
                '<img src="{}"><br>'
                "{}"
                "</center>".format(
                    status_pict,
                    status,
                )
            )

        if not thumbnail:
            thumbnail = default_thumbnail
        if not thumbnail:
            thumbnail = self.get_default_thumbnail()
        if isinstance(thumbnail, (tuple, list)):
            try:
                thumbnail = resources.get(*thumbnail)
            except (TypeError, resources.NotFoundError, resources.ResourcesError):
                pass

        html = '<center><img src="{}" height={}>{}</center>'.format(
            thumbnail, button_height, html
        )

        if color:
            html = "<font color={}>{}</font>".format(color, html)

        self.set_html(html)

    def get_settings_object(self):
        return self.home_page.get_home().projects_settings.get_project_settings(
            self.name
        )

    def goto_settings(self):
        settings = self.get_settings_object()
        self.home_page.page.goto(settings.oid())

    def run_thumbnail_preset(self):
        settings = self.get_settings_object()
        self.home_page.page.show_action_dialog(settings.thumbnail.presets.oid())

    def _on_context_menu(self):
        m = QtWidgets.QMenu(self)
        m.addAction("Configure", self.goto_settings)
        m.addAction("Select Thumbnail preset", self.run_thumbnail_preset)
        m.exec_(QtGui.QCursor.pos())

    def _on_clicked(self):
        self.goto_project()

    def goto_project(self):
        self.home_page.page.goto("/" + self.name)


class ButtonHomePage(CustomPageWidget):
    def _get_project_infos(self):
        # This is quite uggly, we should not access actors in
        # the GUI part (it could be on another process...)
        # But I'm kind of fed up following that rule without
        # ever actually encountering a situation where it stands...
        flow_actor = self.session.get_actor("Flow")
        return flow_actor.get_projects_info()

    def get_home(self):
        # This is quite ugly, we should not access actors in
        # the GUI part (it could be on another process...)
        # But I'm kind of fed up following that rule without
        # ever actually encountering a situation where it stands...
        home = self.session.get_actor("Flow").get_object(self.oid)
        return home

    def _build_all(self):
        vlo = self.layout()

        projects_infos = self._get_project_infos()
        if projects_infos:
            layout = FlowLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            vlo.addLayout(layout)

            home_settings = self.get_home().home_settings
            show_status = home_settings.show_status.get()
            show_archived = home_settings.show_archived.get()
            button_height = home_settings.button_height.get()
            default_thumbnail = home_settings.default_thumbnail.get()
            for name, info in projects_infos:
                if not show_archived and info["status"] == "Archived":
                    continue
                if not show_status:
                    info["status"] = None  # mmmmmouai.... c'est moche.
                b = ProjectButton(self, name, info, button_height, default_thumbnail)
                layout.addWidget(b)

            vlo.addSpacing(100)
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.on_context_menu)

        else:
            welcome = """
            <H2>Welcome !</H2>
            It looks like you have no Project yet.<br>
            You can edit the <b>settings</b> to create one:
            """
            label = QtWidgets.QLabel(welcome, self)
            button = QtWidgets.QPushButton("Edit Settings...")
            button.clicked.connect(self.on_goto_settings)

            vlo.addWidget(label)
            vlo.addWidget(button)

    def _clear_layout(self, lo):
        li = lo.takeAt(0)
        while li:
            w = li.widget()
            if w:
                w.deleteLater()
            clo = li.layout()
            if clo:
                self._clear_layout(clo)
            li = lo.takeAt(0)

    def _clear_all(self):
        vlo = self.layout()
        self._clear_layout(vlo)

    def build(self):
        vlo = QtWidgets.QVBoxLayout()
        self.setLayout(vlo)
        self._build_all()

    def on_context_menu(self):
        m = QtWidgets.QMenu()
        m.addAction("Admin...", self.on_goto_settings)
        m.exec_(QtGui.QCursor.pos())

    def on_goto_settings(self):
        self.get_home().use_custom_page = False
        self.page.goto(None)

    def on_touch_event(self, oid):
        if oid == self.oid:
            self.setEnabled(False)
            try:
                self._clear_all()
                self._build_all()
            finally:
                self.setEnabled(True)

    def die(self):
        pass
