"""
Populate Weekend Trunk Writer application with actual employee names
"""
import json
from werkzeug.security import generate_password_hash
import os

# Trunk writers from WEEKEND TRUNKWRITER ROTATION.docx
# Format: (Last name, First name, email prefix)
trunk_writers = [
    ("Ali", "Idrees", "Idrees.Ali"),
    ("Allen", "Jonathan", "jonathan.allen"),
    ("Alper", "Alexandra", "Alexandra.Alper"),
    ("Ax", "Joseph A.", "Joseph.Ax"),
    ("Brooks", "Brad", "Brad.Brooks"),
    ("Brunnstrom", "David R.", "David.Brunnstrom"),
    ("Coster", "Helen A.", "helen.coster"),
    ("Cowan", "Richard J.", "Richard.Cowan"),
    ("Erickson", "Bo", "BO.ERICKSON"),
    ("Gorman", "Steve J.", "steve.gorman"),
    ("Goudsward", "Andrew", "Andrew.Goudsward"),
    ("Harte", "Julia", "Julia.Harte"),
    ("Heath", "Brad", "Brad.Heath"),
    ("Heavey", "Susan", "SHeavey"),
    ("Hesson", "Ted", "Ted.Hesson"),
    ("Kruzel", "John", "John.Kruzel"),
    ("Lawder", "David", "David.Lawder"),
    ("Layne", "Nathan", "Nathan.Layne"),
    ("Lewis", "Simon", "simon.lewis"),
    ("Martina", "Michael", "michael.martina"),
    ("Morgan", "David G.", "david.morgan"),
    ("Oliphant", "Jim", "james.oliphant"),
    ("Reid", "Timothy J.", "tim.reid"),
    ("Satter", "Raphael", "Raphael.Satter"),
    ("Spetalnick", "Matt S.", "matt.spetalnick"),
    ("Stewart", "Phillip", "Phillip.Stewart"),
    ("Sullivan", "Andy", "Andy.Sullivan"),
    ("Tanfani", "Joseph", "Joseph.Tanfani"),
    ("Trotta", "Daniel", "DANIEL.TROTTA"),
    ("Zengerle", "Patricia A.", "patricia.zengerle"),
]

# Sort by last name
trunk_writers.sort(key=lambda x: x[0])

# Create employees dictionary
employees = {}

# Manager account
employees['admin'] = {
    'name': 'Admin',
    'is_manager': True,
    'password': generate_password_hash('admin123')
}

# Add trunk writers
for last_name, first_name, email_prefix in trunk_writers:
    # Use email prefix (before @) as username
    username = email_prefix.lower()
    
    # Display name format: "Last, First"
    display_name = f"{last_name}, {first_name}"
    
    employees[username] = {
        'name': display_name,
        'is_manager': False,
        'password': generate_password_hash('password')
    }

# Save to data directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

output_file = os.path.join(data_dir, 'employees.json')
with open(output_file, 'w') as f:
    json.dump(employees, f, indent=2)

print(f"✓ Created {len(trunk_writers)} trunk writer accounts")
print(f"✓ Saved to: {output_file}")
print(f"\nManager login:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"\nEmployee login (all trunk writers):")
print(f"  Username: [email prefix before @]")
print(f"  Password: password")
print(f"\nExample logins:")
print(f"  Username: idrees.ali")
print(f"  Username: jonathan.allen")
print(f"  Username: andy.sullivan")
print(f"\nEmployees sorted alphabetically by last name in manager dashboard:")
for i, (last_name, first_name, email_prefix) in enumerate(trunk_writers[:5], 1):
    print(f"  {i}. {last_name}, {first_name} (username: {email_prefix.lower()})")
print(f"  ...")
