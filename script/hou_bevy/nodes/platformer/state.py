import hou
import viewerstate.utils as su
from hou import Vector3
from hou_bevy.nodes.platformer.geometry import reorder_points
from hou_bevy.nodes.platformer.tools.rect.rect_draw import DrawRect
from hou_bevy.nodes.platformer.tools.rect.rect_edit import EditRect


class State(object):
    MSG = "Move the mouse over the geometry."

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.node = None
        self.stash = None
        self.geometry = None
        self.pressed = False

        self.active_tool: str | None = None

        # tools
        self.tool_draw_rect = None
        self.tool_edit_rect = None

        self.poly_guide = hou.GeometryDrawableGroup("poly_guide")

    def onEnter(self, kwargs):
        """Assign the geometry to drawabled"""
        self.node = kwargs["node"]
        self.geometry = self.node.geometry()
        if not self.node:
            raise

        self.active_tool = "DRAW"
        self.scene_viewer.setPromptMessage(State.MSG)
        self.stash = self.node.node("stash")
        self.mode = self.node.parm("mode").eval()

        self.tool_draw_rect = DrawRect(self)
        self.tool_edit_rect = EditRect(self)

    def start(self):
        if not self.pressed:
            self.scene_viewer.beginStateUndo("Add point")
            self.index = self.pointCount()

        self.pressed = True

    def finish(self):
        if self.pressed:
            self.scene_viewer.endStateUndo()
        self.pressed = False

    def onInterrupt(self, kwargs):
        self.finish()
        if self.mode == 1:
            if self.tool_edit_rect:
                self.tool_edit_rect.onInterrupt()

    def onResume(self, kwargs):
        self.scene_viewer.setPromptMessage(State.MSG)
        if self.mode == 1:
            if self.tool_edit_rect:
                self.tool_edit_rect.onResume(kwargs)

    def onMouseEvent(self, kwargs):
        ui_event = kwargs["ui_event"]
        self.mode = self.node.parm("mode").eval()
        if self.mode == 0 and self.tool_draw_rect:
            self.tool_draw_rect.on_draw_rect(ui_event)
        elif self.mode == 1 and self.tool_edit_rect:
            self.tool_edit_rect.onEditRect(ui_event)
            self.poly_guide.show(False)
        else:
            self.poly_guide.show(False)

    def onDraw(self, kwargs):
        """This callback is used for rendering the drawables"""
        handle = kwargs["draw_handle"]
        self.poly_guide.draw(handle)
        if self.tool_edit_rect:
            self.tool_edit_rect.selected_guide.draw(handle)
            self.tool_edit_rect.selected_edge.draw(handle)
