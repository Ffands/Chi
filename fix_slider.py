import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """        val resolutionScaleLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(0, 5, 0, 5) }
        resolutionScaleLayout.addView(TextView(service).apply { text = "Качество (0.1 - 1.0):"; setTextColor(Color.WHITE); layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 1f) })
        val resolutionScaleEdit = EditText(service).apply {
            inputType = InputType.TYPE_CLASS_NUMBER or InputType.TYPE_NUMBER_FLAG_DECIMAL
            setText(node.checkResolutionScale.toString())
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(dpToPx(130), WindowManager.LayoutParams.WRAP_CONTENT)
        }
        resolutionScaleLayout.addView(resolutionScaleEdit)"""

replacement = """        val resolutionScaleLayout = LinearLayout(service).apply { orientation = LinearLayout.HORIZONTAL; gravity = Gravity.CENTER_VERTICAL; setPadding(0, 5, 0, 5) }
        val resolutionScaleText = TextView(service).apply { 
            text = "Качество (${(node.checkResolutionScale * 100).toInt()}%):"
            setTextColor(Color.WHITE)
            layoutParams = LinearLayout.LayoutParams(dpToPx(130), WindowManager.LayoutParams.WRAP_CONTENT) 
        }
        val resolutionScaleBar = android.widget.SeekBar(service).apply {
            max = 90
            progress = ((node.checkResolutionScale - 0.1f) * 100).toInt()
            layoutParams = LinearLayout.LayoutParams(0, WindowManager.LayoutParams.WRAP_CONTENT, 1f)
        }
        resolutionScaleLayout.addView(resolutionScaleText)
        resolutionScaleLayout.addView(resolutionScaleBar)"""

content = content.replace(target, replacement)

# Add listener to update text and preview
img_target = """        val imgPreview = android.widget.ImageView(service).apply {"""
img_replace = """        val imgPreview = android.widget.ImageView(service).apply {"""

# We need to insert the listener after imgPreview is declared so it can update it
content = content.replace(img_replace, img_replace) # wait, I will do this in the next step

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
