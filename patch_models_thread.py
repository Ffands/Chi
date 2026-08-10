with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'r') as f:
    content = f.read()

content = content.replace("var skipSequentialExecution: Boolean = false,", "var skipSequentialExecution: Boolean = false,\n    var isIndependentThread: Boolean = false,")

tojson_find = """        if (skipSequentialExecution) obj.put("skipSequentialExecution", skipSequentialExecution)"""
tojson_repl = """        if (skipSequentialExecution) obj.put("skipSequentialExecution", skipSequentialExecution)\n        if (isIndependentThread) obj.put("isIndependentThread", isIndependentThread)"""
content = content.replace(tojson_find, tojson_repl)

fromjson_find = """val skipSeq = obj.optBoolean("skipSequentialExecution", false)"""
fromjson_repl = """val skipSeq = obj.optBoolean("skipSequentialExecution", false)\n            val isIndep = obj.optBoolean("isIndependentThread", false)"""
content = content.replace(fromjson_find, fromjson_repl)

fromjson2_find = """skipSequentialExecution = skipSeq,"""
fromjson2_repl = """skipSequentialExecution = skipSeq,\n                isIndependentThread = isIndep,"""
content = content.replace(fromjson2_find, fromjson2_repl)

with open('./app/src/main/java/com/example/autoclicker/Models.kt', 'w') as f:
    f.write(content)
print("Models patched for isIndependentThread")
