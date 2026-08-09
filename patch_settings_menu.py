import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Let's insert toggles right after Alpha/Scale settings
insert_marker = """        scaleLayout.addView(Button(service).apply { text = "+"; setOnClickListener { if(uiScale < 2.0f) { uiScale += 0.1f; applyUIScaleChange() } } })
        layout.addView(scaleLayout)"""
        
new_settings = """        scaleLayout.addView(Button(service).apply { text = "+"; setOnClickListener { if(uiScale < 2.0f) { uiScale += 0.1f; applyUIScaleChange() } } })
        layout.addView(scaleLayout)
        
        layout.addView(TextView(service).apply { text = "Панель инструментов"; setTextColor(Color.WHITE); setScaledTextSize(14f); setPadding(0, 15, 0, 10) })
        
        val pEye = android.widget.CheckBox(service).apply {
            text = "Кнопка 'Видимость меток' (👁)"
            setTextColor(Color.WHITE)
            isChecked = showEyeBtn
            setOnCheckedChangeListener { _, c -> showEyeBtn = c; saveUISettings(); recreateFloatingControlBar() }
        }
        val pLines = android.widget.CheckBox(service).apply {
            text = "Кнопка 'Линии связи' (🕸)"
            setTextColor(Color.WHITE)
            isChecked = showLinesBtn
            setOnCheckedChangeListener { _, c -> showLinesBtn = c; saveUISettings(); recreateFloatingControlBar() }
        }
        val pHotbar = android.widget.CheckBox(service).apply {
            text = "Кнопка 'Быстрая панель' (⚡)"
            setTextColor(Color.WHITE)
            isChecked = showHotbarBtn
            setOnCheckedChangeListener { _, c -> showHotbarBtn = c; saveUISettings(); recreateFloatingControlBar() }
        }
        val pGear = android.widget.CheckBox(service).apply {
            text = "Кнопка 'Настройки' (⚙)"
            setTextColor(Color.WHITE)
            isChecked = showSettingsBtn
            setOnCheckedChangeListener { _, c -> showSettingsBtn = c; saveUISettings(); recreateFloatingControlBar() }
        }
        layout.addView(pEye)
        layout.addView(pLines)
        layout.addView(pHotbar)
        layout.addView(pGear)"""

content = content.replace(insert_marker, new_settings)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)

print("Settings menu patched")
