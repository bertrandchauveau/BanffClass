# BanffClass - a Kidney Transplant Biopsy Classification Tool


BanffClass is a free desktop application designed to apply the Banff classification for kidney allograft pathology based on individual histological scores and clinico-biological parameters. It provides both rejection diagnoses and continuous indices in a user-friendly interface.

## 🚀 About
BanffClass is a desktop application that helps pathologists, nephrologists, and researchers apply the Banff classification for kidney transplant biopsies. The tool:
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
This application is **NOT meant for clinical use**. It is provided for **RESEARCH AND EDUCATIONAL purposes only**. Please refer to the [official Banff classification documentation](https://banfffoundation.org/central-repository-for-banff-classification-resources-3/) for complete guidelines.
By using this application, you agree to the License terms (available when launching the app) and that:
- The developers are not responsible for any diagnostic errors
- Your use of this software is at your own risk

## 📥 Installation
### System Requirements
- Windows: Windows 10 or later (64-bit)
- macOS: macOS Catalina (10.15) or later

### Downloading the Application
- Go to the [Releases page](https://github.com/bertrandchauveau/banffclass_local/releases/latest)
- Download the latest release for your operating system:
  - BanffClass-windows.zip (for Windows users)
  - BanffClass-macos.zip (for macOS users)
- Extract the ZIP file to a location of your choice

### 🛡️ Important Security Note
These applications are unsigned. This means that:

- Windows: You'll see a "Windows protected your PC" warning
- macOS: You'll encounter "Gatekeeper" warnings (see below)

This is normal and expected. Download only from [the release page](https://github.com/bertrandchauveau/BanffClass/releases) of this repository. 
Optionally verify the file against the SHA-256 checksum on the release page.

### For Institutional/Enterprise Devices
If you're installing this on an institutional or corporate device:

- Please check with your IT department first
- Your organization may have strict security policies regarding unsigned applications
- Some institutions require approval for any software installation
- Your IT team can help ensure compliance with local security requirements

### 🖥️ Windows
1. Download `BanffClass-windows.zip`.
2. Right-click the ZIP → Properties → tick **Unblock** at the bottom of the
   General tab → OK.
3. Extract the ZIP (File Explorer, 7-Zip, WinRAR), open the folder, and
   double-click `BanffClass.exe`.
4. If you still see "Windows protected your PC": click **More info**, then
   **Run anyway**.

Optional: move the app folder to a desired location and create a shortcut of BanffClass.exe

### 🍎 macOS
1. Download the macOS build, unzip it and move `BanffClass.app` to Applications.
2. Double-click it. You will see a warning; click **Done** (not "Move to
   Trash").
3. Open **System Settings → Privacy & Security**, scroll to **Security**,
   and click **Open Anyway** next to the BanffClass message.
4. Enter your password or Touch ID, then click **Open**.

## 🔄 Updating BanffClass
The application includes an automatic update checker that notifies you when a new version is available.

### Update Process (Manual)
Since applications are unsigned, the auto-update feature only shows a notification - it doesn't install automatically. To update:

- Download the latest release from our [Releases page](https://github.com/bertrandchauveau/banffclass_local/releases/latest)
- Close BanffClass if it's running
- Replace the entire application folder with the new version:
  - Windows: Extract and replace BanffClass.exe (you can delete the old one or keep both versions side-by-side)
  - macOS: Move the old BanffClass.app to Trash, then extract the new one
- Repeat the installation steps for your OS:
  - Windows: May need to "Run anyway" again (or unblock properties)
  - macOS: Will need to right-click → Open or use System Settings override
- 💡 Tip: You don't lose any data when updating. BanffClass doesn't store patient data locally.

## Usage instructions (.py script)
To use BanffClass outside of the application via scripting, see banff_single.py. Input variables should be provided as a dictionary following the specifications below (otherwise, use np.nan):
- **g**, **ptc**, **i**, **t**, **v**, **ci**, **ct**, **ti**, **i-IFTA**, **t-IFTA**: corresponding Banff scores, from 0 to 3
- **cg**: cg Banff score, from 0 to 3 (1a/1b => 1)
- **C4d**: **C4d score as a binary variable 0/1**. It is up to you to binarize the C4d Banff score from 0 to 3 into 0/1 based on your technics (immunofluorescence positive if Banff score > 1, chromogenic IHC positive if Banff score > 0).
- **pvl**: pvl Banff score, from 0 to 3
- **TMA**: binary variable 0/1, 1 if histological lesions of thrombotic microangiopathy are observed
- **ATI**: binary variable 0/1, 1 if histological acute tubular injury is present
- **ptcml**: binary variable 0/1, 1 if severe peritubular capillary basement membrane multilayering is present by electron microscopy
- **current DSA**: binary variable 0/1, 1 if presence of DSA in the serum at time of the biopsy
- **historical DSA**: binary variable 0/1, 1 if anteriority of DSA detection
- **historical AMR**: binary variable 0/1, 1 if anteriority of AMR
- **transcripts MVI**: binary variable 0/1, 1 if tissue transcriptomics is in favor of an MVI/AMR-related diagnosis
- **transcripts TI**: binary variable 0/1, 1 if tissue transcriptomics is in favor of an tubulo-interstitial/TCMR-related diagnosis
- **infection**: binary variable 0/1, 1 if presence of an infection-related nephritis. Will be automatically set to 1 if pvl is > 0.
- **recurrent/de novo GN**: binary variable 0/1, 1 if presence of recurrent or de novo glomerulonephritis.
- **chronic transplant arteriopathy**: binary variable 0/1, 1 if presence of “chronic allograft arteriopathy” is present (arterial intimal fibrosis with mononuclear cell infiltration in fibrosis, and formation of neointima).
- **ABOi**: binary variable 0/1, 1 if current transplantation is in a ABO incompatible context

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

The source code in this repository is licensed under the GNU Affero General
Public License v3.0 or later. The AGPL does not grant any rights
to the name "BanffClass" or to the project logo, which remain the property of
KU Leuven (Maarten Naesens) and University of Bordeaux (Bertrand Chauveau).

- You may redistribute the **unmodified** official releases, provided you keep
  the name, the version number and this notice intact.
- You may fork, modify and redistribute the source code under the AGPL, but a
  modified version **must not** be distributed under the name "BanffClass" or
  with our logo, and must not suggest that it is the official version or is
  endorsed by the authors and their institution.
- Modified versions must state clearly that they are modified and who modified
  them, in the software and its documentation.

Official releases are published only in this repository, with SHA-256
checksums. Builds obtained elsewhere are not guaranteed to be authentic.

Made with ❤️ for the kidney transplant community
