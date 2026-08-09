import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

target = """    var isMenuFullscreen = false
    var isCaffeineEnabled = false"""
replacement = """    var isMenuFullscreen = false
    var isCaffeineEnabled = false
    var showEyeBtn = true
    var showLinesBtn = true
    var showHotbarBtn = true
    var showSettingsBtn = true
    var ocrCustomSuffixes = "" """

content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
