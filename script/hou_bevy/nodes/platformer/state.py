from winreg import KEY_READ

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
        self.text = hou.TextDrawable(self.scene_viewer, "text")

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

        self.text.show(True)

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
        if self.mode == 0 and self.tool_draw_rect and self.tool_edit_rect:
            self.tool_draw_rect.on_draw_rect(ui_event)
            self.tool_edit_rect.onRemoveSelectedPrim()
        elif self.mode == 1 and self.tool_edit_rect:
            self.tool_edit_rect.onEditRect(ui_event)
            self.poly_guide.show(False)
        else:
            self.poly_guide.show(False)

    def onDraw(self, kwargs):
        """This callback is used for rendering the drawables"""
        handle = kwargs["draw_handle"]
        self.poly_guide.draw(handle)
        # params = {
        #     "text": "Hello",
        #     "multi_line": True,
        #     "translate": (0, 0, 0.0),
        #     "highlight_mode": hou.drawableHighlightMode.MatteOverGlow,
        #     "glow_width": 1,
        #     "color1": hou.Color(1.0, 0.0, 0.0),
        #     "color2": (0.0, 0.0, 0.0, 1.0),
        # }
        # self.text.draw(handle, params)

        if self.tool_edit_rect:
            self.tool_edit_rect.selected_guide.draw(handle)
            self.tool_edit_rect.selected_edge.draw(handle)

    # def onKeyTransitEvent(self, kwargs):
    #     ui_event = kwargs["ui_event"]
    #     device = ui_event.device()
    #     key = device.keyString()

    #     if device.modifierString():
    #         print(str(key))

    def onKeyEvent(self, kwargs):
        ui_event = kwargs["ui_event"]
        key_pressed = ui_event.device().keyString()

        # Ctrl+d > Delete key value
        if key_pressed == "Ctrl+d":
            if self.mode == 1 and self.tool_edit_rect:
                self.tool_edit_rect.onDeleteRect()
