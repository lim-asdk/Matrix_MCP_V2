"""
Matrix MCP v2.0 | Native Desktop Launcher

FUNCTION: Desktop App Wrapper (Offline-Ready Native Window)
TARGET: Windows Desktop (via System WebView2 / EdgeChromium)
"""

import os
import sys
import logging
import threading
from pathlib import Path

# IMPORTANT: Ensure pywebview is installed. 
# It uses the system's built-in WebView2 component (lightweight & native).
import webview 

# --- DYNAMIC IMPORTS & RUNTIME SETUP ---
def setup_paths():
    """Consistent path resolution for the whole project."""
    current_path = Path(__file__).resolve()
    found_root = None
    for i in range(5):
        parent = current_path.parents[i]
        if (parent / "lim_arsenal").exists():
            found_root = parent
            break
    if not found_root:
        found_root = Path(__file__).resolve().parent

    project_root = found_root
    package_dir = project_root / "lim_arsenal"
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        
    engine_dir = package_dir / "engine"          
    if str(engine_dir) not in sys.path:
        sys.path.insert(0, str(engine_dir))
    return project_root

ROOT_PATH = setup_paths()
os.chdir(ROOT_PATH)

# Use dynamic imports for engine components to avoid boot delay
from L3_Orchestration.pro_bridge_api import ProBridgeAPI
from L1_Infrastructure.path_manager import PathManager
from lim_arsenal import get_available_packs

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("MatrixMCP.Desktop")

def start_desktop_app():
    """Launch Sequence for Native Desktop Mode (Offline Ready)"""
    logger.info("Initializing Native Desktop Environment...")

    # 1. Setup Logic & Pack Discovery
    packs = get_available_packs()
    active_pack = "stock_pro" if "stock_pro" in packs else (packs[0] if packs else None)
    
    if active_pack:
        PathManager.set_active_pack(active_pack)
        display_mode = f"Pack: {active_pack}"
    else:
        PathManager.active_pack = None 
        display_mode = "Emergency Assistant"

    # 2. Bridge API Setup (Python <-> JS Connection)
    api = ProBridgeAPI()

    # 3. UI Path Procurement (Local File Loading)
    ui_path = PathManager.get_ui_path("index_pro.html")
    if not ui_path.exists():
        start_url = "data:text/html,<h1>Error: UI File Missing</h1>"
    else:
        # Load as a file URI for clean offline local execution
        start_url = ui_path.absolute().as_uri()

    # 4. Create Native Window
    window = webview.create_window(
        title=f"Matrix MCP v2.0 [{display_mode}]",
        url=start_url,
        js_api=api,
        width=1280,
        height=850,
        resizable=True,
        background_color='#0f172a'
    )
    
    api.set_window(window)

    # 5. Start WebView (Forcing edgechromium/WebView2 for minimal footprint on Windows)
    logger.info(f"Launching Native Window via WebView2 (Offline: {start_url})")
    # debug=False turns off the Inspect DevTools for end-users
    webview.start(gui='edgechromium', debug=False, http_server=True)

if __name__ == "__main__":
    start_desktop_app()
