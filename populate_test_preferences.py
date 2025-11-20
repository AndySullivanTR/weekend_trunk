""" 
Generate random preferences for all employees
This populates the preferences.json file for testing the allocation algorithm
"""

import json
import random

# Path to files
EMPLOYEES_FILE = 'data/employees.json'
PREFS_FILE = 'data/preferences.json'

# Load existing employees
with open(EMPLOYEES_FILE, 'r') as f:
    employees = json.load(f)

# Get non-manager employee usernames
employee_usernames = [username for username, emp in employees.items() if not emp.get('is_manager')]

print(f"Found {len(employee_usernames)} employees")

# All 60 shift IDs (0-59)
all_shifts = list(range(60))

# Generate random preferences for each employee
preferences = {}

for username in employee_usernames:
    
    # Shuffle all shifts
    shuffled = all_shifts.copy()
    random.shuffle(shuffled)
    
    # Top 12 are first 12 from shuffled list
    top_12 = shuffled[:12]
    
    # Bottom 6 are next 6 from shuffled list (ensuring no overlap)
    bottom_6 = shuffled[12:18]
    
    # Random shift type preferences (1, 2, 3)
    shift_types = [1, 2, 3]
    random.shuffle(shift_types)
    
    preferences[username] = {
        'top_12': top_12,
        'bottom_6': bottom_6,
        'shift_type_pref': {
            'saturday': str(shift_types[0]),
            'sunday_morning': str(shift_types[1]),
            'sunday_evening': str(shift_types[2])
        }
    }

# Save to file
with open(PREFS_FILE, 'w') as f:
    json.dump(preferences, f, indent=2)

print(f"✅ Generated random preferences for {len(preferences)} employees")
print(f"✅ Saved to {PREFS_FILE}")
print(f"\nYou can now:")
print(f"1. Restart Flask app (or just refresh browser)")
print(f"2. Login as admin/admin123")
print(f"3. Click 'Assign Shifts'")
print(f"4. Check the results and export to Excel")
