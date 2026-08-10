import sys
with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

mroutes_code = """
            val mRoutes = mutableListOf<ManagerRoute>()
            if (obj.has("managerRoutes")) {
                val routesArray = obj.getJSONArray("managerRoutes")
                for (i in 0 until routesArray.length()) {
                    val rObj = routesArray.getJSONObject(i)
                    mRoutes.add(ManagerRoute(
                        checkNodeId = rObj.getInt("checkNodeId"),
                        onSuccessGoToId = rObj.getInt("onSuccessGoToId")
                    ))
                }
            }
            return TargetNode("""

content = content.replace("            return TargetNode(", mroutes_code)
with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
print("Added mRoutes parsing")
