import sys

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'r') as f:
    content = f.read()

bad_str = """                                }, null)
                            }, 50L)"""

good_str = """                                }, null)
                            })"""

content = content.replace(bad_str, good_str)

with open('./app/src/main/java/com/example/autoclicker/AutoClickService.kt', 'w') as f:
    f.write(content)
print("Patched postDelayed -> post")
