import re

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

target = """                    if (foundRect != null) {
                        if (isScaledDown) {
                            node.x = left + (foundRect.centerX() / scale).toInt()
                            node.y = top + (foundRect.centerY() / scale).toInt()
                        } else {
                            node.x = left + foundRect.centerX()
                            node.y = top + foundRect.centerY()
                        }
                    }"""

replacement = """                    if (foundRect != null) {
                        node.x = left + foundRect.centerX()
                        node.y = top + foundRect.centerY()
                    }"""

content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
