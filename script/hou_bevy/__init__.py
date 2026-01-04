def reload_module():
    from importlib import reload

    print("doing reload")
    import hou_bevy.nodes.platformer.geometry
    import hou_bevy.nodes.platformer.state
    import hou_bevy.nodes.platformer.tools.rect.rect_draw
    import hou_bevy.nodes.platformer.tools.rect.rect_edit

    reload(hou_bevy.nodes.platformer.geometry)
    reload(hou_bevy.nodes.platformer.state)
    reload(hou_bevy.nodes.platformer.tools.rect.rect_draw)
    reload(hou_bevy.nodes.platformer.tools.rect.rect_edit)
