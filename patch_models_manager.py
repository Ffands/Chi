import re

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

content = content.replace("enum class NodeType { CLICK, CHECK_COLOR, MACRO }", "enum class NodeType { CLICK, CHECK_COLOR, MACRO, MANAGER }")

manager_route_class = """data class ManagerRoute(
    var checkNodeId: Int,
    var onSuccessGoToId: Int
) {
    fun toJson(): org.json.JSONObject {
        val obj = org.json.JSONObject()
        obj.put("checkNodeId", checkNodeId)
        obj.put("onSuccessGoToId", onSuccessGoToId)
        return obj
    }
    companion object {
        fun fromJson(obj: org.json.JSONObject): ManagerRoute {
            return ManagerRoute(
                obj.getInt("checkNodeId"),
                obj.getInt("onSuccessGoToId")
            )
        }
    }
}

data class TargetNode("""
content = content.replace("data class TargetNode(", manager_route_class)

content = content.replace("var swipePathPoints: List<Pair<Float, Float>> = emptyList(),", "var swipePathPoints: List<Pair<Float, Float>> = emptyList(),\n    var managerRoutes: List<ManagerRoute> = emptyList(),")


json_serialization = """        if (swipePathPoints.isNotEmpty()) {
            val pointArr = org.json.JSONArray()
            for (p in swipePathPoints) {
                val pObj = org.json.JSONObject()
                pObj.put("x", p.first.toDouble())
                pObj.put("y", p.second.toDouble())
                pointArr.put(pObj)
            }
            obj.put("swipePathPoints", pointArr)
        }"""
new_json_serialization = json_serialization + """
        if (managerRoutes.isNotEmpty()) {
            val mrArr = org.json.JSONArray()
            for (mr in managerRoutes) {
                mrArr.put(mr.toJson())
            }
            obj.put("managerRoutes", mrArr)
        }"""
content = content.replace(json_serialization, new_json_serialization)

json_deserialization = """            if (obj.has("swipePathPoints")) {
                val arr = obj.getJSONArray("swipePathPoints")
                for (i in 0 until arr.length()) {
                    val pObj = arr.getJSONObject(i)
                    pathPoints.add(Pair(pObj.getDouble("x").toFloat(), pObj.getDouble("y").toFloat()))
                }
            }"""
new_json_deserialization = json_deserialization + """
            val mRoutes = mutableListOf<ManagerRoute>()
            if (obj.has("managerRoutes")) {
                val arr = obj.getJSONArray("managerRoutes")
                for (i in 0 until arr.length()) {
                    mRoutes.add(ManagerRoute.fromJson(arr.getJSONObject(i)))
                }
            }"""
content = content.replace(json_deserialization, new_json_deserialization)

content = content.replace("swipePathPoints = pathPoints,", "swipePathPoints = pathPoints,\n                managerRoutes = mRoutes,")

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
print("Models patched")
