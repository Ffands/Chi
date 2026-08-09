import re

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

target = """    var isSmartOcr: Boolean = false,
    var ocrOperator: String = ">=",
    var ocrTargetValue: Double = 0.0
)"""
replacement = """    var isSmartOcr: Boolean = false,
    var ocrOperator: String = ">=",
    var ocrTargetValue: Double = 0.0,
    var ocrCustomSuffixes: String = "k:1000,m:1000000,b:1000000000,к:1000,м:1000000,б:1000000000"
)"""

content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
