# Shadow APK Crypter – HellGate v2.0

An advanced tool for merging and encrypting APKs with different payloads, designed to provide multiple layers of protection and obfuscation.

**Note:** This project is a prototype and requires further development.

## ✨ Overview

Shadow APK Crypter is a sophisticated tool designed to merge and encrypt Android applications (APK files) with malicious payloads in a way that makes detection and analysis significantly more difficult. Its primary function is to "wrap" the payload within a legitimate (clean) application and apply multiple layers of protection and concealment.

## 🔥 Key Features

* Advanced payload encryption using multiple layers (XOR, RC4, Compression, Base64)
* Code and string obfuscation
* Anti-debugging and anti-emulator protection
* Generation of fake metadata
* Support for changing app icon and name
* Automatic APK signing
* Boot-time execution capability
* Multiple encryption layers
* Custom protection mechanisms

## 📦 Requirements

* Python 3.7+
* Java JDK 8+
* Android SDK (for aapt2)
* `apktool.jar`
* `uber-apk-signer.jar`

## 🔧 Installation

1. Install Python requirements:

    ```bash
    pip install -r requirements.txt
    ```

2. Place the following files in the `tools/` folder:

    *   `apktool.jar`
    *   `uber-apk-signer.jar`
    *   `keystore.jks` (optional)

3. Place the clean target APK in `libs/CleanApp.apk`.
4. Place your payload APK in `payloads/CraxsRat.apk`.

## 🚀 Usage

To run the tool, execute the `build_forge.py` script:

```bash
python build_forge.py
```

The resulting encrypted and merged APK will be located in the `output/` directory.

## 📂 Project Structure

```
shadow_apk_crypter/
├── libs/                  # Clean dummy app
├── payloads/              # Payload APK (e.g., CraxsRat.apk)
├── output/                # Final output APK
├── tools/                 # Building and signing tools
├── templates/             # Interface templates
└── build_forge.py         # Main build script
```

##   ️ Core Components

### Main Scripts
* `shadow_apk_crypter.py`: Main script managing encryption and merging
* `payload_encrypter.py`: Handles payload encryption with multiple layers
* `build_forge.py`: Orchestrates the APK decompilation, injection, and rebuilding process
* `injector.py`: Injects the payload into the clean app and handles package name changes
* `inject_obfuscate.py`: Performs class name and string obfuscation

### Smali Components
* `smali/`: Contains modified Smali files:
  * `Utils.smali.txt`: Decoding utility for encrypted strings
  * `BootReceiver.smali.txt`: Handles boot-time execution

## 🔄 Build Process

1. **Decompilation**
   * Decompiles both CleanApp.apk and payload APK using apktool
   * Converts to Smali format in tmp/ directory

2. **Payload Injection**
   * Copies payload Smali files to clean app's Smali directory
   * Integrates payload functionality with clean app

3. **Manifest Modification**
   * Adds necessary permissions for payload functionality
   * Generates and applies random package name
   * Updates manifest entries

4. **Code Protection**
   * Applies string encryption
   * Performs class name obfuscation
   * Injects anti-debug and anti-vm protection
   * Adds fake code and metadata

5. **Rebuilding**
   * Rebuilds modified Smali files into APK
   * Signs the final APK
   * Outputs to output/ directory

## 🔒 Security Features

* **Multiple Encryption Layers**
  * XOR encryption
  * RC4 encryption
  * Data compression
  * Base64 encoding

* **Anti-Analysis Protection**
  * Anti-debugging mechanisms
  * Anti-emulator detection
  * Code obfuscation
  * String encryption

* **Stealth Features**
  * Random package name generation
  * Fake metadata injection
  * Boot-time execution
  * Background service integration

## 🌐 My Websites

* [Shadow Hacker](https://www.shadowhackr.com/)
* [moPDF](https://www.mopdf.com/)
* [Facebook Profile](https://www.facebook.com/Tareq.DJX/)

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring they have the right to modify and use any applications or payloads with this tool. The developers are not responsible for any misuse or damage caused by this tool.

## 🔄 Future Development

This project is a prototype and requires further development. Planned improvements include:
* Enhanced encryption algorithms
* Improved anti-analysis features
* Better code obfuscation
* GUI interface
* Additional payload support
* Advanced protection mechanisms

