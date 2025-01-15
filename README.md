# 100-Day Savings Challenge App - Deployment and Usage Guide

## For Developers: Deploying the App

### Prerequisites
Make sure you have the following installed:
```bash
pip3 install pyinstaller
pip3 install tkcalendar
pip3 install icalendar
pip3 install pytz
```

### Setting Up the Project
1. Create a new directory for your project:
```bash
mkdir 100-day-savings
cd 100-day-savings
```

2. Save the app code as `savings_app.py`

### Creating the Executable
1. Open Terminal and navigate to your project directory:
```bash
cd path/to/100-day-savings
```

2. Run PyInstaller with these options:
```bash
pyinstaller --onefile --windowed --name="Savings Calculator" savings_app.py
```

The flags mean:
- `--onefile`: Create a single executable file
- `--windowed`: Don't show Terminal when running
- `--name`: Set the name of the executable

### Finding the Executable
After PyInstaller completes:
1. Navigate to the `dist` folder in your project directory
2. You'll find `Savings Calculator.app` (Mac) or `Savings Calculator.exe` (Windows)

### Distribution
For Mac users:
1. Right-click on the .app file
2. Select "Compress"
3. Share the resulting zip file

For Windows users:
1. Zip the entire folder containing the .exe
2. Share the zip file

## For Users: Running the App

### Installation
1. Extract the zip file
2. For Mac:
   - Right-click "Savings Calculator.app"
   - Select "Open"
   - Click "Open" in the security dialog
3. For Windows:
   - Double-click "Savings Calculator.exe"

### Using the App

#### Setting a Start Date
1. Use the calendar widget to select your start date
2. The selected date appears below the calendar

#### Generating Your Savings Plan
1. Click "Generate Savings Report"
2. The report shows:
   - Daily savings amounts
   - Weekly summaries
   - Total savings goal

#### Exporting to Calendar
1. Click "Export to Calendar"
2. Choose where to save the .ics file
3. Import the .ics file into your calendar app:
   - Apple Calendar: Double-click the file
   - Google Calendar: Import through calendar settings
   - Outlook: Double-click or import through calendar menu

### Common Issues and Solutions

#### Mac Security Warning
If you see "app cannot be opened because it is from an unidentified developer":
1. Right-click the app
2. Select "Open"
3. Click "Open" in the dialog

#### Calendar Import Issues
If calendar events don't import:
1. Make sure the .ics file downloaded successfully
2. Try manually importing through your calendar app
3. Check if your calendar app supports .ics files

#### App Won't Start
1. Ensure all prerequisites are installed
2. Try running from a directory without spaces
3. Check system requirements:
   - Mac: macOS 10.14 or later
   - Windows: Windows 10 or later

## Technical Details

### File Structure
```
100-day-savings/
├── savings_app.py
├── build/
├── dist/
│   └── Savings Calculator.app
└── requirements.txt
```

### Requirements
```txt
tkcalendar==1.6.1
icalendar==5.0.7
pytz==2024.1
```

### Debugging
If needed, run the app from Terminal to see error messages:
```bash
./dist/Savings\ Calculator.app/Contents/MacOS/Savings\ Calculator
```

---
Version 1.0 - Last Updated: January 2025
