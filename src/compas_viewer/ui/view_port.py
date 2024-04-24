from typing import TYPE_CHECKING
from OpenGL import GL
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from compas_viewer.components.default_component_factory import ViewerSetting, ViewerTreeForm

if TYPE_CHECKING:
    from .ui import UI

class OpenGLWidget(QOpenGLWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initializeGL()

    def clear(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)  # type: ignore

    def initializeGL(self):
        GL.glClearColor(0.7, 0.7, 0.7, 1.0)
        GL.glPolygonOffset(1.0, 1.0)
        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glEnable(GL.GL_POINT_SMOOTH)
        GL.glEnable(GL.GL_LINE_SMOOTH)
        GL.glEnable(GL.GL_FRAMEBUFFER_SRGB)

    def resizeGL(self, w: int, h: int):
        GL.glViewport(0, 0, w, h)


class View3D:
    def __init__(self, viewport: "ViewPort") -> None:
        self.viewport = viewport
        self.viewmode = "perspective"
        self.renderer = OpenGLWidget()

class SideBarRightDefault:
    pass

class SideBarRight:
    def __init__(self, viewport: "ViewPort") -> None:
        self.viewport = viewport
        self.config = viewport.ui.viewer.config.ui.sidebar
        self.setting = ViewerSetting()
        self.tree_form = ViewerTreeForm(viewport.ui.viewer.scene)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Vertical)
        self.splitter.setChildrenCollapsible(True)
        # self.scenetree = SceneTreeView()
        # self.objectlist = ObjectListView()
        # self.camerasettings = CameraSettings()

        
        # self.splitter.addWidget(self.scenetree.widget)
        # self.splitter.addWidget(self.objectlist.widget)
        # slot 1
        self.splitter.addWidget(self.tree_form.tree_view())
        # slot 2
        self.splitter.addWidget(self.setting.camera_all_setting())
        self.splitter.setHidden(not self.config.show)


class ViewPort:
    def __init__(self, ui: "UI"):
        self.ui = ui
        self.view3d = View3D(self)
        self.sidebar = SideBarRight(self)
        self.splitter = QtWidgets.QSplitter()

        self.splitter.addWidget(self.view3d.renderer)
        self.splitter.addWidget(self.sidebar.splitter)
        self.ui.window.centralWidget().layout().addWidget(self.splitter)