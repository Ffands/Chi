with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# First find the definition of scrollContent and topScroll
scroll_block = """        val scrollContent = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
        }
        val topScroll = android.widget.HorizontalScrollView(service).apply {
            isHorizontalScrollBarEnabled = false
            layoutParams = LinearLayout.LayoutParams(dpToPx(180), LinearLayout.LayoutParams.WRAP_CONTENT)
            addView(scrollContent)
        }
"""

content = content.replace(scroll_block, "")

# Now insert it before minMaxBtn
minmax_start = """        val minMaxBtn = Button(service).apply {"""
content = content.replace(minmax_start, scroll_block + "\n" + minmax_start)

# Now add topScroll.visibility = vis inside the listener
exitbtn_vis = "exitBtn.visibility = vis"
content = content.replace(exitbtn_vis, "exitBtn.visibility = vis\n                topScroll.visibility = vis")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Fixed!")
