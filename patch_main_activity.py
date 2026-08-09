import re

with open('./app/src/main/java/com/example/autoclicker/MainActivity.kt', 'r') as f:
    content = f.read()

# Add RadioGroup for modes
imports_old = "import android.widget.TextView"
imports_new = "import android.widget.TextView\nimport android.widget.RadioGroup\nimport android.widget.RadioButton\nimport android.content.Context"
content = content.replace(imports_old, imports_new)

# Insert after card3
target = """        contentLayout.addView(card3)"""
replacement = """        contentLayout.addView(card3)
        
        val modeLayout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Color.parseColor("#1B2A38"))
            setPadding(40, 40, 40, 40)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
            params.setMargins(0, 0, 0, 40)
            layoutParams = params
        }
        val modeTitle = TextView(this).apply {
            text = "РЕЖИМ РАБОТЫ"
            textSize = 18f
            typeface = Typeface.DEFAULT_BOLD
            setTextColor(Color.WHITE)
            setPadding(0, 0, 0, 20)
        }
        modeLayout.addView(modeTitle)
        
        val modeGroup = RadioGroup(this).apply {
            orientation = RadioGroup.VERTICAL
        }
        
        val modes = listOf(
            "SINGLE" to "Одиночный режим (1 метка)",
            "SEQUENTIAL" to "Многоцелевой режим (Цепочка)",
            "ADVANCED" to "Инженерный режим (Сложная логика)",
            "RECORD" to "Запись макроса (Ручной ввод)"
        )
        
        val prefs = getSharedPreferences("AutoClickerSettings", Context.MODE_PRIVATE)
        val currentMode = prefs.getString("AppMode", "ADVANCED")
        
        for ((modeId, modeDesc) in modes) {
            val rb = RadioButton(this).apply {
                text = modeDesc
                setTextColor(Color.WHITE)
                textSize = 16f
                setPadding(0, 20, 0, 20)
                tag = modeId
                isChecked = modeId == currentMode
            }
            modeGroup.addView(rb)
        }
        
        modeGroup.setOnCheckedChangeListener { group, checkedId ->
            val rb = group.findViewById<RadioButton>(checkedId)
            val selectedMode = rb.tag.toString()
            prefs.edit().putString("AppMode", selectedMode).apply()
            
            // Apply to running service if possible
            if (AutoClickService.instance != null) {
                AutoClickService.instance!!.updateAppMode(selectedMode)
            }
        }
        
        modeLayout.addView(modeGroup)
        contentLayout.addView(modeLayout)"""

content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/MainActivity.kt', 'w') as f:
    f.write(content)

print("MainActivity patched for Mode Selection")
