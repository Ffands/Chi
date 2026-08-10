import sys
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_if = """                setOnClickListener {
                    if (mode == AppMode.SINGLE && service.nodes.size > 1) {
                        val first = service.nodes.firstOrNull()
                        service.nodes.clear()
                        nodeViews.values.forEach { windowManager.removeView(it) }
                        nodeViews.clear()
                        nodeParams.clear()
                        swipeEndViews.values.forEach { windowManager.removeView(it) }
                        swipeEndViews.clear()
                        swipeEndParams.clear()
                        if (first != null) {
                            service.nodes.add(first)
                            createNodeView(first)
                        }
                    }
                    appMode = mode"""

good_if = """                setOnClickListener {
                    appMode = mode"""

content = content.replace(bad_if, good_if)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("Patched AppMode.SINGLE")
