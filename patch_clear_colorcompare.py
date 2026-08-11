import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """                        textZoneEndViews.clear()
                        textZoneEndParams.clear()
                        if (first != null) {"""

good_str = """                        textZoneEndViews.clear()
                        textZoneEndParams.clear()
                        colorCompareViews.values.forEach { windowManager.removeView(it) }
                        colorCompareViews.clear()
                        colorCompareParams.clear()
                        if (first != null) {"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("clear color compare patched")
