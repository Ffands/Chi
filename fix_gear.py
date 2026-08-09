import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# 1. Update gearBtn visibility
target_gear = """        val gearBtn = Button(service).apply {
            text = "⚙"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = if (showSettingsBtn) View.VISIBLE else View.GONE
            setOnClickListener { showModMenu() }
        }"""
replace_gear = """        val gearBtn = Button(service).apply {
            text = "⚙"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.TRANSPARENT)
            layoutParams = LinearLayout.LayoutParams(dpToPx(40), dpToPx(40))
            setPadding(0, 0, 0, 0)
            visibility = View.VISIBLE
            setOnClickListener { showModMenu() }
        }"""
content = content.replace(target_gear, replace_gear)

# 2. Update minMaxBtn visibility logic
target_minmax_vis = """                gearBtn.visibility = if (isMinimized || !showSettingsBtn) View.GONE else View.VISIBLE"""
replace_minmax_vis = """                gearBtn.visibility = if (isMinimized) View.GONE else View.VISIBLE"""
content = content.replace(target_minmax_vis, replace_minmax_vis)

# 3. Remove pGear
target_pgear = """        val pGear = android.widget.CheckBox(service).apply {
            text = "Кнопка 'Настройки' (⚙)"
            setTextColor(Color.WHITE)
            isChecked = showSettingsBtn
            setOnCheckedChangeListener { _, c -> showSettingsBtn = c; saveUISettings(); recreateFloatingControlBar() }
        }
        layout.addView(pEye)
        layout.addView(pLines)
        layout.addView(pHotbar)
        layout.addView(pGear)"""
replace_pgear = """        layout.addView(pEye)
        layout.addView(pLines)
        layout.addView(pHotbar)"""
content = content.replace(target_pgear, replace_pgear)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
