from kabaret import flow
from kabaret.app.actors.flow.generic_home_flow import HomeRoot, Home


class _Choice(flow.values.ChoiceValue):
    @classmethod
    def default(cls):
        return cls.CHOICES[0]


class IconChoice(_Choice):
    CHOICES = ["clap", "reel", "screen"]


class ColorChoice(_Choice):
    CHOICES = ["blue", "green", "orange", "pink", "red"]


class SelectThumbnailAction(flow.Action):
    _thumbnail_owner = flow.Parent(2)
    _value = flow.Parent()

    icon = flow.Param(IconChoice.default(), IconChoice).watched()
    color = flow.Param(ColorChoice.default(), ColorChoice).watched()

    def get_buttons(self):
        self._revert_value = self._value.get()
        self.message.set(
            "Configure Thumbnail for {}".format(self._thumbnail_owner.name())
        )
        return ["Close", "Revert"]

    def child_value_changed(self, child_value):
        name = "{}-{}".format(self.icon.get(), self.color.get())
        self._value.set(("icons.fbp", name))

    def run(self, button):
        if button == "Revert":
            self._value.set(self._revert_value)
            self.root().Home.touch()
        return


class ThumbnailValue(flow.values.Value):
    """
    A Value with a preset action that generate a thumbnail resource
    identifier from a bunch of choices.
    """

    presets = flow.Child(SelectThumbnailAction)


class ProjectSettings(flow.Object):
    doc = flow.Label(
        """
        Color:
            Use an html compatible value, like "#0088FF".

        Thumbnail:
            Use a resource identifier like "['icons.gui', 'star']",
            or a file path (but avoid backslashes !),
            or a data URI for the thumbnail.

        To further more configure the Home, right click an empty space
        close to one of the Projects and select "Admin...".
        """
    )
    color = flow.Param("").watched()
    thumbnail = flow.Param("", ThumbnailValue).watched()

    def child_value_changed(self, child_value):
        self.root().Home.touch()

    def as_dict(self):
        d = dict(
            color=self.color.get(),
            thumbnail=self.thumbnail.get(),
        )
        return d


class ProjectsSettings(flow.Map):
    @classmethod
    def _create_value_store(cls, parent, name):
        """
        The DKSHome is a SessionObject (base classe of `Home`)
        so it uses a MemoryValueStore and nothing is saved to the
        db (this is needed by `Home`).
        But we need to save the settings so we re-configure to the
        default value store here (the one from the root).
        """
        return parent.root()._mng.value_store

    @classmethod
    def mapped_type(cls):
        return ProjectSettings

    def get_project_settings(self, project_name):
        if not self.has_mapped_name(project_name):
            settings = self.add(project_name)
        else:
            settings = self.get_mapped(project_name)
        return settings

    def get_settings_dict(self, project_name):
        return self.get_project_settings().as_dict()


class HomeSettings(flow.Object):
    @classmethod
    def _create_value_store(cls, parent, name):
        """
        The DKSHome is a SessionObject (base classe of `Home`)
        so it uses a MemoryValueStore and nothing is saved to the
        db (this is needed by `Home`).
        But we need to save the settings so we re-configure to the
        default value store here (the one from the root).
        """
        return parent.root()._mng.value_store

    show_status = flow.BoolParam()
    show_archived = flow.SessionParam(False).ui(editor="bool")
    button_height = flow.IntParam(100)
    default_thumbnail = flow.Param("", ThumbnailValue)


class ShowButtonHomeAction(flow.Action):
    ICON = ("icons.gui", "home-outline")
    _home = flow.Parent()

    def needs_dialog(self):
        return False

    def run(self, button):
        self._home.use_custom_page = True
        return self.get_result(goto=self._home.oid())


class ButtonHome(Home):
    home_settings = flow.Child(HomeSettings)
    projects_settings = flow.Child(ProjectsSettings)

    back = flow.Child(ShowButtonHomeAction)

    def __init__(self, *args, **kwargs):
        super(ButtonHome, self).__init__(*args, **kwargs)
        self.use_custom_page = True

    def _fill_ui(self, ui):
        from .ui import ButtonHomePage

        if self.use_custom_page:
            ui["custom_page"] = (
                ButtonHomePage.__module__ + "." + ButtonHomePage.__name__
            )


class ButtonHomeRoot(HomeRoot):
    Home = flow.Child(ButtonHome)

    def set_flow_actor(self, flow_actor):
        self.flow_actor = flow_actor
