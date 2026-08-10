with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

find_skip = """        if (node.type == NodeType.CHECK_COLOR && appMode == AppMode.ADVANCED) {
            val skipSwitch = android.widget.Switch(service).apply {
                text = "Пропуск очереди"
                setTextColor(Color.CYAN)
                isChecked = node.skipSequentialExecution
                setOnCheckedChangeListener { _, isChecked ->
                    node.skipSequentialExecution = isChecked
                }
            }
            headerLayout.addView(skipSwitch)
        }"""

repl_skip = """        if (appMode == AppMode.ADVANCED) {
            if (node.type == NodeType.CHECK_COLOR || node.type == NodeType.MACRO) {
                val skipSwitch = android.widget.Switch(service).apply {
                    text = "Функция (Пропуск в очереди)"
                    setTextColor(Color.CYAN)
                    isChecked = node.skipSequentialExecution
                    setOnCheckedChangeListener { _, isChecked ->
                        node.skipSequentialExecution = isChecked
                    }
                }
                headerLayout.addView(skipSwitch)
            }
            
            val threadSwitch = android.widget.Switch(service).apply {
                text = "Отдельный поток (Параллельно)"
                setTextColor(Color.parseColor("#FFA500")) // Orange
                isChecked = node.isIndependentThread
                setOnCheckedChangeListener { _, isChecked ->
                    node.isIndependentThread = isChecked
                }
            }
            headerLayout.addView(threadSwitch)
        }"""

content = content.replace(find_skip, repl_skip)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("UI THREAD patched")
