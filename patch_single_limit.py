import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

add_old = """    fun addNode(type: NodeType, startX: Int? = null, startY: Int? = null) {
        val id = nodeCounter++"""
add_new = """    fun addNode(type: NodeType, startX: Int? = null, startY: Int? = null) {
        if (appMode == AppMode.SINGLE && service.nodes.isNotEmpty()) {
            android.widget.Toast.makeText(service, "В Одиночном режиме доступна только одна метка!", android.widget.Toast.LENGTH_SHORT).show()
            return
        }
        val id = nodeCounter++"""
content = content.replace(add_old, add_new)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Single node limit patched")
