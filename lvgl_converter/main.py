#!/usr/bin/env python3
"""
Convert an image to a C array suitable for LVGL with 1-bit alpha channel.
This script replaces https://lvgl.github.io/lv_img_conv/ which is not working correctly
"""

from PIL import Image
import math

def img_to_lvgl_alpha_1bit(image_path, c_array_name="my_img"):
    # Open and convert image to grayscale (for thresholding)
    img = Image.open(image_path).convert("L")
    w, h = img.size

    # Apply threshold (you can tweak 128 for darker/lighter cutoff)
    threshold = 128
    binary_pixels = img.point(lambda p: 1 if p >= threshold else 0, "1")

    # Extract raw pixel data
    pixels = binary_pixels.getdata()

    # Pack into bytes (8 pixels per byte, MSB first)
    byte_data = []
    for y in range(h):
        for x_byte in range(math.ceil(w / 8)):
            byte = 0
            for bit in range(8):
                x = x_byte * 8 + bit
                if x < w:
                    pixel = pixels[y * w + x]
                    if pixel:  # opaque
                        byte |= (1 << (7 - bit))  # MSB first
            byte_data.append(byte)

    # Build C array string
    hex_bytes = ", ".join(f"0x{b:02X}" for b in byte_data)

    # LVGL expects this header before the data:
    # https://docs.lvgl.io/master/overview/images.html#c-array-images
    c_code = f"""
#include "lvgl.h"

LV_IMG_DECLARE({c_array_name});

const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_LARGE_CONST uint8_t {c_array_name}_map[] = {{
    {hex_bytes}
}};

const lv_img_dsc_t {c_array_name} = {{
  .header.always_zero = 0,
  .header.w = {w},
  .header.h = {h},
  .data_size = {len(byte_data)},
  .header.cf = LV_IMG_CF_ALPHA_1BIT,
  .data = {c_array_name}_map
}};
"""

    return c_code


# Example usage
if __name__ == "__main__":
    c_code = img_to_lvgl_alpha_1bit("../assets/bongocat_.gif", "bongocat")
    with open("example_img.c", "w") as f:
        f.write(c_code)
    print("C file generated: example_img.c")
