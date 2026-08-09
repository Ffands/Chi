import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Apply to buttons when creating them
vis_toggle_old = """        val toggleVisBtn = Button(service).apply {
            text = "👁"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)"""
vis_toggle_new = """        val toggleVisBtn = Button(service).apply {
            text = "👁"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showEyeBtn) View.VISIBLE else View.GONE"""
content = content.replace(vis_toggle_old, vis_toggle_new)

gear_toggle_old = """        val gearBtn = Button(service).apply {
            text = "⚙"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)"""
gear_toggle_new = """        val gearBtn = Button(service).apply {
            text = "⚙"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showSettingsBtn) View.VISIBLE else View.GONE"""
content = content.replace(gear_toggle_old, gear_toggle_new)

hotbar_toggle_old = """        val hotbarToggleBtn = Button(service).apply {
            text = "⚡"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)"""
hotbar_toggle_new = """        val hotbarToggleBtn = Button(service).apply {
            text = "⚡"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showHotbarBtn) View.VISIBLE else View.GONE"""
content = content.replace(hotbar_toggle_old, hotbar_toggle_new)

lines_toggle_old = """        val linesToggleBtn = Button(service).apply {
            text = "🕸"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)"""
lines_toggle_new = """        val linesToggleBtn = Button(service).apply {
            text = "🕸"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showLinesBtn) View.VISIBLE else View.GONE"""
content = content.replace(lines_toggle_old, lines_toggle_new)

# Apply to minMaxBtn logic
minmax_old = """                playBtn.visibility = vis
                recordBtn.visibility = if (isMinimized || appMode != AppMode.RECORD) View.GONE else View.VISIBLE
                toggleVisBtn.visibility = vis
                linesToggleBtn.visibility = vis
                hotbarToggleBtn.visibility = vis
                gearBtn.visibility = vis
                exitBtn.visibility = vis
                if (isMinimized) hotbarRow.visibility = View.GONE"""
minmax_new = """                playBtn.visibility = vis
                recordBtn.visibility = if (isMinimized || appMode != AppMode.RECORD) View.GONE else View.VISIBLE
                toggleVisBtn.visibility = if (isMinimized || !showEyeBtn) View.GONE else View.VISIBLE
                linesToggleBtn.visibility = if (isMinimized || !showLinesBtn) View.GONE else View.VISIBLE
                hotbarToggleBtn.visibility = if (isMinimized || !showHotbarBtn) View.GONE else View.VISIBLE
                gearBtn.visibility = if (isMinimized || !showSettingsBtn) View.GONE else View.VISIBLE
                exitBtn.visibility = vis
                if (isMinimized) hotbarRow.visibility = View.GONE"""
content = content.replace(minmax_old, minmax_new)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("Applied panel visibility rules")
