import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

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

insertion_point = "        topRow.addView(dragHandle)"

if target_btn not in content:
    content = content.replace(insertion_point, target_btn + "\n\n" + insertion_point)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
