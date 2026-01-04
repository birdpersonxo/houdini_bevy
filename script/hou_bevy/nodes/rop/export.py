import json
from importlib import reload
from pathlib import Path

import hou
import hou_bevy.component

reload(hou_bevy.component)

from hou_bevy.component import HouData, HouRect, Vec2, Vec3


def rop_output(kwargs):
    """
    Rop output node
    """
    node = kwargs["node"]
    geo = node.geometry()
    output_path = node.parm("sopoutput").eval()

    hou_data = HouData()
    if geo:
        for prim in geo.prims():
            # Get the vector value (e.g., [x, y, z])
            layer_name = prim.attribValue("name")
            layer_type = prim.attribValue("type")

            data = None

            if layer_type == "HouRect":
                center = prim.attribValue("center")
                translation = Vec3.new(center[0], center[1], center[2])

                size = list(prim.attribValue("size"))[:2]
                size = Vec2.new(size[0], size[1])

                uv = prim.attribValue("uv")
                uv_list = Vec2.to_list(uv)

                data = HouRect.new(size, translation, uv_list)

            hou_data.create_layer(layer_name)  # creates layer only if not exists
            hou_data.append_data(layer_name, data)

    if output_path:
        hou_data.export_as_json(output_path)
