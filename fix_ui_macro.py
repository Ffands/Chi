with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_anti = """        if (node.type == NodeType.CHECK_COLOR) {
            antiDetectSection.visibility = View.GONE
        }"""

repl_anti = """        if (node.type == NodeType.CHECK_COLOR) {
            antiDetectSection.visibility = View.GONE
        }
        
        val macroSection = addSection("Настройки Макроса", node.macroProfileName != null) { body ->
            val tvMacroDesc = TextView(service).apply {
                text = "Если условие выполнится, будет загружен и запущен выбранный профиль."
                setTextColor(Color.LTGRAY)
                setScaledTextSize(12f)
                setPadding(0, 0, 0, 10)
            }
            body.addView(tvMacroDesc)
            
            val prefs = service.getSharedPreferences("AutoClickerProfiles", android.content.Context.MODE_PRIVATE)
            val allKeys = prefs.all.keys.toList()
            val spinnerItems = mutableListOf("— Не выбрано —")
            spinnerItems.addAll(allKeys)
            
            val macroSpinner = android.widget.Spinner(service).apply {
                val adapter = android.widget.ArrayAdapter(service, android.R.layout.simple_spinner_dropdown_item, spinnerItems)
                this.adapter = adapter
                
                val currentIdx = spinnerItems.indexOf(node.macroProfileName ?: "")
                if (currentIdx != -1) {
                    setSelection(currentIdx)
                }
                onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
                    override fun onItemSelected(p0: android.widget.AdapterView<*>?, p1: View?, pos: Int, id: Long) {
                        if (pos == 0) {
                            node.macroProfileName = null
                        } else {
                            node.macroProfileName = spinnerItems[pos]
                        }
                    }
                    override fun onNothingSelected(p0: android.widget.AdapterView<*>?) {}
                }
            }
            body.addView(macroSpinner)
        }
        if (node.type != NodeType.MACRO) {
            macroSection.visibility = View.GONE
            if (node.type == NodeType.CHECK_COLOR) {
                // If it's just check color (trigger), no antidetect
                antiDetectSection.visibility = View.GONE
            }
        } else {
            // It's a macro. Hide antidetect
            antiDetectSection.visibility = View.GONE
        }"""

content = content.replace(find_anti, repl_anti)

# We also need to hide Swipe settings if it's a MACRO
find_swipe = """            if (node.type == NodeType.CHECK_COLOR) {
                swipeLayout.visibility = View.GONE
                swipeDurRow.visibility = View.GONE
                swipeDeltaLayout.visibility = View.GONE
                clickDurRow.visibility = View.GONE
            }"""

repl_swipe = """            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO) {
                swipeLayout.visibility = View.GONE
                swipeDurRow.visibility = View.GONE
                swipeDeltaLayout.visibility = View.GONE
                clickDurRow.visibility = View.GONE
            }"""

content = content.replace(find_swipe, repl_swipe)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("UI MACRO patched")
