import importlib
import sys

import hou


def reload_hda_python(hda_node=None):
    """Reload Python from HDA"""

    # If no node specified, get selected node
    if hda_node is None:
        nodes = hou.selectedNodes()
        if not nodes:
            hou.ui.displayMessage("Select an HDA node first")
            return
        hda_node = nodes[0]

    # Get HDA definition
    definition = hda_node.type().definition()
    if definition is None:
        hou.ui.displayMessage("Selected node is not an HDA")
        return

    # Get module name (usually based on HDA name)
    hda_name = definition.nodeType().name()

    # Try to find and reload the module
    modules_to_reload = []

    # Common module naming patterns in Houdini
    possible_modules = [
        hda_name,  # Direct module name
        f"{hda_name}_python",  # Common suffix
        f"hda_{hda_name}",  # Another common pattern
    ]

    for mod_name in possible_modules:
        if mod_name in sys.modules:
            modules_to_reload.append(mod_name)

    # Also check for modules in the current HDA's namespace
    for mod in sys.modules.keys():
        if hda_name in mod:
            modules_to_reload.append(mod)

    # Reload found modules
    reloaded = []
    for mod_name in set(modules_to_reload):  # Remove duplicates
        try:
            importlib.reload(sys.modules[mod_name])
            reloaded.append(mod_name)
        except Exception as e:
            print(f"Failed to reload {mod_name}: {e}")

    # Force HDA to reload its Python
    try:
        # This forces HDA to re-evaluate its Python
        definition.updateFromNode(hda_node)
        print(f"✓ HDA Python reloaded: {', '.join(reloaded)}")

        # Optional: Force recook of the node
        hda_node.cook(force=True)

    except Exception as e:
        hou.ui.displayMessage(f"Error reloading HDA: {str(e)}")


# Run with selected node
reload_hda_python()
