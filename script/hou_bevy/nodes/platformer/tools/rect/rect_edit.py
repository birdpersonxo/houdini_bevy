# rect_tool.py
import hou
import hou_bevy.nodes.platformer.geometry as platformer_geom
from hou import Vector3


class EditRect:
    MSG = "Move the mouse over the geometry."

    def __init__(self, state_instance):
        self.state = state_instance

        ## mesh data
        self.selected_prim = None

        face = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Face,
            "face",
            params={
                "style": hou.drawableGeometryFaceStyle.Plain,
                "color1": (0.5, 4.0, 0.0, 0.3),
            },
        )

        line = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Line,
            "line",
            params={
                "color1": (0.1, 0.1, 0.8, 1.0),
                "style": hou.drawableGeometryLineStyle.Plain,
                "line_width": 1,
            },
        )

        self.selected_guide = hou.GeometryDrawableGroup("selected_guide")
        self.selected_guide.addDrawable(face)
        self.selected_guide.addDrawable(line)

        self.selected_edge = hou.GeometryDrawableGroup("selected_edge")

        selected_line = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Line,
            "line",
            params={
                "color1": (1, 1.0, 0.8, 1.0),
                "style": hou.drawableGeometryLineStyle.Plain,
                "line_width": 1,
            },
        )
        point = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Point,
            "point",
            params={
                "num_rings": 2,
                "radius": 6,
                "color1": (1.0, 0.1, 0.1, 1.0),
                "style": hou.drawableGeometryPointStyle.LinearCircle,
            },
        )
        self.selected_edge.addDrawable(selected_line)
        self.selected_edge.addDrawable(point)

    def show(self, visible):
        self.selected_guide.show(visible)

    def onResume(self, kwargs):
        self.show(True)
        self.selected_edge.show(True)
        self.state.scene_viewer.setPromptMessage(EditRect.MSG)

    def onInterrupt(self):
        self.show(False)
        self.selected_edge.show(False)

    def onDeleteRect(self):
        if self.selected_prim and self.poly_geo:
            geo = self.state.stash.geometry().freeze()
            geo.deletePrims([self.selected_prim], keep_points=False)
            self.state.node.parm("stash").set(geo)
            self.onRemoveSelectedPrim()

    def onRemoveSelectedPrim(self):
        self.selected_prim = None
        self.poly_geo = None
        # self.selected_guide.setGeometry(self.poly_geo)
        self.selected_guide.show(False)

    def onEditRect(self, ui_event):
        device = ui_event.device()
        origin, direction = ui_event.ray()
        min_dist = float("inf")

        geometry = self.state.node.geometry()
        position = hou.Vector3()
        normal = hou.Vector3()
        uvw = hou.Vector3()
        intersected = geometry.intersect(origin, direction, position, normal, uvw)

        # PRIM SELECTION
        if intersected != -1:
            prim = geometry.prim(intersected)
            primnum = prim.number()

            # on click
            if device.isLeftButton():
                self.selected_prim = prim
                # print(self.selected_prim)
                # print(self.selected_prim.number())

                ## hightlight face
                poly_points = geometry.prim(primnum).points()
                self.poly_geo = hou.Geometry()
                poly = self.poly_geo.createPolygon()
                for pt in poly_points:
                    point = self.poly_geo.createPoint()
                    point.setPosition(pt.position())
                    poly.addVertex(point)

                # update the drawable
                self.selected_guide.setGeometry(self.poly_geo)
                self.show(True)
        else:
            if device.isLeftButton():
                self.onRemoveSelectedPrim()

        # EDGE SELECTION
        # if self.selected_prim and self.poly_geo:
        #     # find to closes points
        #     cursor = hou.Vector3(origin[0], origin[1], 0)
        #     nearest_points = self.poly_geo.nearestPoints(cursor, 3, max_radius=1000)
        #     print(nearest_points)

        #     if len(nearest_points) >= 2:
        #         if len(nearest_points) == 2:
        #             ## make draw the edge
        #             self.closest_edge = self.poly_geo.findEdge(
        #                 nearest_points[0], nearest_points[1]
        #             )

        #             ## draw guide
        #             edge_geo = hou.Geometry()
        #             self.selected_edge.setGeometry(edge_geo)
        #             point0 = edge_geo.createPoint()
        #             point0.setPosition(nearest_points[0].position())

        #             point1 = edge_geo.createPoint()
        #             point1.setPosition(nearest_points[1].position())

        #             poly = edge_geo.createPolygon()
        #             poly.addVertex(point0)
        #             poly.addVertex(point1)

        #             self.selected_edge.show(True)

        #         else:
        #             for i in range(len(nearest_points)):
        #                 for j in range(i + 1, len(nearest_points)):
        #                     edge = self.poly_geo.findEdge(
        #                         nearest_points[i], nearest_points[j]
        #                     )
        #                     self.closest_edge = edge
        #                     # if edge:
        #                     #     verts = edge.vertices()
        #                     #     p0 = verts[0].point().position()
        #                     #     p1 = verts[1].point().position()
        #                     #     closest = self.closestPointOnSegment(p0, p1, cursor)
        #                     #     dist = (closest - cursor).length()

        #                     #     if dist < min_dist:
        #                     #         min_dist = dist
        #                     #         self.closest_edge = edge
        #                     #         self.closest_point_on_edge = closest

        #     if self.closest_edge:
        #         # print(self.closest_edge, "closest edge")
        #         pass

    def closestPointOnSegment(self, a, b, p):
        """Return closest point on segment AB to point P"""
        ab = b - a
        t = (p - a).dot(ab) / ab.dot(ab)
        t = max(0, min(1, t))
        return a + ab * t
