with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

old_enhance = """fun enhanceBitmapForOcr(src: Bitmap): Bitmap {
        val w = src.width
        val h = src.height
        val scale = if (w < 150 || h < 150) 2f else 1.5f
        
        val sw = (w * scale).toInt()
        val sh = (h * scale).toInt()
        val scaled = Bitmap.createScaledBitmap(src, sw, sh, true)
        
        val pixels = IntArray(sw * sh)
        scaled.getPixels(pixels, 0, sw, 0, 0, sw, sh)
        
        for (i in pixels.indices) {
            val color = pixels[i]
            val r = (color shr 16) and 0xFF
            val g = (color shr 8) and 0xFF
            val b = color and 0xFF
            
            val lum = (r * 77 + g * 150 + b * 29) shr 8
            var newLum = ((lum - 128) * 3) + 128
            if (newLum > 255) newLum = 255
            else if (newLum < 0) newLum = 0
            
            pixels[i] = (0xFF shl 24) or (newLum shl 16) or (newLum shl 8) or newLum
        }
        
        scaled.setPixels(pixels, 0, sw, 0, 0, sw, sh)
        return scaled
    }"""

new_enhance = """fun enhanceBitmapForOcr(src: Bitmap): Bitmap {
        val w = src.width
        val h = src.height
        val scale = if (w < 150 || h < 150) 2f else 1.5f
        
        val sw = (w * scale).toInt()
        val sh = (h * scale).toInt()
        return Bitmap.createScaledBitmap(src, sw, sh, true)
    }"""

if old_enhance in content:
    content = content.replace(old_enhance, new_enhance)
    with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
        f.write(content)
    print("enhanceBitmapForOcr patched!")
else:
    print("Could not find enhanceBitmapForOcr")
