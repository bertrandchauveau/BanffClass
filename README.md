# BanffClass - a Kidney Transplant Biopsy Classification Tool


BanffClass is a free, open-source desktop application designed to apply the Banff classification for kidney allograft pathology based on individual histological scores and clinico-biological parameters. It provides both rejection diagnoses and continuous indices in a user-friendly interface.

## 🚀 About
BanffClass is a desktop application that helps pathologists, nephrologists, and researchers apply the 2024 Banff classification for kidney transplant biopsies. The tool:
- Implements the Banff 2022-2024 updates as closely as possible to the official guidelines
- Provides both case-by-case analysis and batch processing modes
- Computes rejection diagnoses (TCMR, AMR/MVI) and continuous indices
- Is 100% local: no data transfer, no data retention - your patient data never leaves your computer

## Key Features
- 🔍 1-by-1 Mode	for interactive analysis of individual cases with visual variable selection
- 📊 Batch Mode	for processing multiple cases from an Excel file simultaneously
- 🧮 Continuous Indices	computes activity, chronicity, AMR/MVI, and TCMR/TI indices
- 🔄 Version Ready	with architecture supporting future Banff classification versions
- 💻 Cross-Platform	(Windows and macOS)

## ⚠️ Important Notice
This application is **NOT meant for clinical use**. It is provided for **RESEARCH AND EDUCATIONAL purposes only**. By using this application, you agree to the License terms (available when launching the app).

## 📥 Installation
### System Requirements
- Windows: Windows 10 or later (64-bit)
- macOS: macOS Catalina (10.15) or later

### Downloading the Application
- Go to the [Releases page](https://github.com/bertrandchauveau/banffclass_local/releases/latest))
- Download the latest release for your operating system:
  - BanffClass-windows.zip (for Windows users)
  - BanffClass-macos.zip (for macOS users)
- Extract the ZIP file to a location of your choice

### 🛡️ Important Security Note
These applications are unsigned. This means that:

- Windows: You'll see a "Windows protected your PC" warning
- macOS: You'll encounter "Gatekeeper" warnings (see below)

This is normal and expected. The application is open-source, and you can verify the code yourself on GitHub.

### For Institutional/Enterprise Devices
If you're installing this on an institutional or corporate device:

- Please check with your IT department first
- Your organization may have strict security policies regarding unsigned applications
- Some institutions require approval for any software installation
- Your IT team can help ensure compliance with local security requirements

### 🖥️ Windows Users - How to Open
- Extract the ZIP file using File Explorer or WinRAR/7-Zip
- Navigate to the extracted folder and find BanffClass.exe
- When you double-click, you may see:
  - Windows protected your PC
  - Microsoft Defender SmartScreen prevented an unrecognized app from starting.
- To proceed:
  - Click on "More info" in the popup window
  - Then click "Run anyway"
- Alternatively, you can bypass the warning entirely:
  - Right-click on BanffClass.exe
  - Select Properties
  - At the bottom of the "General" tab, check: ☐ Unblock
- Click Apply and then OK
- Now double-click to run normally

### 🍎 macOS Users - How to Open
When you first try to open BanffClass on macOS: "BanffClass" cannot be opened because the developer cannot be verified. This is Gatekeeper protection, which verifies that apps come from trusted developers.

- Method 1: Right-Click Open (Recommended)
  - Find BanffClass.app in your extracted folder
  - Right-click on it and select Open
  - In the dialog box, click "Open" again
  - This allows you to open the app without changing system settings.

- Method 2: System Preferences Override
  - If right-click doesn't work:
  - Attempt to open the app once (which will likely fail).
  - Go to System Settings/Settings → Privacy & Security
  - Scroll down to the Security section
  - You'll see a message about BanffClass being blocked
  - Click "Open Anyway"

## 🔄 Updating BanffClass
The application includes an automatic update checker that notifies you when a new version is available.

### Update Process (Manual)
Since applications are unsigned, the auto-update feature only shows a notification - it doesn't install automatically. To update:

- Download the latest release from our [Releases page](https://github.com/bertrandchauveau/banffclass_local/releases/latest))
- Close BanffClass if it's running
- Replace the entire application folder with the new version:
  - Windows: Extract and replace BanffClass.exe (you can delete the old one or keep both versions side-by-side)
  - macOS: Move the old BanffClass.app to Trash, then extract the new one
- Repeat the installation steps for your OS:
  - Windows: May need to "Run anyway" again (or unblock properties)
  - macOS: Will need to right-click → Open or use System Settings override
- 💡 Tip: You don't lose any data when updating. BanffClass doesn't store patient data locally.


## 📄 License & Disclaimer
This software is provided for **educational and research purposes only**. It should not be used as the sole basis for clinical decisions. Please refer to the [official Banff classification documentation](https://banfffoundation.org/central-repository-for-banff-classification-resources-3/) for complete guidelines.

By using this application, you agree that:
- The developers are not responsible for any diagnostic errors
- You will verify all results manually in critical cases
- Your use of this software is at your own risk

## 📬 Contact
Dr. Bertrand Chauveau
- Email: bertrand.chauveau@chu-bordeaux.fr
- Department of Pathology, Bordeaux University Hospital

Prof. Maarten Naesens
- Email: maarten.naesens@kuleuven.be
- Department of Nephrology, University Hospitals Leuven

## 📝 How to Cite
BanffClass – an application for the classification of renal transplant biopsies. Bertrand Chauveau, Maarten Naesens. Version 0.1.0 (2026‑08‑25). Available at: https://github.com/bertrandchauveau/BanffClass

## ⚖️ Legal Notice
This software is not affiliated with or endorsed by the Banff Foundation. The Banff classification system is used under fair academic use guidelines.


Made with ❤️ for the kidney transplant community
