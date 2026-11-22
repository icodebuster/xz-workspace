"""Swap the banner's dark green sky for Axis navy, blending anti-aliased edges."""
import sys
from collections import Counter
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
NEW = (0x0B, 0x1A, 0x28)  # Axis nav navy
T = 140.0                 # colour distance over which edge pixels stop shifting

im = Image.open(src).convert("RGB")
px = list(im.getdata())
old = Counter(px).most_common(1)[0][0]
print("background was", "#%02X%02X%02X" % old)

delta = [n - o for n, o in zip(NEW, old)]
out = []
for p in px:
    d = sum((a - b) ** 2 for a, b in zip(p, old)) ** 0.5
    w = max(0.0, 1.0 - d / T)
    out.append(tuple(max(0, min(255, round(c + w * dc))) for c, dc in zip(p, delta)))

res = Image.new("RGB", im.size)
res.putdata(out)
res = res.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
res.save(dst, optimize=True)
print("saved", dst)
