"""
you can use it in three ways:

1. Simple enable/disable:

    page.accepts_drops = True  # Uses default handler that prints files

2. Custom handler using the property:

    def my_handler(files):
        print("Got files:", files)

    page.on_files_dropped = my_handler
    page.accepts_drops = True

3. Direct enable with custom handler:

    def my_handler(files):
        print("Got files:", files)

    page.enable_drag_and_drop(files_callback=my_handler)
"""

import pythoncom
import win32api
import win32con
import win32gui
import win32com.server.policy
from ctypes import windll, create_unicode_buffer
import threading
import time
import logging
import sys
import flet as ft

logger = logging.getLogger(__name__)

DROPEFFECT_NONE = 0
DROPEFFECT_COPY = 1
DROPEFFECT_MOVE = 2
DROPEFFECT_LINK = 4


class IDropTarget(win32com.server.policy.DesignatedWrapPolicy):
    _com_interfaces_ = [pythoncom.IID_IDropTarget]
    _public_methods_ = ["DragEnter", "DragOver", "DragLeave", "Drop"]

    def __init__(self, callbacks):
        self._wrap_(self)
        self.callbacks = callbacks
        logger.debug("IDropTarget initialized")

    def DragEnter(self, pDataObj, grfKeyState, point_tuple, pdwEffect):
        logger.debug("DragEnter called")
        try:
            format = (
                win32con.CF_HDROP,
                None,
                pythoncom.DVASPECT_CONTENT,
                -1,
                pythoncom.TYMED_HGLOBAL,
            )

            try:
                pDataObj.QueryGetData(format)
                if self.callbacks.get("on_drag_enter"):
                    self.callbacks["on_drag_enter"](point_tuple)
                return DROPEFFECT_COPY
            except:
                return DROPEFFECT_NONE
        except Exception as e:
            logger.exception("Error in DragEnter")
            return DROPEFFECT_NONE

    def DragOver(self, grfKeyState, point_tuple, pdwEffect):
        logger.debug("DragOver called")
        if self.callbacks.get("on_drag_over"):
            self.callbacks["on_drag_over"](point_tuple)
        return DROPEFFECT_COPY

    def DragLeave(self):
        logger.debug("DragLeave called")
        if self.callbacks.get("on_drag_leave"):
            self.callbacks["on_drag_leave"]()
        return DROPEFFECT_NONE

    def Drop(self, pDataObj, grfKeyState, point_tuple, pdwEffect):
        logger.debug("Drop called")
        try:
            format = (
                win32con.CF_HDROP,
                None,
                pythoncom.DVASPECT_CONTENT,
                -1,
                pythoncom.TYMED_HGLOBAL,
            )

            medium = pDataObj.GetData(format)

            if medium.data:
                file_count = windll.shell32.DragQueryFileW(medium.data, -1, None, 0)
                logger.debug(f"Number of files dropped: {file_count}")

                files = []
                for i in range(file_count):
                    length = windll.shell32.DragQueryFileW(medium.data, i, None, 0) + 1
                    buffer = create_unicode_buffer(length)
                    windll.shell32.DragQueryFileW(medium.data, i, buffer, length)
                    files.append(buffer.value)
                    logger.debug(f"File {i}: {buffer.value}")

                if self.callbacks.get("on_files_dropped"):
                    self.callbacks["on_files_dropped"](files)
                return DROPEFFECT_COPY

            return DROPEFFECT_NONE

        except Exception as e:
            logger.exception("Error in Drop")
            return DROPEFFECT_NONE


class DropTarget:
    def __init__(self, hwnd, callbacks):
        self.hwnd = hwnd
        self.callbacks = callbacks
        self.running = True

        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        try:
            pythoncom.OleInitialize()

            drop_target = IDropTarget(self.callbacks)
            drop_target_ptr = pythoncom.WrapObject(
                drop_target, pythoncom.IID_IDropTarget, pythoncom.IID_IDropTarget
            )

            pythoncom.RegisterDragDrop(self.hwnd, drop_target_ptr)

            while self.running:
                pythoncom.PumpMessages()

        except Exception as e:
            logger.exception("Error in drop target thread")
        finally:
            try:
                pythoncom.RevokeDragDrop(self.hwnd)
                pythoncom.CoUninitialize()
            except Exception as e:
                logger.exception("Error during cleanup")

    def stop(self):
        self.running = False
        win32gui.PostThreadMessage(self.thread.ident, win32con.WM_QUIT, 0, 0)
        self.thread.join()


def _default_on_files_dropped(self, files):
    print("Files dropped:", files)


def _default_on_drag_enter(self, point):
    print("Drag enter at point:", point)


def _default_on_drag_over(self, point):
    print("Drag over at point:", point)


def _default_on_drag_leave(self):
    print("Drag leave")


def _enable_drag_and_drop(
    self,
    files_callback=None,
    drag_enter_callback=None,
    drag_over_callback=None,
    drag_leave_callback=None,
):
    if sys.platform != "win32":
        logger.warning("Drag and drop is only supported on Windows")
        return

    # Set up default callbacks if not already defined
    if not hasattr(self, "on_files_dropped"):
        self.on_files_dropped = self._default_on_files_dropped
    if not hasattr(self, "on_drag_enter"):
        self.on_drag_enter = self._default_on_drag_enter
    if not hasattr(self, "on_drag_over"):
        self.on_drag_over = self._default_on_drag_over
    if not hasattr(self, "on_drag_leave"):
        self.on_drag_leave = self._default_on_drag_leave

    callbacks = {
        "on_files_dropped": files_callback or self.on_files_dropped,
        "on_drag_enter": drag_enter_callback or self.on_drag_enter,
        "on_drag_over": drag_over_callback or self.on_drag_over,
        "on_drag_leave": drag_leave_callback or self.on_drag_leave,
    }

    def on_window_handle_found(hwnd):
        if hasattr(self, "_drop_target"):
            self._drop_target.stop()
        self._drop_target = DropTarget(hwnd, callbacks)

    def find_window_by_title(title):
        def enum_windows_proc(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd) and title in win32gui.GetWindowText(hwnd):
                lParam.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(enum_windows_proc, hwnds)
        return hwnds[0] if hwnds else None

    def poll_for_window():
        hwnd = None
        while hwnd is None:
            hwnd = find_window_by_title(self.title)
            time.sleep(0.1)
        on_window_handle_found(hwnd)

    print(f"[DEBUG] Enabling enhanced drag & drop on flet window: {self.title}")
    threading.Thread(target=poll_for_window, daemon=True).start()
