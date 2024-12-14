import os
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Optional
from PIL import Image

import flet as ft
from flet.version import version as flet_version
from flet.utils import is_macos, is_windows, is_linux

# Optional platform-specific imports
try:
    import ctypes
except ImportError:
    ctypes = None

try:
    from AppKit import NSImage, NSWorkspace, NSURL
except ImportError:
    NSImage = NSWorkspace = NSURL = None

try:
    from gi import require_version
    require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError:
    Gtk = None

class AppIconChanger:
    SUPPORTED_FORMATS = {"ico", "png", "jpeg", "bmp", "icns"}
    
    def __init__(self, icon_path: str, app_name: Optional[str] = None, app_path: Optional[str] = None):
        self.image_path = os.path.abspath(icon_path)
        self.app_name = app_name
        self.app_path = app_path or self._get_default_app_path()
        self.icon_path = self._prepare_icon()
        
    def _get_default_app_path(self) -> Path:
        app_name = f"{self.app_name}.app" if self.app_name else "Flet.app"
        return Path.home().joinpath(".flet", "bin", f"flet-{flet_version}", app_name)
    
    def _prepare_icon(self) -> str:
        image_type = self._get_image_type()
        if image_type not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported image type: {image_type}")
            
        if is_windows() and image_type != "ico":
            return self._convert_to_ico()
        elif is_macos() and image_type != "icns":
            return self._convert_to_icns()
        return self.image_path
    
    def _get_image_type(self) -> str:
        with Image.open(self.image_path) as img:
            return img.format.lower()
    
    def _convert_to_ico(self) -> str:
        ico_path = f"{os.path.splitext(self.image_path)[0]}.ico"
        with Image.open(self.image_path) as img:
            img.save(ico_path, format="ICO", sizes=[(32, 32), (64, 64), (128, 128), (256, 256)])
        return ico_path
    
    def _convert_to_icns(self) -> str:
        icns_path = "/tmp/new_icon.icns"
        iconset_dir = "/tmp/icon.iconset"
        os.makedirs(iconset_dir, exist_ok=True)
        
        try:
            for size in [16, 32, 128, 256, 512]:
                with Image.open(self.image_path) as img:
                    img.resize((size, size)).save(f"{iconset_dir}/icon_{size}x{size}.png")
                    img.resize((size * 2, size * 2)).save(f"{iconset_dir}/icon_{size}x{size}@2x.png")
            
            subprocess.run(["iconutil", "-c", "icns", iconset_dir, "-o", icns_path])
            return icns_path
        finally:
            shutil.rmtree(iconset_dir)
    
    def change_icon(self):
        if is_windows():
            if not ctypes:
                raise ImportError("ctypes required for Windows icon change")
            threading.Thread(target=self._change_windows_icon).start()
        elif is_macos():
            if not all([NSImage, NSWorkspace, NSURL]):
                raise ImportError("AppKit required for macOS icon change")
            self._change_macos_icon()
        elif is_linux():
            if not Gtk:
                raise ImportError("Gtk required for Linux icon change")
            self._change_linux_icon()
        else:
            raise OSError("Unsupported operating system")
    
    def _change_windows_icon(self):
        import pygetwindow as gw
        
        def update_icon():
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            hicon = user32.LoadImageW(0, self.icon_path, 1, 0, 0, 0x00000010 | 0x00000002)
            if not hicon:
                raise OSError(f"Failed to load icon: {ctypes.WinError(ctypes.get_last_error())}")
                
            hwnd = user32.GetForegroundWindow()
            if not hwnd:
                raise OSError(f"Failed to get window: {ctypes.WinError(ctypes.get_last_error())}")
            
            try:
                user32.SendMessageW(hwnd, 0x0080, 0, hicon)  # ICON_SMALL
                user32.SendMessageW(hwnd, 0x0080, 1, hicon)  # ICON_BIG
            finally:
                kernel32.CloseHandle(hicon)
        
        while not gw.getWindowsWithTitle(self.app_name):
            continue
        update_icon()
    
    def _change_macos_icon(self):
        if not all(map(os.path.exists, [self.app_path, self.icon_path])):
            raise FileNotFoundError("App or icon path not found")
        
        icon_cr_path = os.path.join(self.app_path, "Icon\r")
        if os.path.exists(icon_cr_path):
            os.remove(icon_cr_path)
        
        new_icon_path = os.path.join(self.app_path, "Contents", "Resources", "new_icon.icns")
        shutil.copy(self.icon_path, new_icon_path)
        
        self._update_plist()
        self._create_icon_resource(new_icon_path)
    
    def _update_plist(self):
        plist_path = os.path.join(self.app_path, "Contents", "Info.plist")
        with open(plist_path, "r") as f:
            content = f.read()
        
        if "new_icon.icns" not in content:
            content = content.replace(
                "<key>CFBundleIconFile</key><string>AppIcon</string>",
                "<key>CFBundleIconFile</key><string>new_icon</string>"
            )
            with open(plist_path, "w") as f:
                f.write(content)
    
    def _create_icon_resource(self, icns_path: str):
        icon_cr_path = os.path.join(self.app_path, "Icon\r")
        open(icon_cr_path, "a").close()
        
        app_url = NSURL.fileURLWithPath_(str(self.app_path))
        icon_url = NSURL.fileURLWithPath_(str(icns_path))
        icon_image = NSImage.alloc().initWithContentsOfURL_(icon_url)
        NSWorkspace.sharedWorkspace().setIcon_forFile_options_(icon_image, app_url.path(), 0)
    
    def _change_linux_icon(self):
        icon = Gtk.Image.new_from_file(self.icon_path)
        Gtk.Window.set_default_icon_list(icon.get_pixbuf())


def change_app_icon(icon_path: str, app_name: str = None, app_path: str = None):
    changer = AppIconChanger(icon_path, app_name, app_path)
    changer.change_icon()