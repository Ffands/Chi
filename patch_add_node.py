import sys
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_params = """        val params = WindowManager.LayoutParams(
            dpToPx(60), dpToPx(60),
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            flags,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = startX ?: (windowManager.defaultDisplay.width / 2)
            y = startY ?: (windowManager.defaultDisplay.height / 2)
        }
        node.x = params.x + dpToPx(30)
        node.y = params.y + dpToPx(30)"""

good_params = """        val params = WindowManager.LayoutParams(
            dpToPx(60), dpToPx(60),
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            flags,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.TOP or Gravity.START
            x = if (startX != null) startX - dpToPx(30) else (windowManager.defaultDisplay.width / 2 - dpToPx(30))
            y = if (startY != null) startY - dpToPx(30) else (windowManager.defaultDisplay.height / 2 - dpToPx(30))
        }
        node.x = params.x + dpToPx(30)
        node.y = params.y + dpToPx(30)"""

content = content.replace(bad_params, good_params)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Patched addNode offset")
