# Installing Python 3 and pip - Setup Guide

## For macOS Users

### Method 1: Using Homebrew (Recommended)
1. Install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Python 3 (includes pip3):
```bash
brew install python3
```

3. Verify installation:
```bash
python3 --version
pip3 --version
```

### Method 2: Direct Download
1. Go to [Python's official website](https://www.python.org/downloads/)
2. Click "Download Python 3.x.x for macOS"
3. Open the downloaded .pkg file
4. Follow installation wizard
5. Check "Install certificates.command" in the install process

## For Windows Users

### Step 1: Download Python
1. Visit [Python's official website](https://www.python.org/downloads/)
2. Click "Download Python 3.x.x"
3. Important: Check "Add Python 3.x to PATH" during installation

### Step 2: Installation
1. Run the downloaded .exe file
2. Select "Install Now" (recommended)
3. Wait for installation to complete
4. Click "Close" when finished

### Step 3: Verify Installation
1. Open Command Prompt (cmd)
2. Type:
```bash
python --version
pip --version
```

## Troubleshooting

### For macOS

#### Python Not Found
```bash
# Add to your ~/.zshrc or ~/.bash_profile:
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```

#### Pip Not Working
```bash
# Reinstall pip
python3 -m ensurepip --upgrade
```

### For Windows

#### 'Python' Not Recognized
1. System Properties → Advanced → Environment Variables
2. Edit Path
3. Add Python's installation directory
4. Add Python's Scripts directory

#### Pip Not Found
```bash
# In Command Prompt:
python -m ensurepip --upgrade
```

## Verifying Everything Works

### Test Python
1. Open Terminal (macOS) or Command Prompt (Windows)
2. Type:
```python
python3
print("Hello, World!")
exit()
```

### Test pip
```bash
pip3 list  # Shows installed packages
```

## Next Steps

After installation, install required packages:
```bash
pip3 install tkcalendar
pip3 install icalendar
pip3 install pytz
pip3 install pyinstaller
```

## Common Issues and Solutions

### Permission Errors
- macOS: Add `sudo` before commands
- Windows: Run Command Prompt as Administrator

### SSL Certificate Errors
```bash
# macOS:
open /Applications/Python\ 3.x/Install\ Certificates.command

# Windows:
python -m pip install --upgrade certifi
```

### Path Issues
Make sure to restart your terminal/command prompt after installation

## System Requirements

### macOS
- macOS 10.14 or later
- 2GB free disk space
- Admin privileges for installation

### Windows
- Windows 10 or later
- 2GB free disk space
- Admin privileges for installation

---
Note: Replace 3.x.x with the latest Python version available when downloading.
