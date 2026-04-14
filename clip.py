from PIL import Image

def extract_gif_region(
    path: str,
    region: tuple[int, int, int, int],
    bg_color: tuple[int, int, int],
    frames: list[int] | None = None,
    tolerance: int = 30,
) -> list[Image.Image]:
    """
    Extrait une région d'un GIF en supprimant le fond.

    Args:
        path: chemin vers le GIF
        region: (x, y, w, h) région à extraire
        bg_color: (r, g, b) couleur de fond à supprimer
        frames: indices des frames à extraire, None = toutes
        tolerance: tolérance de couleur pour la suppression du fond

    Returns:
        liste d'images RGBA avec le fond supprimé
    """
    gif = Image.open(path)
    x, y, w, h = region
    box = (x, y, x + w, y + h)
    tr, tg, tb = bg_color
    results = []

    frame_index = 0
    while True:
        if frames is None or frame_index in frames:
            frame = gif.convert("RGBA").crop(box)
            data = frame.getdata()
            new_data = [
                (r, g, b, 0) if abs(r - tr) < tolerance and abs(g - tg) < tolerance and abs(b - tb) < tolerance else (r, g, b, a)
                for r, g, b, a in data
            ]
            frame.putdata(new_data)
            results.append(frame)

        frame_index += 1
        try:
            gif.seek(frame_index)
        except EOFError:
            break

    return results