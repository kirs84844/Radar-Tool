import ctypes
import time

# [核心防御] 强制系统 DPI 感知，确保测出的坐标是绝对物理像素，无视 Windows 缩放
try:
    ctypes.windll.user32.SetProcessDPIAware()
except AttributeError:
    pass

def start_radar():
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    
    print("==================================================")
    print(" 物理坐标与RGB颜色探测雷达 (DPI强制接管版) ")
    print(" 请将 HIS 系统调整至你平时工作的标准最大化状态 ")
    print(" 将鼠标悬停在目标位置，记录下方刷新的数值 ")
    print(" 按 Ctrl+C 终止程序 ")
    print("==================================================\n")
    
    while True:
        # 1. 获取物理坐标
        user32.GetCursorPos(ctypes.byref(pt))
        # 2. 获取屏幕设备上下文
        hdc = user32.GetDC(0)
        # 3. 提取颜色
        pixel = gdi32.GetPixel(hdc, pt.x, pt.y)
        user32.ReleaseDC(0, hdc)
        
        # 4. 转换为 RGB
        r = pixel & 0x0000ff
        g = (pixel & 0x00ff00) >> 8
        b = (pixel & 0xff0000) >> 16
        
        print(f"物理坐标 -> X: {pt.x:>4}, Y: {pt.y:>4}  |  RGB: ({r:>3}, {g:>3}, {b:>3})")
        time.sleep(0.5)

if __name__ == "__main__":
    start_radar()
