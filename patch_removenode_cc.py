import sys

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

bad_str = """    private fun removeNode(id: Int) {
        val view = nodeViews.remove(id)
        if (view != null) windowManager.removeView(view)
        nodeParams.remove(id)
        removeSwipeEndMarker(id)
        removeTextZoneMarkers(id)
        val idx = service.nodes.indexOfFirst { it.id == id }"""

good_str = """    private fun removeNode(id: Int) {
        val view = nodeViews.remove(id)
        if (view != null) windowManager.removeView(view)
        nodeParams.remove(id)
        removeSwipeEndMarker(id)
        removeTextZoneMarkers(id)
        removeColorCompareMarker(id)
        val idx = service.nodes.indexOfFirst { it.id == id }"""

content = content.replace(bad_str, good_str)
with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
print("removenode color compare patched")
