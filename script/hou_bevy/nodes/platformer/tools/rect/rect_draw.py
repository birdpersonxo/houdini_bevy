# rect_tool.py
import hou
import hou_bevy.nodes.platformer.geometry as platformer_geom
from hou import Vector3


class DrawRect:
    def __init__(self, state_instance):
        """
        Initialize with reference to the main state instance.

        Args:
            state_instance: The main State class instance to access its attributes
        """
        self.state = state_instance

        # Initialize rectangle drawing state
        self.first_point = None
        self.second_point = None
        self.third_point = None
        self.fourth_point = None
        self.first_axis = None
        self.click_count = 0

        self.guides()

    def guides(self):
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

        line = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Line,
            "line",
            params={
                "color1": (0.5, 0.5, 0.5, 1.0),
                "style": hou.drawableGeometryLineStyle.Plain,
                "line_width": 1,
            },
        )

        face = hou.GeometryDrawable(
            self.state.scene_viewer,
            hou.drawableGeometryType.Face,
            "face",
            params={
                "style": hou.drawableGeometryFaceStyle.Plain,
                "color1": (0.0, 0.2, 0.7, 0.5),
            },
        )

        self.state.poly_guide.addDrawable(point)
        self.state.poly_guide.addDrawable(line)
        self.state.poly_guide.addDrawable(face)

    def reset(self):
        """Reset rectangle drawing state."""
        self.first_point = None
        self.second_point = None
        self.third_point = None
        self.fourth_point = None
        self.click_count = 0

    def on_draw_rect(self, ui_event):
        """
        Handle rectangle drawing logic.

        Args:
            ui_event: The Houdini UI event
        """
        device = ui_event.device()
        origin, direction = ui_event.ray()
        x, y, z = origin[0], origin[1], 0
        c = hou.Vector3(x, y, 0)

        # Get geometry from stash (accessed through state instance)
        stash_geo = self.state.node.geometry()
        nearest = stash_geo.nearestPoints(c, 2, max_radius=5)

        cursor_pos = hou.Vector3(x, y, z)
        snap_pos = None
        if nearest:
            snap_pos = nearest[0].position()

        # Handle different click states
        if self.click_count == 0:
            if snap_pos:
                cursor_pos = snap_pos
        elif self.click_count == 1:
            # Determine primary axis
            x_delta = abs(self.first_point[0] - cursor_pos[0])
            y_delta = abs(self.first_point[1] - cursor_pos[1])

            if y_delta > x_delta:
                x = self.first_point[0]
                self.first_axis = "Y"
            else:
                y = self.first_point[1]
                self.first_axis = "X"

            if snap_pos:
                if self.first_axis == "Y":
                    y = snap_pos[1]
                else:
                    x = snap_pos[0]

            cursor_pos = hou.Vector3(x, y, z)

        elif self.click_count == 2:
            if self.first_axis == "Y":
                y = self.second_point[1]
            else:
                x = self.second_point[0]

            if snap_pos:
                if self.first_axis == "Y":
                    x = snap_pos[0]
                else:
                    y = snap_pos[1]

            cursor_pos = hou.Vector3(x, y, z)

        reason = ui_event.reason()

        # Update drawable geometry
        poly_geo = hou.Geometry()
        cursor_point = poly_geo.createPoint()
        cursor_point.setPosition(cursor_pos)

        self.state.poly_guide.setGeometry(poly_geo)

        # Handle mouse clicks
        if device.isLeftButton():
            if reason == hou.uiEventReason.Picked:
                if self.first_point is None:
                    self.first_point = cursor_pos
                elif self.second_point is None:
                    self.second_point = cursor_pos
                elif self.third_point is None:
                    self.third_point = cursor_pos

                self.click_count += 1
                if self.click_count > 2:
                    self.create_rect_geo()
                    self.reset()

        # Draw rectangle preview
        if self.first_point:
            static_point_1 = poly_geo.createPoint()
            static_point_1.setPosition(self.first_point)

            if not self.second_point:
                poly = poly_geo.createPolygon()
                poly.addVertex(static_point_1)
                poly.addVertex(cursor_point)
            else:
                # Add second point
                static_point_2 = poly_geo.createPoint()
                static_point_2.setPosition(self.second_point)

                # Calculate fourth point
                if self.first_axis == "Y":
                    x4 = cursor_pos[0]
                    y4 = self.first_point[1]
                else:
                    x4 = self.first_point[0]
                    y4 = cursor_pos[1]

                self.fourth_point = hou.Vector3(x4, y4, 0)
                static_point_4 = poly_geo.createPoint()
                static_point_4.setPosition(self.fourth_point)

                # Create rectangle polygon
                poly = poly_geo.createPolygon()
                poly.addVertex(static_point_1)
                poly.addVertex(static_point_2)
                poly.addVertex(cursor_point)
                poly.addVertex(static_point_4)

        self.state.poly_guide.show(True)

    def create_rect_geo(self):
        reordered_points, points = platformer_geom.reorder_points(
            self.first_point,
            self.second_point,
            self.third_point,
            self.fourth_point,
            self.first_axis,
        )

        # Access node through state instance
        geo = self.state.stash.geometry().freeze()

        points = geo.createPoints(reordered_points)
        poly = geo.createPolygon()
        poly.addVertex(points[0])
        poly.addVertex(points[1])
        poly.addVertex(points[2])
        poly.addVertex(points[3])

        # Set geometry using state's node reference
        self.state.node.parm("stash").set(geo)
