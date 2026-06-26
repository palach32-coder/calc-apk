[app]
# Название и пакет
title = Имперский калькулятор
package.name = imperialcalc
package.domain = org.imperial

# Исходные файлы
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Иконка
icon.filename = %(source.dir)s/icon.jpg

# Требования и разрешения
requirements = python3,kivy
android.permissions = INTERNET

# Настройки Android (стабильные версии)
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25.1.8937393
android.archs = arm64-v8a, armeabi-v7a
orientation = portrait

# ВАЖНО: Принудительное указание путей, чтобы сборщик не терял их
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.1.8937393

[buildozer]
log_level = 2
warn_on_root = 1
# Это ускоряет сборку на серверах GitHub
build_mode = debug
