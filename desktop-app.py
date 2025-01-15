import tkinter as tk
from tkinter import ttk, filedialog
import sys
import os
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from tkcalendar import Calendar as TkCalendar

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("100-Day Savings Challenge")
        
        self.root.minsize(600, 450)  # Increased height to accommodate calendar
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 600) // 2
        y = (screen_height - 450) // 2
        self.root.geometry(f"600x450+{x}+{y}")

        # Store calendar data as instance variable
        self.current_calendar = None
        self.selected_date = datetime.now()

        def create_savings_calendar(start_date_str):
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

        def date_selected(event):
            """Handle date selection from calendar"""
            date = cal.selection_get()
            self.selected_date = date
            date_label.config(text=f"Selected Start Date: {date.strftime('%Y-%m-%d')}")

        def export_to_calendar():
            """Export weekly summaries to an ICS file."""
            if not self.current_calendar:
                result_text.insert(tk.END, "\nPlease generate a savings report first!")
                return

            cal = Calendar()
            cal.add('version', '2.0')
            cal.add('prodid', '-//100 Day Savings Challenge//example.com//')

            for monday, total in self.current_calendar['weekly_summaries'].items():
                event = Event()
                start_date = datetime.strptime(monday, '%Y-%m-%d')
                
                event.add('summary', f'Savings Goal: ${total:.2f}')
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
                    result_text.insert(tk.END, f"\nCalendar events saved successfully to {file_path}")
            except Exception as e:
                result_text.insert(tk.END, f"\nError saving calendar events: {str(e)}")

        def generate_report():
            """Generate and display the savings report"""
            start_date = self.selected_date.strftime('%Y-%m-%d')
            self.current_calendar = create_savings_calendar(start_date)
            
            report = "100-Day Savings Challenge Report\n"
            report += "=" * 40 + "\n\n"
            
            # Daily breakdown
            report += "Daily Savings:\n"
            report += "-" * 40 + "\n"
            for date, data in self.current_calendar['daily_savings'].items():
                report += f"{date} ({data['weekday']}): "
                report += f"Day {data['day_number']} - ${data['amount']:.2f}\n"
            
            # Weekly summaries
            report += "\nWeekly Summaries:\n"
            report += "-" * 40 + "\n"
            for monday, total in self.current_calendar['weekly_summaries'].items():
                report += f"Week starting {monday}: ${total:.2f}\n"
            
            # Total savings
            report += f"\nTotal Savings: ${self.current_calendar['total_savings']:.2f}\n"
            
            # Update the result text
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, report)

        # Create and pack widgets
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="100-Day Savings Challenge Calculator").pack(pady=5)

        # Add calendar widget
        cal = TkCalendar(main_frame, selectmode='day', date_pattern='y-mm-dd')
        cal.pack(pady=5)
        cal.bind('<<CalendarSelected>>', date_selected)

        # Add date label
        date_label = ttk.Label(main_frame, text=f"Selected Start Date: {datetime.now().strftime('%Y-%m-%d')}")
        date_label.pack(pady=5)

        # Button frame for multiple buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=5)
        
        # Generate Report button
        ttk.Button(button_frame, text="Generate Savings Report", command=generate_report).pack(side=tk.LEFT, padx=5)
        
        # Export Calendar button
        ttk.Button(button_frame, text="Export to Calendar", command=export_to_calendar).pack(side=tk.LEFT, padx=5)
        
        # Add a text widget to display the report
        result_text = tk.Text(main_frame, height=12, width=60)
        result_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=result_text.yview)
        scrollbar.pack(side="right", fill="y")
        result_text.configure(yscrollcommand=scrollbar.set)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.run()