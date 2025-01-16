import tkinter as tk
from tkinter import ttk, filedialog
import sys
import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from tkcalendar import Calendar as TkCalendar
from tkinter.font import Font

class ModernTheme:
    # Modern color palette
    PRIMARY_COLOR = "#2962FF"  # Deep blue
    SECONDARY_COLOR = "#82B1FF"  # Light blue
    BACKGROUND_COLOR = "#F5F5F7"  # Light gray
    SURFACE_COLOR = "#FFFFFF"  # White
    TEXT_COLOR = "#1D1D1F"  # Near black
    ACCENT_COLOR = "#FF3D00"  # Orange accent
    
    # Font configurations
    TITLE_FONT = ("SF Pro Display", 24, "bold")
    HEADING_FONT = ("SF Pro Display", 16, "bold")
    BODY_FONT = ("SF Pro Text", 12)
    BUTTON_FONT = ("SF Pro Text", 12, "bold")

    @classmethod
    def apply_theme(cls):
        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TFrame": {
                "configure": {
                    "background": cls.BACKGROUND_COLOR
                }
            },
            "TLabel": {
                "configure": {
                    "background": cls.BACKGROUND_COLOR,
                    "foreground": cls.TEXT_COLOR,
                    "padding": (10, 5)
                }
            },
            "TButton": {
                "configure": {
                    "background": cls.PRIMARY_COLOR,
                    "foreground": cls.SURFACE_COLOR,
                    "padding": (20, 10),
                    "font": cls.BUTTON_FONT
                },
                "map": {
                    "background": [("active", cls.SECONDARY_COLOR)],
                    "foreground": [("active", cls.TEXT_COLOR)]
                }
            },
            "Vertical.TScrollbar": {
                "configure": {
                    "background": cls.BACKGROUND_COLOR,
                    "troughcolor": cls.SURFACE_COLOR,
                    "width": 16
                }
            }
        })
        style.theme_use("modern")

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("100-Day Savings Challenge")
        self.root.minsize(1000, 800)
        
        # Apply modern theme
        ModernTheme.apply_theme()
        
        # Configure root window
        self.root.configure(bg=ModernTheme.BACKGROUND_COLOR)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 800) // 2
        self.root.geometry(f"1000x800+{x}+{y}")

        # Store calendar data
        self.current_calendar = None
        self.selected_date = datetime.now()

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Title section
        title_label = ttk.Label(
            main_frame,
            text="100-Day Savings Challenge",
            font=ModernTheme.TITLE_FONT,
            foreground=ModernTheme.PRIMARY_COLOR
        )
        title_label.pack(pady=(0, 30))

        # Create two-column layout
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Calendar
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Customize calendar appearance
        cal_style = ttk.Style()
        cal_style.configure(
            'Calendar.TFrame',
            background=ModernTheme.SURFACE_COLOR
        )
        
        self.calendar = TkCalendar(
            left_frame,
            selectmode='day',
            date_pattern='y-mm-dd',
            font=ModernTheme.BODY_FONT,
            selectforeground=ModernTheme.SURFACE_COLOR,
            selectbackground=ModernTheme.PRIMARY_COLOR,
            background=ModernTheme.SURFACE_COLOR,
            foreground=ModernTheme.TEXT_COLOR,
            headersbackground=ModernTheme.SECONDARY_COLOR,
            headersforeground=ModernTheme.SURFACE_COLOR,
            borderwidth=0,
            weekendbackground=ModernTheme.BACKGROUND_COLOR,
            weekendforeground=ModernTheme.TEXT_COLOR,
            othermonthwebackground=ModernTheme.BACKGROUND_COLOR,
            othermonthweforeground='#999999'
        )
        self.calendar.pack(fill=tk.BOTH, expand=True)
        self.calendar.bind('<<CalendarSelected>>', self.date_selected)

        # Selected date label
        self.date_label = ttk.Label(
            left_frame,
            font=ModernTheme.HEADING_FONT,
            foreground=ModernTheme.PRIMARY_COLOR
        )
        self.date_label.pack(pady=20)
        self.update_date_label()

        # Right column - Report and Controls
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(15, 0))

        # Button container
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))

        # Modern styled buttons
        generate_btn = ttk.Button(
            button_frame,
            text="Generate Report",
            command=self.generate_report,
            style='Modern.TButton'
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))

        export_btn = ttk.Button(
            button_frame,
            text="Export Calendar",
            command=self.export_to_calendar,
            style='Modern.TButton'
        )
        export_btn.pack(side=tk.LEFT)

        # Report text area with modern styling
        self.result_text = tk.Text(
            right_frame,
            font=ModernTheme.BODY_FONT,
            bg=ModernTheme.SURFACE_COLOR,
            fg=ModernTheme.TEXT_COLOR,
            relief="flat",
            padx=15,
            pady=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Modern scrollbar
        scrollbar = ttk.Scrollbar(
            right_frame,
            orient="vertical",
            command=self.result_text.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.result_text.configure(yscrollcommand=scrollbar.set)

    def update_date_label(self):
        self.date_label.config(
            text=f"Selected Start Date: {self.selected_date.strftime('%B %d, %Y')}"
        )

    def date_selected(self, event):
        self.selected_date = self.calendar.selection_get()
        self.update_date_label()

    def generate_report(self):
        start_date = self.selected_date.strftime('%Y-%m-%d')
        self.current_calendar = self.create_savings_calendar(start_date)
        
        report = "📊 Savings Challenge Report\n"
        report += "═" * 40 + "\n\n"
        
        # Daily breakdown
        report += "📅 Daily Savings:\n"
        report += "─" * 40 + "\n"
        for date, data in self.current_calendar['daily_savings'].items():
            report += f"📍 {date} ({data['weekday']}): "
            report += f"Day {data['day_number']} - ${data['amount']:.2f}\n"
        
        # Weekly summaries
        report += "\n📆 Weekly Summaries:\n"
        report += "─" * 40 + "\n"
        for monday, total in self.current_calendar['weekly_summaries'].items():
            report += f"📅 Week starting {monday}: ${total:.2f}\n"
        
        # Total savings
        report += f"\n💰 Total Savings: ${self.current_calendar['total_savings']:.2f}\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, report)

    def create_savings_calendar(self, start_date_str):
        """Creates a 100-day savings calendar with weekly summaries on Mondays."""
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        calendar = {
            'daily_savings': {},
            'weekly_summaries': {},
            'total_savings': 0
        }
        
        current_week_sum = 0
        last_monday = None
        
        for day in range(100):
            current_date = start_date + timedelta(days=day)
            amount = day + 1
            
            date_str = current_date.strftime('%Y-%m-%d')
            calendar['daily_savings'][date_str] = {
                'day_number': day + 1,
                'amount': amount,
                'weekday': current_date.strftime('%A')
            }
            
            current_week_sum += amount
            calendar['total_savings'] += amount
            
            if current_date.weekday() == 0:
                last_monday = date_str
                calendar['weekly_summaries'][date_str] = 0
                
            if last_monday:
                calendar['weekly_summaries'][last_monday] = current_week_sum
                
            if current_date.weekday() == 6:
                current_week_sum = 0

        return calendar

    def export_to_calendar(self):
        if not self.current_calendar:
            self.result_text.insert(tk.END, "\n⚠️ Please generate a savings report first!")
            return

        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//100 Day Savings Challenge//example.com//')

        for monday, total in self.current_calendar['weekly_summaries'].items():
            event = Event()
            start_date = datetime.strptime(monday, '%Y-%m-%d')
            
            event.add('summary', f'💰 Savings Goal: ${total:.2f}')
            event.add('description', f'Weekly savings target: ${total:.2f}\nPart of your 100-day savings challenge!')
            event.add('dtstart', start_date.date())
            event.add('dtend', (start_date + timedelta(days=1)).date())
            event.add('dtstamp', datetime.now(pytz.UTC))
            
            cal.add_component(event)

        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".ics",
                filetypes=[("Calendar files", "*.ics")],
                title="Save Calendar Events"
            )
            
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(cal.to_ical())
                self.result_text.insert(tk.END, f"\n✅ Calendar events saved successfully to {file_path}")
        except Exception as e:
            self.result_text.insert(tk.END, f"\n❌ Error saving calendar events: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()