"""
This package provides scene object plugins for visualizing COMPAS objects in `compas_viewer`.
"""
from compas.scene import register
from compas.plugins import plugin
from .sceneobject import ViewerSceneObject
from compas.datastructures import Mesh, Network
from compas.geometry import Point, Line, Vector


from .meshobject import MeshObject
from .networkobject import NetworkObject
from .pointobject import PointObject
from .lineobject import LineObject
from .vectorobject import VectorObject
from .tagobject import TagObject, Tag
from .gridobject import GridObject, Grid


@plugin(category="drawing-utils", requires=["compas_viewer"])
def clear(guids=None):
    pass


@plugin(category="drawing-utils", requires=["compas_viewer"])
def redraw():
    pass


@plugin(category="factories", requires=["compas_viewer"])
def register_scene_objects():
    register(Mesh, MeshObject, context="Viewer")
    register(Network, NetworkObject, context="Viewer")
    register(Point, PointObject, context="Viewer")
    register(Line, LineObject, context="Viewer")
    register(Tag, TagObject, context="Viewer")
    register(Grid, GridObject, context="Viewer")
    register(Vector, VectorObject, context="Viewer")


__all__ = [
    "ViewerSceneObject",
    "MeshObject",
    "PointObject",
    "LineObject",
    "TagObject",
    "Tag",
    "GridObject",
    "Grid",
    "Vector",
    "VectorObject",
]
