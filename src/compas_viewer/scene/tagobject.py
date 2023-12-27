from os import PathLike
from os import path
from typing import Optional
from typing import Tuple
from typing import Union

from compas.colors import Color
from compas.geometry import Geometry
from compas.geometry import Point
from compas.scene import GeometryObject
from freetype import FT_LOAD_FLAGS
from freetype import Face
from numpy import array
from numpy import linalg
from numpy import zeros
from OpenGL import GL

from compas_viewer import DATA
from compas_viewer.utilities import make_index_buffer
from compas_viewer.utilities import make_vertex_buffer

from .sceneobject import ViewerSceneObject

FONT = path.join(DATA, "default_config", "FreeSans.ttf")


class Tag(Geometry):
    """The geometry class of the tag. A tag is a text label that is always facing the camera.

    Parameters
    ----------
    text : str
        The text of the tag.
    position : :class:`compas.geometry.Point` | tuple[float, float, float]
        The position of the tag.
    color : :class:`compas.colors.Color`, optional
        The color of the tag.
        Default is black.
    height : float, optional
        The height of the tag.
        Default is 50.
    absolute_height : bool, optional
        If True, the height of the tag is calculated based on the distance between the tag and the camera.
        Default is False.
    font : :class:`os.PathLike`, optional
        The font of the tag.
        Default is FreeSans.ttf in the default config folder.

    Attributes
    ----------
    text : str
        The text of the tag.
    position : :class:`compas.geometry.Point`
        The position of the tag.
    color : :class:`compas.colors.Color`
        The color of the tag.
    height : float
        The height of the tag.
    absolute_height : bool
        If True, the height of the tag is calculated based on the distance between the tag and the camera.
    font : :class:`os.PathLike`
        The font of the tag.
    """

    def __eq__(self, other):
        return (
            isinstance(other, Tag)
            and self.text == other.text
            and self.position == other.position
            and self.color == other.color
            and self.height == other.height
            and self.absolute_height == other.absolute_height
            and self.font == other.font
        )

    def __init__(
        self,
        text: str,
        position: Union[Point, Tuple[float, float, float]],
        color: Color = Color(1.0, 1.0, 1.0),
        height: float = 50,
        absolute_height: bool = False,
        font: Optional[PathLike] = None,
    ):
        super().__init__()
        self.text = text
        self.position = Point(*position)
        self.color = color
        self.height = height
        self.absolute_height = absolute_height
        self.font = font or FONT

    def transform(self, transformation):
        """Transform the tag.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation used to transform the geometry.

        Returns
        -------
        None

        """
        self.position.transform(transformation)


class TagObject(ViewerSceneObject, GeometryObject):
    """
    The scene object of the :class:`compas_viewer.scene.Tag` geometry.
    Unlike :class:`compas_viewer.scene.TextObject`, tag object is a sprite always facing the camera.

    Parameters
    ----------
    tag : :class:`compas_viewer.scene.Tag`
        The tag geometry.
    **kwargs : dict, optional
        Additional options for the :class:`compas_viewer.scene.ViewerSceneObject`.
    """

    def __init__(self, tag: Tag, **kwargs):
        super(TagObject, self).__init__(geometry=Tag, **kwargs)
        self._tag = tag

    def init(self):
        self.make_buffers()

    def make_buffers(self):
        self._text_buffer = {
            "positions": make_vertex_buffer(self._tag.position),
            "elements": make_index_buffer([0]),
            "text_texture": self.make_text_texture(),
            "n": 1,
        }

    def make_text_texture(self):
        face = Face(self._tag.font)

        char_width = 48
        char_height = 80
        # the size is specified in 1/64 pixel
        face.set_char_size(64 * char_width)

        text = self._tag.text
        string_buffer = zeros(shape=(char_height, char_width * len(text)))

        for i, c in enumerate(text):
            if c == " ":
                continue
            face.load_char(c, FT_LOAD_FLAGS["FT_LOAD_RENDER"])
            glyph = face.glyph
            bitmap = glyph.bitmap
            char = array(bitmap.buffer)
            char = char.reshape((bitmap.rows, bitmap.width))
            string_buffer[-char.shape[0] :, i * char_width : i * char_width + char.shape[1]] = char  # noqa: E203

        string_buffer = string_buffer.reshape((string_buffer.shape[0] * string_buffer.shape[1]))

        # create glyph texture
        texture = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_R8,
            char_width * len(text),
            char_height,
            0,
            GL.GL_RED,
            GL.GL_UNSIGNED_BYTE,
            string_buffer,
        )
        return texture

    def _calculate_text_height(self, camera_position):
        if self._tag.absolute_height:
            return int(
                (10 * self._tag.height)
                / float(
                    linalg.norm(
                        array(self._tag.position) - array([camera_position.x, camera_position.y, camera_position.z])
                    )
                )
            )

        else:
            return self._tag.height

    def draw(self, shader, camera_position):
        """Draw the object from its buffers"""
        shader.enable_attribute("position")
        shader.uniform4x4("transform", self.matrix)
        shader.uniform1f("object_opacity", self.opacity)
        shader.uniform1i("text_height", self._calculate_text_height(camera_position))
        shader.uniform1i("text_num", len(self._tag.text))
        shader.uniform3f("text_color", self.color)
        shader.uniformText("text_texture", self._text_buffer["text_texture"])
        shader.bind_attribute("position", self._text_buffer["positions"])
        shader.draw_texts(elements=self._text_buffer["elements"], n=self._text_buffer["n"])
        shader.uniform1i("is_text", 0)
        shader.uniform1f("object_opacity", 1)
        shader.disable_attribute("position")

    def update(self):
        super()._update_matrix()
        self.init()
