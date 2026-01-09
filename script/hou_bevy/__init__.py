def reload_module():
    from importlib import reload

    print("reloaded: houdini_bevy")
    import hou_bevy.nodes.platformer.geometry
    import hou_bevy.nodes.platformer.state
    import hou_bevy.nodes.platformer.tools.rect.rect_draw
    import hou_bevy.nodes.platformer.tools.rect.rect_edit
    import hou_bevy.nodes.rop.export

    reload(hou_bevy.nodes.platformer.geometry)
    reload(hou_bevy.nodes.platformer.state)
    reload(hou_bevy.nodes.platformer.tools.rect.rect_draw)
    reload(hou_bevy.nodes.platformer.tools.rect.rect_edit)
    reload(hou_bevy.nodes.rop.export)
