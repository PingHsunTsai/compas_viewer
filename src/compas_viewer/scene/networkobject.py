from typing import List
from typing import Optional
from typing import Tuple

from compas.colors import Color
from compas.datastructures import Network
from compas.geometry import Point
from compas.scene import NetworkObject as BaseNetworkObject

from .sceneobject import ViewerSceneObject


class NetworkObject(ViewerSceneObject, BaseNetworkObject):
    """Object for displaying COMPAS network data structures.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        The network data structure.
    **kwargs : Dict, optional
        Additional options for the :class:`compas_viewer.scene.ViewerSceneObject`.

    """

    def __init__(self, network: Network, **kwargs):
        super(NetworkObject, self).__init__(network=network, **kwargs)
        self.show_points = True
        # TODO: add show_nodes in base NetworkObject. Change show_points to _show_points as internal variable.

        self._points_data = self._get_points_data()
        self._lines_data = self._get_lines_data()

    def _get_points_data(self) -> Optional[Tuple[List[Point], List[Color], List[List[int]]]]:
        if not self.show_points:
            return None
        positions = []
        colors = []
        elements = []
        i = 0

        for node in self.network.nodes():
            assert isinstance(node, int)
            positions.append(self.network.nodes_attributes("xyz")[node])
            colors.append(self.pointscolor.get(node, self.pointscolor["_default"]))  # type: ignore
            elements.append([i])
            i += 1
        return positions, colors, elements

    def _get_lines_data(self) -> Optional[Tuple[List[Point], List[Color], List[List[int]]]]:
        if not self.show_lines:
            return None
        positions = []
        colors = []
        elements = []
        i = 0

        for u, v in self.network.edges():
            color = self.linescolor.get((u, v), self.linescolor["_default"])  # type: ignore
            positions.append(self.network.nodes_attributes("xyz")[u])
            positions.append(self.network.nodes_attributes("xyz")[v])
            colors.append(color)
            colors.append(color)
            elements.append([i + 0, i + 1])
            i += 2
        return positions, colors, elements

    def draw_nodes(self):
        # TODO: evaluate if this needs to be enforced.
        pass

    def draw_edges(self):
        pass