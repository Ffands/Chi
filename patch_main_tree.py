import re

with open('./app/src/main/java/com/example/autoclicker/MainActivity.kt', 'r') as f:
    content = f.read()

# Add Tree Button to MainActivity
target = """        contentLayout.addView(startUiBtn)"""
replacement = """        contentLayout.addView(startUiBtn)
        
        val showTreeBtn = Button(this).apply {
            text = "ДЕРЕВО СЦЕНАРИЯ"
            setBackgroundColor(Color.parseColor("#9C27B0"))
            setTextColor(Color.WHITE)
            textSize = 16f
            setPadding(0, 30, 0, 30)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            )
            params.setMargins(0, 30, 0, 0)
            layoutParams = params
            setOnClickListener {
                showScenarioTree()
            }
        }
        contentLayout.addView(showTreeBtn)"""

content = content.replace(target, replacement)

# Add showScenarioTree function
func = """    private fun showScenarioTree() {
        val scroll = ScrollView(this).apply {
            setPadding(40, 40, 40, 40)
        }
        
        val treeText = TextView(this).apply {
            textSize = 14f
            setLineSpacing(0f, 1.2f)
            setTextColor(Color.BLACK)
        }
        
        val instance = AutoClickService.instance
        if (instance == null || instance.nodes.isEmpty()) {
            treeText.text = "Сценарий пуст или служба не запущена."
        } else {
            val sb = java.lang.StringBuilder()
            sb.append("Ваш сценарий:\\n\\n")
            for (node in instance.nodes) {
                sb.append("Метка [${node.id}]: ${if(node.isSwipe) "Свайп" else "Клик"}\\n")
                if (node.triggerMode == 0) sb.append("  ↳ Условие: Цвет ${node.colorOperator}\\n")
                if (node.triggerMode == 1) sb.append("  ↳ Условие: Картинка\\n")
                if (node.triggerMode == 2) sb.append("  ↳ Условие: Текст '${node.targetText}'\\n")
                
                if (node.linkedConditionNodeId != null) {
                    sb.append("  ↳ Логика: ${node.linkedConditionOperator} условие Метки [${node.linkedConditionNodeId}]\\n")
                }
                
                if (node.nextNodeIdOnSuccess != null) {
                    sb.append("  ↳ При успехе -> [${node.nextNodeIdOnSuccess}]\\n")
                } else if (!node.skipSequentialExecution) {
                    sb.append("  ↳ При успехе -> [Следующая по списку]\\n")
                }
                
                if (node.maxCheckCycles != null && node.maxCheckCycles!! > 0) {
                    sb.append("  ↳ Циклов проверок: ${node.maxCheckCycles}\\n")
                    if (node.nextNodeIdOnFail != null) {
                        sb.append("  ↳ При провале -> [${node.nextNodeIdOnFail}]\\n")
                    } else {
                        sb.append("  ↳ При провале -> [Следующая по списку]\\n")
                    }
                }
                sb.append("\\n")
            }
            treeText.text = sb.toString()
        }
        
        scroll.addView(treeText)
        
        android.app.AlertDialog.Builder(this)
            .setTitle("ДЕРЕВО СЦЕНАРИЯ")
            .setView(scroll)
            .setPositiveButton("ЗАКРЫТЬ", null)
            .show()
    }
"""

content = content.replace("    private fun createCard", func + "    private fun createCard")

with open('./app/src/main/java/com/example/autoclicker/MainActivity.kt', 'w') as f:
    f.write(content)

print("MainActivity patched with Scenario Tree")
