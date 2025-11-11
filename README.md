# Weekend Trunk Shifts Scheduler

A Flask web application for managing weekend shift scheduling with preference-based allocation.

## Features

- **Employee Interface**: Employees can rank their top 12 preferred shifts and bottom 6 least wanted shifts
- **General Shift Preferences**: Rank shift types (Saturday 11-7, Sunday 8-4, Sunday 3-10)
- **Fair Allocation Algorithm**: Two-phase allocation ensuring equity
  - Phase 1: Random order, get everyone their first shift
  - Phase 2: Compensatory order based on Phase 1 satisfaction
- **Manager Dashboard**: View submissions, run allocation, export to Excel
- **60 Shifts**: 20 weekends × 3 shifts per weekend (Dec 13, 2025 - Apr 26, 2026)
- **30 Employees**: Pre-configured with employee1 through employee30

## Quick Start

### Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Access at `http://localhost:5000`

### Login Credentials

**Manager:**
- Username: `admin`
- Password: `admin123`

**Employees:**
- Username: `employee1` through `employee30`
- Password: `password`

## Deployment to Render.com

### Prerequisites
- GitHub account
- Render.com account (free)

### Steps

1. **Create a GitHub repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment

3. **Access your application**
   - Render will provide a URL like: `https://weekend-trunk-shifts.onrender.com`
   - Share this URL with employees

## File Structure

```
.
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── render.yaml                 # Render deployment configuration
├── templates/
│   ├── login.html             # Login page
│   ├── employee_dashboard.html # Employee shift selection interface
│   └── manager_dashboard.html  # Manager control panel
└── data/                       # Auto-created directory for JSON storage
    ├── employees.json         # Employee accounts
    ├── preferences.json       # Employee preferences
    ├── settings.json          # Deadline and lock status
    └── assignments.json       # Final shift assignments
```

## Usage Workflow

### For Employees

1. **Login** with your credentials
2. **Rank general shift preferences** (1-3)
3. **Select shifts**:
   - Click shifts to add to "Top 12" (first 12 clicks)
   - Continue clicking to add to "Bottom 6" (next 6 clicks)
   - Click again to remove a selection
4. **Submit preferences** before the deadline
5. **View assigned shifts** after manager runs allocation

### For Manager

1. **Login** with admin credentials
2. **Monitor submissions** - See who has submitted preferences
3. **Set/update deadline** for submissions
4. **Run allocation algorithm** once all employees have submitted
5. **Export to Excel** for distribution
6. **Download backup** (JSON) for data persistence

## Allocation Algorithm

The system uses a two-phase balanced allocation approach:

### Phase 1: First Shift
- Process employees in random order (seed=42 for reproducibility)
- Try to assign from employee's top 12 preferences
- Skip if: shift full, would create same-weekend conflict
- Fallback: Use shift type preference for non-bottom-6 shifts

### Phase 2: Second Shift
- Sort employees by Phase 1 satisfaction (worst assignments first)
- Randomize within same satisfaction level
- Same logic as Phase 1
- Ensures employees who got poor first shifts get priority for second

### Constraints
- Each employee gets exactly 2 shifts over 20 weeks
- No employee gets both shifts on the same weekend
- Bottom 6 preferences avoided unless no other option
- All 60 shifts must be filled (60 slots ÷ 30 employees × 2 = perfect match)

## Data Persistence

⚠️ **Important**: Render's free tier uses ephemeral storage, meaning data resets on app restart.

### Backup Strategy

1. **Regular backups**: Use "Download Backup" button to save JSON data
2. **Before shutdown**: Export Excel and download backup
3. **After restart**: You'll need to re-import data or restart preference collection

### For Production Use

Consider upgrading to:
- Render PostgreSQL database (free tier available)
- Persistent disk storage
- Or export data before each shutdown

## Customization

### Change Employee List

Edit `init_data_files()` in `app.py`:

```python
# Replace employee names
employee_names = ['Alice', 'Bob', 'Charlie', ...]
for name in employee_names:
    employees[name.lower()] = {
        'name': name,
        'is_manager': False,
        'password': generate_password_hash('password')
    }
```

### Change Schedule Dates

Edit `generate_shifts()` in `app.py`:

```python
start_date = datetime(2026, 1, 3)  # Change start date
for week in range(20):              # Change number of weekends
    ...
```

### Modify Shift Times

Edit the shift generation in `generate_shifts()`:

```python
# Saturday
shifts.append({
    'time': '11:00 AM - 7:00 PM',  # Change times here
    ...
})
```

## Troubleshooting

### App won't start on Render
- Check build logs for Python version compatibility
- Verify all dependencies are in `requirements.txt`
- Ensure `gunicorn` is installed

### Data disappears after restart
- Expected behavior on free tier
- Download regular backups
- Consider adding PostgreSQL database

### Allocation fails
- Verify all employees submitted complete preferences (12 top + 6 bottom)
- Check console logs for specific error messages
- Ensure no conflicts in shift availability

## Support

For issues or questions:
1. Check Render deployment logs
2. Review browser console for JavaScript errors
3. Verify JSON data files are properly formatted

## License

Internal use only - Reuters News
