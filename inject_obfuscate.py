import os, re, base64

def obfuscate_class_names(smali_dir):
    renamed = {}
    for root, _, files in os.walk(smali_dir):
        for file in files:
            if file.endswith(".smali"):
                old_path = os.path.join(root, file)
                new_name = "C" + str(abs(hash(file)) % 10000) + ".smali"
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                renamed[file.replace(".smali", "")] = new_name.replace(".smali", "")
    print(f"[✓] Renamed {len(renamed)} classes.")
    return renamed

def encode_string(text):
    return base64.b64encode(text.encode()).decode()

def encrypt_smali_strings(smali_dir):
    pattern = re.compile(r'const-string [vp0-9]+, "(.*?)"')
    modified = 0

    for root, _, files in os.walk(smali_dir):
        for file in files:
            if not file.endswith(".smali"): continue
            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                match = pattern.search(line)
                if match:
                    original = match.group(1)
                    encoded = encode_string(original)
                    newline = line.replace(f'"{original}"', f'"{encoded}"')
                    new_lines.append(newline)
                    new_lines.append('    invoke-static {v0}, Lcom/shadow/obf/Utils;->decode(Ljava/lang/String;)Ljava/lang/String;\n')
                    modified += 1
                else:
                    new_lines.append(line)

            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(new_lines)

    print(f"[✓] Encrypted {modified} strings.")
