import re

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

target = """    var swipePathPoints: List<Pair<Float, Float>> = emptyList(),
    var ocrFullScreenClick: Boolean = false,
    var checkResolutionScale: Float = 1.0f
)"""
replacement = """    var swipePathPoints: List<Pair<Float, Float>> = emptyList(),
    var ocrFullScreenClick: Boolean = false,
    var checkResolutionScale: Float = 1.0f,
    var isSmartOcr: Boolean = false,
    var ocrOperator: String = ">=",
    var ocrTargetValue: Double = 0.0
)"""
content = content.replace(target, replacement)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
