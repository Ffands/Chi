import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target_1 = """            } else if (node.triggerMode == 1) { // Image Fragment
                body.addView(colorOpLayout)
                body.addView(fragZoneBtn)
                body.addView(imgThresholdLayout)
                body.addView(searchRadiusLayout)
                body.addView(imgPreview)"""

replacement_1 = """            } else if (node.triggerMode == 1) { // Image Fragment
                body.addView(colorOpLayout)
                body.addView(fragZoneBtn)
                body.addView(imgThresholdLayout)
                body.addView(searchRadiusLayout)
                body.addView(resolutionScaleLayout)
                body.addView(imgPreview)"""

content = content.replace(target_1, replacement_1)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
