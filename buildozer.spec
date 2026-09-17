[app]
title = கர்ப்பகால யோகா
package.name = pregnancyyoga
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0

# Bundle the Tamil font and any images inside assets/ automatically
# because they live under source.dir.
requirements = python3,kivy

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/assets/images/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
