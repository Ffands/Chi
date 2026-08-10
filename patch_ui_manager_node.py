import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# 1. Update the spinner for NodeType
find_spinner = """            val items = arrayOf("Клик", "Триггер (Цвет/Текст)", "Макрос")
            val typeSpinner = android.widget.Spinner(service).apply {
                val adapter = android.widget.ArrayAdapter(service, android.R.layout.simple_spinner_dropdown_item, items)
                this.adapter = adapter
                setSelection(when(node.type) {
                    NodeType.CLICK -> 0
                    NodeType.CHECK_COLOR -> 1
                    NodeType.MACRO -> 2
                })
                visibility = if (appMode == AppMode.ADVANCED) View.VISIBLE else View.GONE
                onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
                    override fun onItemSelected(p0: android.widget.AdapterView<*>?, p1: View?, pos: Int, id: Long) {
                        val newType = when(pos) {
                            0 -> NodeType.CLICK
                            1 -> NodeType.CHECK_COLOR
                            2 -> NodeType.MACRO
                            else -> NodeType.CLICK
                        }"""
repl_spinner = """            val items = arrayOf("Клик", "Триггер (Цвет/Текст)", "Макрос", "Менеджер")
            val typeSpinner = android.widget.Spinner(service).apply {
                val adapter = android.widget.ArrayAdapter(service, android.R.layout.simple_spinner_dropdown_item, items)
                this.adapter = adapter
                setSelection(when(node.type) {
                    NodeType.CLICK -> 0
                    NodeType.CHECK_COLOR -> 1
                    NodeType.MACRO -> 2
                    NodeType.MANAGER -> 3
                })
                visibility = if (appMode == AppMode.ADVANCED) View.VISIBLE else View.GONE
                onItemSelectedListener = object : android.widget.AdapterView.OnItemSelectedListener {
                    override fun onItemSelected(p0: android.widget.AdapterView<*>?, p1: View?, pos: Int, id: Long) {
                        val newType = when(pos) {
                            0 -> NodeType.CLICK
                            1 -> NodeType.CHECK_COLOR
                            2 -> NodeType.MACRO
                            3 -> NodeType.MANAGER
                            else -> NodeType.CLICK
                        }"""

content = content.replace(find_spinner, repl_spinner)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Spinner updated")
