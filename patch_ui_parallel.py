with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_spinner = """            body.addView(macroSpinner)
        }"""

repl_spinner = """            body.addView(macroSpinner)
            
            val parallelSwitch = android.widget.Switch(service).apply {
                text = "Выполнять параллельно (Не прерывать текущий)"
                setTextColor(Color.parseColor("#FFA500"))
                isChecked = node.macroRunParallel
                setOnCheckedChangeListener { _, isChecked ->
                    node.macroRunParallel = isChecked
                }
                setPadding(20, 20, 0, 0)
            }
            body.addView(parallelSwitch)
        }"""

content = content.replace(find_spinner, repl_spinner)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("UI Parallel patched")
