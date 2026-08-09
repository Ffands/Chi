import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Fix import
if "import android.widget.HorizontalScrollView" not in content:
    content = content.replace("import android.widget.ScrollView", "import android.widget.ScrollView\nimport android.widget.HorizontalScrollView")

# Move minMaxBtn
target_btn = """        val minMaxBtn = Button(service).apply {
            text = "➖"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            
            var isMinimized = false
            setOnClickListener {
                isMinimized = !isMinimized
                text = if (isMinimized) "➕" else "➖"
                val vis = if (isMinimized) View.GONE else View.VISIBLE
                playBtn.visibility = vis
                recordBtn.visibility = if (isMinimized || appMode != AppMode.RECORD) View.GONE else View.VISIBLE
                toggleVisBtn.visibility = if (isMinimized || !showEyeBtn) View.GONE else View.VISIBLE
                linesToggleBtn.visibility = if (isMinimized || !showLinesBtn) View.GONE else View.VISIBLE
                hotbarToggleBtn.visibility = if (isMinimized || !showHotbarBtn) View.GONE else View.VISIBLE
                gearBtn.visibility = if (isMinimized || !showSettingsBtn) View.GONE else View.VISIBLE
                exitBtn.visibility = vis
                if (isMinimized) hotbarRow.visibility = View.GONE
            }
        }"""

if target_btn in content:
    # Remove from its current location
    content = content.replace(target_btn, "")
    
    # Insert after linesToggleBtn
    lines_btn = """        val linesToggleBtn = Button(service).apply {
            text = "🕸"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showLinesBtn) View.VISIBLE else View.GONE
            setOnClickListener {
                service.engine.toggleDrawLines()
                text = if (service.engine.isDrawLinesEnabled) "🕸" else "🕸✖"
            }
        }"""
    
    if lines_btn in content:
        content = content.replace(lines_btn, lines_btn + "\n\n" + target_btn)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
