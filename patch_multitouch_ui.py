import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """        maxTimeLayout.addView(maxTimeEdit)
        layout.addView(maxTimeLayout)

        val extremeSpeedLayout = LinearLayout(service).apply {"""

replacement = """        maxTimeLayout.addView(maxTimeEdit)
        layout.addView(maxTimeLayout)

        val multitouchLayout = LinearLayout(service).apply { 
            orientation = LinearLayout.HORIZONTAL 
            setPadding(0, 10, 0, 10)
            gravity = Gravity.CENTER_VERTICAL
        }
        val multitouchCheck = android.widget.CheckBox(service).apply {
            text = "Синхронный Мультитач (может сбоить камеру)"
            setTextColor(Color.WHITE)
            isChecked = service.enableMultitouch
            setOnCheckedChangeListener { _, isChecked ->
                service.enableMultitouch = isChecked
                saveUISettings()
                if (isChecked) {
                    android.widget.Toast.makeText(service, "Внимание! Во многих играх мультитач вызывает сбой масштабирования камеры.", android.widget.Toast.LENGTH_LONG).show()
                }
            }
        }
        multitouchLayout.addView(multitouchCheck)
        layout.addView(multitouchLayout)

        val extremeSpeedLayout = LinearLayout(service).apply {"""
content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
