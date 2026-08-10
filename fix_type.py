with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

old_type = """        val typeSwitch = android.widget.Switch(service).apply {
            text = if (node.type == NodeType.CHECK_COLOR) "ТРИГГЕР " else "КЛИК "
            setTextColor(Color.YELLOW)
            isChecked = node.type == NodeType.CHECK_COLOR
            visibility = if (appMode == AppMode.ADVANCED) View.VISIBLE else View.GONE
            setOnCheckedChangeListener { _, isChecked ->
                node.type = if (isChecked) NodeType.CHECK_COLOR else NodeType.CLICK
                showEditNodeMenu(node)
                nodeViews[node.id]?.invalidate()
            }
        }
        headerLayout.addView(typeSwitch)"""

new_type = """        val typeSpinner = android.widget.Spinner(service).apply {
            val items = arrayOf("КЛИК", "ТРИГГЕР", "МАКРОС")
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
                    }
                    if (node.type != newType) {
                        node.type = newType
                        showEditNodeMenu(node)
                        nodeViews[node.id]?.invalidate()
                    }
                }
                override fun onNothingSelected(p0: android.widget.AdapterView<*>?) {}
            }
        }
        headerLayout.addView(typeSpinner)"""

content = content.replace(old_type, new_type)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Type patched!")
