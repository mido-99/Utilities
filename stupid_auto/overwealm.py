import pyautogui
import ctypes, time

def get_windows_scaling():
    """Gets the display scaling factor on Windows."""
    try:
        awareness = ctypes.windll.shcore.GetProcessDpiAwareness(0)
        if awareness == 0:  # DPI_UNAWARE
            return 1.0
        elif awareness == 1:  # DPI_SYSTEM_AWARE
            hwnd = ctypes.windll.user32.GetDesktopWindow()
            hDC = ctypes.windll.user32.GetDC(hwnd)
            logical_width = ctypes.windll.user32.GetDeviceCaps(hDC, 88)  # HORZRES
            physical_width = ctypes.windll.user32.GetDeviceCaps(hDC, 118) # DESKTOPHORZRES
            ctypes.windll.user32.ReleaseDC(hwnd, hDC)
            if logical_width and physical_width:
                return physical_width / logical_width
            else:
                return 1.0
        elif awareness == 2:  # DPI_PER_MONITOR_AWARE
            # This is more complex and requires handling each monitor individually.
            # A simpler approach might be to use GetScaleFactorForDevice.
            hDC = ctypes.windll.user32.GetDC(0)
            scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(hDC) / 100.0
            ctypes.windll.user32.ReleaseDC(0, hDC)
            return scale_factor
        elif awareness == 3: # DPI_PER_MONITOR_AWARE_V2
            hDC = ctypes.windll.user32.GetDC(0)
            scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(hDC) / 100.0
            ctypes.windll.user32.ReleaseDC(0, hDC)
            return scale_factor
        else:
            return 1.0
    except AttributeError:
        # Handle cases where the functions are not available (older Windows versions)
        return 1.0

if __name__ == "__main__":
    
    print('2 Seconds to start')
    time.sleep(3)
    # while True:
    for _ in range(7):
        pyautogui.moveTo(1540, 643)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.moveTo(1498, 728)
        pyautogui.click()
        pyautogui.moveTo(1195, 680)
        pyautogui.click()
        time.sleep(0.2)
        # break
