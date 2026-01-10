import os
import subprocess
import sys
import threading
from pathlib import Path

import hou


def run_usd_parser(input_file, output_file=None, remove_input=bool):
    """
    Run the usdrs.exe parser asynchronously
    """
    # Get the path to the executable
    # Assuming usdrs.exe is in the same directory as the HDA
    exe_path = get_exe_path()

    # Verify executable exists
    if not os.path.exists(exe_path):
        hou.ui.displayMessage(f"Error: usdrs.exe not found at {exe_path}")
        return False

    # Build command arguments
    cmd = [exe_path, "export", input_file]
    if output_file:
        cmd.extend(["-o", output_file])

    if remove_input:
        cmd.extend(["--remove-input"])

    # Run asynchronously
    def run_process():
        try:
            # Use Popen to run without blocking
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32"
                else 0,
            )

            # Read output in background
            stdout, stderr = process.communicate()

            # Check result
            if process.returncode == 0:
                hou.ui.setStatusMessage(
                    "USD parsing completed successfully",
                    severity=hou.severityType.Message,
                )
                if stdout:
                    print(f"Output: {stdout}")
            else:
                hou.ui.displayMessage(
                    f"Error parsing USD: {stderr}", severity=hou.severityType.Error
                )

        except Exception as e:
            hou.ui.displayMessage(
                f"Failed to run usdrs.exe: {str(e)}", severity=hou.severityType.Error
            )

    # Start the thread
    thread = threading.Thread(target=run_process)
    thread.daemon = True  # Thread will exit when main program exits
    thread.start()

    # Update status
    hou.ui.setStatusMessage(
        "USD parsing started in background...",
        severity=hou.severityType.ImportantMessage,
    )

    return True


def get_exe_path():
    """Get path to usdrs.exe relative to hou_bevy package"""

    try:
        # Import hou_bevy to get its location
        import hou_bevy

        # Get the directory where hou_bevy package is located
        package_dir = os.path.dirname(os.path.abspath(hou_bevy.__file__))
        script_dir = os.path.dirname(package_dir)  # Remove 'hou_bevy'
        houdini_bevy_dir = os.path.dirname(script_dir)  # Remove 'script'

        # Build path to bin directory
        bin_dir = os.path.join(houdini_bevy_dir, "bin")
        exe_path = os.path.join(bin_dir, "usdrs.exe")

        if os.path.exists(exe_path):
            print(f"Found usdrs.exe at: {exe_path}")
            return exe_path
        else:
            print(f"usdrs.exe not found at: {exe_path}")

    except ImportError:
        print("hou_bevy package not found in Python path")

    # Fallback: Search for hou_bevy in Python paths
    for path in sys.path:
        if "hou_bevy" in path:
            # Check if this is the package directory
            potential_exe = os.path.join(path, "bin", "usdrs.exe")
            if os.path.exists(potential_exe):
                print(f"Found via sys.path: {potential_exe}")
                return potential_exe

    raise FileNotFoundError(
        "usdrs.exe not found in hou_bevy/bin directory. "
        "Make sure hou_bevy package is properly installed."
    )
