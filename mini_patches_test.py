# -*- coding: utf-8 -*-
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

fig, ax = plt.subplots(figsize=(4, 3))
ax.add_patch(mpl.patches.Rectangle((0, 0), 30, 100, facecolor="#4E79A7", edgecolor="white", lw=2))
ax.add_patch(mpl.patches.Rectangle((30, 0), 30, 100, facecolor="#EE7733", edgecolor="white", lw=2))
ax.add_patch(mpl.patches.Rectangle((60, 0), 40, 100, facecolor="#59A14F", edgecolor="white", lw=2))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_axis_off()
fig.set_dpi(200)
fig.canvas.draw()
im = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba())
im.convert("RGB").save("mini_patches.png")
print("saved", fig.canvas.get_width_height(), "patches:", len(ax.patches))
