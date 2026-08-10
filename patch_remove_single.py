with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "enum class AppMode { SINGLE, SEQUENTIAL, ADVANCED, RECORD }",
    "enum class AppMode { SEQUENTIAL, ADVANCED, RECORD }"
)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    ui = f.read()

ui = ui.replace(
    '            AppMode.SINGLE to "Одиночный (1 клик)",\n',
    ''
)
ui = ui.replace(
    """                    if (mode == AppMode.SINGLE && service.nodes.size > 1) {
                        Toast.makeText(service, "Очистите профиль для одиночного режима", Toast.LENGTH_SHORT).show()
                        return@setOnItemSelectedListener
                    }""",
    ""
)

# Removing AppMode.SINGLE condition visibility = if (appMode == AppMode.SINGLE && service.nodes.isNotEmpty()) View.GONE else View.VISIBLE
# on line 840. We can just set it to View.VISIBLE
ui = ui.replace(
    "visibility = if (appMode == AppMode.SINGLE && service.nodes.isNotEmpty()) View.GONE else View.VISIBLE",
    "visibility = View.VISIBLE"
)
ui = ui.replace(
    "if (appMode == AppMode.SINGLE && service.nodes.isNotEmpty()) {",
    "if (false) {"
)
ui = ui.replace(
    "if (appMode == AppMode.SINGLE) {",
    "if (false) {"
)
ui = ui.replace(
    "if (appMode == AppMode.SINGLE || (appMode == AppMode.SEQUENTIAL && node.type == NodeType.CLICK)) {",
    "if (appMode == AppMode.SEQUENTIAL && node.type == NodeType.CLICK) {"
)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(ui)

print("Removed Single mode")
