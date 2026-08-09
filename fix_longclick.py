import re

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'r') as f:
    content = f.read()

# Add to minMaxBtn
target_minmax = """                if (isMinimized) hotbarRow.visibility = View.GONE
            }
        }"""
replace_minmax = """                if (isMinimized) hotbarRow.visibility = View.GONE
            }
            setOnLongClickListener {
                showSettingsBtn = true
                saveUISettings()
                gearBtn.visibility = View.VISIBLE
                showModMenu()
                true
            }
        }"""
content = content.replace(target_minmax, replace_minmax)

# Add to playBtn
target_play = """                text = if (service.isPlaying) "⏸" else "▶"
                setTextColor(if (service.isPlaying) Color.parseColor("#FFD50000") else Color.parseColor("#FF00C853"))
            }
        }"""
replace_play = """                text = if (service.isPlaying) "⏸" else "▶"
                setTextColor(if (service.isPlaying) Color.parseColor("#FFD50000") else Color.parseColor("#FF00C853"))
            }
            setOnLongClickListener {
                showSettingsBtn = true
                saveUISettings()
                gearBtn.visibility = View.VISIBLE
                showModMenu()
                true
            }
        }"""
content = content.replace(target_play, replace_play)

with open('./app/src/main/java/com/example/autoclicker/UIManager.kt', 'w') as f:
    f.write(content)
