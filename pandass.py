import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Load the Excel file
excel_file = pd.ExcelFile('May_June_25.xlsx')  # Replace with the actual path
print(excel_file.sheet_names)  # Print the sheet names
df = excel_file.parse('Sheet1')  # Replace with the name of your sheet

# Convert the date column to datetime
df['dt'] = pd.to_datetime(df['dt'])

# Filter for Apr 20 to April 30, 2025
start_date = pd.to_datetime('2025-04-20')
end_date = pd.to_datetime('2025-04-30')
df = df[(df['dt'] >= start_date) & (df['dt'] <= end_date)]

# Check if DataFrame is empty after date filtering
if df.empty:
    print("Warning: No data found for March 1 to April 30, 2025. Check the 'dt' column dates.")
    print("Available dates:", df['dt'].dt.date.unique())
else:
    print("Data filtered for April 20 to April 30, 2025. Number of rows:", len(df))

# Create a single plot
fig, ax = plt.subplots()

# Loop through LCP columns (62 only, adjust range as needed)
for i in range(54, 56):
    gate = f'Gate {i}'
    if gate in df.columns:  # Check if the column exists
        # Calculate absolute differences between consecutive rows
        diff = df[gate].diff().abs()
        # Mask: Include first row (diff is NaN) or diff in [0.2, 2]
        mask = (diff.isna()) | ((diff >= 0.2) & (diff <= 2))
        # Optional: Add filter for LCP62 <= 10
        # mask = mask & (df[gate] <= 10)
        
        # Plot filtered data
        ax.plot(df['dt'][mask], df[gate][mask], label=gate, marker='o', markersize=3)
        print(f"Plotted {gate} with {mask.sum()} points after filtering.")

# Formatting the x-axis to show dates correctly
date_format = mdates.DateFormatter('%m-%d %H:%M')  # Omit year since all data is 2025
ax.xaxis.set_major_formatter(date_format)

# Rotate date labels for better readability
fig.autofmt_xdate()

# Add labels and legend
ax.set_xlabel('DateTime (March-April 2025)')
ax.set_ylabel('LCP')
ax.set_title('Gate Opening vs DateTime (March 1 - April 30, 2025)')
ax.legend()  # Add a legend to distinguish the lines

# Show the plot
plt.show()