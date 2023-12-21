from pathlib import Path
from typing import Dict
from typing import List
from typing import TypedDict

from compas_viewer import DATA
from compas_viewer.configurations import Config


class MouseConfigType(TypedDict):
    """
    The type template for the mouse only.
    """

    zoom: Dict[str, str]
    pan: Dict[str, str]
    rotate: Dict[str, str]
    boxselection: Dict[str, str]
    box_deselection: Dict[str, str]
    selection: Dict[str, str]


class KeyConfigType(TypedDict):
    """
    The type template for the key only.
    """

    name: str
    keys: List[str]


class ControllerConfigType(TypedDict):
    """
    The type template for the `controller.json`.
    """

    mouse: MouseConfigType
    keys: List[KeyConfigType]


class KeyConfig(Config):
    """
    The class representation for the key only.

    Parameters
    ----------
    config : KeyConfigType
        A TypedDict with defined keys and types.
    """

    def __init__(self, config: KeyConfigType) -> None:
        super(KeyConfig, self).__init__(config)
        self.name = config["name"]
        self.keys = config["keys"]


class ControllerConfig(Config):
    """
    The class representation for the `controller.json` of the class : :class:`compas_viewer.controller.Render`
    The controller.json contains all the settings about controlling the viewer: mouse, keys, ...

    Parameters
    ----------
    config : ControllerConfigType
        A TypedDict with defined keys and types.
    """

    def __init__(self, config: ControllerConfigType) -> None:
        super(ControllerConfig, self).__init__(config)
        self.pan = config["mouse"]["pan"]
        self.zoom = config["mouse"]["zoom"]
        self.rotate = config["mouse"]["rotate"]
        self.boxselection = config["mouse"]["boxselection"]
        self.selection: str = config["mouse"]["selection"]["mouse"]
        self.multiselection: str = config["mouse"]["selection"]["multiselection"]
        self.deletion: str = config["mouse"]["selection"]["deselection"]
        for key in config["keys"]:
            setattr(self, key["name"], KeyConfig(key))

    @classmethod
    def from_default(cls) -> "ControllerConfig":
        controller_config = ControllerConfig.from_json(Path(DATA, "default_config", "controller.json"))
        assert isinstance(controller_config, ControllerConfig)
        return controller_config

    @classmethod
    def from_json(cls, filepath) -> "ControllerConfig":
        controller_config = super().from_json(filepath)
        assert isinstance(controller_config, ControllerConfig)
        return controller_config
