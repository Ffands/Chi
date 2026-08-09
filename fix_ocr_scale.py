import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

# First block (testTextRecognition)
# We find this:
to_remove_1 = """            val scale = node.checkResolutionScale.coerceIn(0.1f, 1.0f)
            var isRegionSelected = !(left == 0 && top == 0 && right == 0 && bottom == 0)
            var cropped = if (isRegionSelected) Bitmap.createBitmap(bitmap, left, top, w, h) else bitmap
            var isScaledDown = false
            
            if (scale < 1.0f) {
                val sw = (cropped.width * scale).toInt().coerceAtLeast(1)
                val sh = (cropped.height * scale).toInt().coerceAtLeast(1)
                val scaled = Bitmap.createScaledBitmap(cropped, sw, sh, true)
                if (isRegionSelected) cropped.recycle()
                cropped = scaled
                isRegionSelected = true // Ensure we recycle the scaled bitmap later
                isScaledDown = true
            }"""

replacement_1 = """            var isRegionSelected = !(left == 0 && top == 0 && right == 0 && bottom == 0)
            var cropped = if (isRegionSelected) Bitmap.createBitmap(bitmap, left, top, w, h) else bitmap"""

content = content.replace(to_remove_1, replacement_1)

# Second block (checkTextCondition)
content = content.replace(to_remove_1, replacement_1) # Because it's identical

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
