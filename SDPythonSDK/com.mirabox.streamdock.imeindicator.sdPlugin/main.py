import ctypes
from ctypes import wintypes
from streamdock_sdk import Plugin

user32 = ctypes.WinDLL('user32', use_last_error=True)
imm32 = ctypes.WinDLL('imm32', use_last_error=True)

def get_ime_status():
    hwnd = user32.GetForegroundWindow()
    hIMC = imm32.ImmGetContext(hwnd)
    if not hIMC:
        return "A"
    open_status = imm32.ImmGetOpenStatus(hIMC)
    conv = ctypes.c_int()
    sent = ctypes.c_int()
    imm32.ImmGetConversionStatus(hIMC, ctypes.byref(conv), ctypes.byref(sent))
    imm32.ImmReleaseContext(hwnd, hIMC)
    if not open_status:
        return "A"
    if conv.value & 0x0001:  # IME_CMODE_NATIVE
        return "한"
    return "A"

class IMEIndicatorPlugin(Plugin):
    def on_tick(self):
        ime = get_ime_status()
        self.set_title(ime)

plugin = IMEIndicatorPlugin()
plugin.run()
