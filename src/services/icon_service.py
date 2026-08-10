import win32con
import win32gui
import win32ui
from PIL import Image, ImageChops, ImageDraw, ImageWin

import src.app.paths as rice_paths


def get_hicon_from_hwnd(hwnd: int):
    hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_BIG, 0)

    if not hicon:
        hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICON)

    if not hicon:
        hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)

    if not hicon:
        hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICONSM)

    if not hicon:
        print("No Icon Found")
        return None

    return hicon


def hicon_to_image(hicon: int, size: int = 256) -> Image.Image:
    # Get the screen device context.
    hdc = win32gui.GetDC(0)

    # Wrap the raw Windows HDC into a pywin32 DC object.
    dc = win32ui.CreateDCFromHandle(hdc)

    # Create an in-memory DC where we can draw the icon.
    mem_dc = dc.CreateCompatibleDC()

    # Create a bitmap with the size we want.
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(dc, size, size)

    # Put the bitmap inside the memory DC.
    old_bitmap = mem_dc.SelectObject(bitmap)

    # Draw the HICON into the bitmap.
    win32gui.DrawIconEx(
        mem_dc.GetSafeHdc(),
        0,
        0,
        hicon,
        size,
        size,
        0,
        0,
        win32con.DI_NORMAL,
    )

    # Read bitmap info and raw bytes.
    bmp_info = bitmap.GetInfo()
    bmp_bytes = bitmap.GetBitmapBits(True)

    # Convert Windows BGRA bytes into a Pillow RGBA image.
    image = Image.frombuffer(
        "RGBA",
        (bmp_info["bmWidth"], bmp_info["bmHeight"]),
        bmp_bytes,
        "raw",
        "BGRA",
        0,
        1,
    ).copy()

    # Cleanup Windows resources.
    mem_dc.SelectObject(old_bitmap)
    win32gui.DeleteObject(bitmap.GetHandle())
    mem_dc.DeleteDC()
    dc.DeleteDC()
    win32gui.ReleaseDC(0, hdc)

    return image


def create_png_from_hwnd(hwnd: int) -> str | None:
    hicon = get_hicon_from_hwnd(hwnd)

    if not hicon:
        return None

    # Convert HICON to Pillow image.
    image = hicon_to_image(hicon, 256)

    # rounding corner
    scale = 4
    width, height = image.size
    mask_size = width * scale, height * scale
    scaled_radius = 6 * scale

    mask = Image.new("L", mask_size, 0)
    mask_draw = ImageDraw.Draw(mask)

    mask_draw.rounded_rectangle(
        (0, 0, mask_size[0] - 1, mask_size[1] - 1),
        radius=scaled_radius,
        fill=255,
    )

    mask = mask.resize(image.size, Image.Resampling.LANCZOS)

    alpha = image.getchannel("A")
    alpha = ImageChops.darker(alpha, mask)

    image.putalpha(alpha)

    icon_path = rice_paths.window_cache_icon_dir / f"hwnd_{hwnd}.png"
    # print(f"icon_path: {icon_path}")
    image.save(icon_path)

    return str(icon_path)


def create_icon_cache(hwnd: int) -> str | None:
    icon_path: str | None = create_png_from_hwnd(hwnd)

    if icon_path:
        return icon_path
    else:
        return None


def get_icon_path(hwnd: int) -> str:

    file_name = f"hwnd_{hwnd}.png"

    icon_abs_path = rice_paths.window_cache_icon_dir / file_name

    if icon_abs_path.exists():
        return str(icon_abs_path)
    else:
        new_icon_path = create_icon_cache(hwnd)

        if new_icon_path:
            return new_icon_path
        else:
            default_icon_path = rice_paths.assets_dir / "default_app_icon.png"
            return str(default_icon_path)
