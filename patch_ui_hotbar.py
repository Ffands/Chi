import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Replace the layout creation
old_layout = """        val layout = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
            setBackgroundColor(Color.parseColor("#FF111111"))
            setPadding(5, 5, 5, 5)
            
            // Add a border
            val drawable = android.graphics.drawable.GradientDrawable()
            drawable.setColor(Color.parseColor("#FF111111"))
            drawable.setStroke(dpToPx(2), Color.parseColor("#FF4CAF50"))
            drawable.cornerRadius = dpToPx(8).toFloat()
            background = drawable
        }"""

new_layout = """        val layout = LinearLayout(service).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#FF111111"))
            setPadding(5, 5, 5, 5)
            
            // Add a border
            val drawable = android.graphics.drawable.GradientDrawable()
            drawable.setColor(Color.parseColor("#FF111111"))
            drawable.setStroke(dpToPx(2), Color.parseColor("#FF4CAF50"))
            drawable.cornerRadius = dpToPx(8).toFloat()
            background = drawable
        }
        
        val topRow = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
        }
        
        val hotbarRow = HorizontalScrollView(service).apply {
            visibility = View.GONE
            layoutParams = LinearLayout.LayoutParams(dpToPx(280), WindowManager.LayoutParams.WRAP_CONTENT)
            setPadding(0, dpToPx(5), 0, 0)
        }
        val hotbarContainer = LinearLayout(service).apply {
            orientation = LinearLayout.HORIZONTAL
        }
        hotbarRow.addView(hotbarContainer)
"""

# Replace layout.addView(...) with topRow.addView(...)
old_adds = """        layout.addView(dragHandle)
        layout.addView(minMaxBtn)
        layout.addView(playBtn)
        layout.addView(recordBtn)
        layout.addView(toggleVisBtn)
        layout.addView(gearBtn)
        layout.addView(exitBtn)"""

new_adds = """        val hotbarToggleBtn = Button(service).apply {
            text = "⚡"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                if (hotbarRow.visibility == View.VISIBLE) {
                    hotbarRow.visibility = View.GONE
                } else {
                    hotbarRow.visibility = View.VISIBLE
                    updateHotbar(hotbarContainer)
                }
            }
        }
        
        val linesToggleBtn = Button(service).apply {
            text = "🕸"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            setOnClickListener {
                service.showLines = !service.showLines
                text = if (service.showLines) "🕸" else "🕸✖"
                linesOverlayView?.visibility = if (service.showLines) View.VISIBLE else View.INVISIBLE
                linesOverlayView?.invalidate()
            }
        }

        topRow.addView(dragHandle)
        topRow.addView(minMaxBtn)
        topRow.addView(playBtn)
        topRow.addView(recordBtn)
        topRow.addView(toggleVisBtn)
        topRow.addView(linesToggleBtn)
        topRow.addView(hotbarToggleBtn)
        topRow.addView(gearBtn)
        topRow.addView(exitBtn)
        
        layout.addView(topRow)
        layout.addView(hotbarRow)"""

# Add updateHotbar func and modify minMaxBtn logic
minmax_old = """                val vis = if (isMinimized) View.GONE else View.VISIBLE
                playBtn.visibility = vis
                recordBtn.visibility = if (isMinimized || appMode != AppMode.RECORD) View.GONE else View.VISIBLE
                toggleVisBtn.visibility = vis
                gearBtn.visibility = vis
                exitBtn.visibility = vis"""

minmax_new = """                val vis = if (isMinimized) View.GONE else View.VISIBLE
                playBtn.visibility = vis
                recordBtn.visibility = if (isMinimized || appMode != AppMode.RECORD) View.GONE else View.VISIBLE
                toggleVisBtn.visibility = vis
                linesToggleBtn.visibility = vis
                hotbarToggleBtn.visibility = vis
                gearBtn.visibility = vis
                exitBtn.visibility = vis
                if (isMinimized) hotbarRow.visibility = View.GONE"""

content = content.replace(old_layout, new_layout)
content = content.replace(old_adds, new_adds)
content = content.replace(minmax_old, minmax_new)

# Add updateHotbar function to UIManager
hotbar_func = """
    private fun updateHotbar(container: LinearLayout) {
        container.removeAllViews()
        val profiles = service.getSavedProfiles()
        if (profiles.isEmpty()) {
            val tv = TextView(service).apply {
                text = "Нет профилей"
                setTextColor(Color.GRAY)
                setPadding(dpToPx(10), 0, dpToPx(10), 0)
            }
            container.addView(tv)
            return
        }
        for (p in profiles) {
            val btn = Button(service).apply {
                text = p
                setTextColor(Color.WHITE)
                setBackgroundColor(Color.parseColor("#222222"))
                setPadding(dpToPx(10), dpToPx(5), dpToPx(10), dpToPx(5))
                val params = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
                params.setMargins(0, 0, dpToPx(5), 0)
                layoutParams = params
                
                setOnClickListener {
                    service.loadProfile(p)
                    service.uiManager.updateMenu()
                    android.widget.Toast.makeText(service, "Загружен: $p", android.widget.Toast.LENGTH_SHORT).show()
                }
            }
            container.addView(btn)
        }
    }
"""

# Insert updateHotbar before showFloatingControlBar
content = content.replace("    fun showFloatingControlBar() {", hotbar_func + "    fun showFloatingControlBar() {")

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("Patched hotbar and lines visibility toggle")
