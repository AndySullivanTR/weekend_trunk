"""
Analyze allocation results - see how well employees did
Shows which employees got their top choices vs. who got screwed
"""

import json
from collections import defaultdict

# Load data
with open('data/employees.json', 'r') as f:
    employees = json.load(f)

with open('data/preferences.json', 'r') as f:
    preferences = json.load(f)

with open('data/assignments.json', 'r') as f:
    assignments = json.load(f)

print("="*80)
print("ALLOCATION RESULTS ANALYSIS")
print("="*80)

# Analyze each employee
employee_results = []

for emp in sorted(assignments.keys()):
    if emp not in employees or employees[emp].get('is_manager'):
        continue
    
    emp_name = employees[emp]['name']
    emp_prefs = preferences.get(emp, {})
    emp_shifts = assignments.get(emp, [])
    
    top_12 = emp_prefs.get('top_12', [])
    bottom_6 = emp_prefs.get('bottom_6', [])
    
    # Calculate ranks for each assigned shift
    shift_ranks = []
    got_top_12 = 0
    got_bottom_6 = 0
    
    for shift_id in emp_shifts:
        if shift_id in top_12:
            rank = top_12.index(shift_id) + 1
            shift_ranks.append(rank)
            got_top_12 += 1
        elif shift_id in bottom_6:
            rank = 'BOTTOM-6'
            shift_ranks.append(rank)
            got_bottom_6 += 1
        else:
            shift_ranks.append('NOT-RANKED')
    
    # Calculate satisfaction score (average rank for top-12 assignments)
    numeric_ranks = [r for r in shift_ranks if isinstance(r, int)]
    avg_rank = sum(numeric_ranks) / len(numeric_ranks) if numeric_ranks else 999
    
    employee_results.append({
        'name': emp_name,
        'shifts': len(emp_shifts),
        'ranks': shift_ranks,
        'avg_rank': avg_rank,
        'top_12_count': got_top_12,
        'bottom_6_count': got_bottom_6,
        'got_screwed': got_bottom_6 > 0 or len(numeric_ranks) == 0
    })

# Sort by satisfaction (best first)
employee_results.sort(key=lambda x: x['avg_rank'])

print("\n" + "="*80)
print("EMPLOYEE RESULTS (Best to Worst)")
print("="*80)
print(f"{'Employee':<15} {'Shifts':<8} {'Ranks':<25} {'Avg Rank':<10} {'Status'}")
print("-"*80)

for result in employee_results:
    ranks_str = ', '.join([f"#{r}" if isinstance(r, int) else str(r) for r in result['ranks']])
    avg_str = f"{result['avg_rank']:.1f}" if result['avg_rank'] < 999 else "N/A"
    
    # Status
    if result['bottom_6_count'] > 0:
        status = "😢 GOT BOTTOM-6"
    elif result['top_12_count'] == 2:
        if result['avg_rank'] <= 3:
            status = "😊 GREAT"
        elif result['avg_rank'] <= 6:
            status = "🙂 GOOD"
        else:
            status = "😐 OK"
    else:
        status = "⚠️  INCOMPLETE"
    
    print(f"{result['name']:<15} {result['shifts']:<8} {ranks_str:<25} {avg_str:<10} {status}")

# Summary statistics
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

total_employees = len(employee_results)
fully_assigned = sum(1 for r in employee_results if r['shifts'] == 2)
got_both_top_12 = sum(1 for r in employee_results if r['top_12_count'] == 2)
got_one_top_12 = sum(1 for r in employee_results if r['top_12_count'] == 1)
got_bottom_6 = sum(1 for r in employee_results if r['bottom_6_count'] > 0)

print(f"Total Employees:           {total_employees}")
print(f"Fully Assigned (2 shifts): {fully_assigned} ({fully_assigned/total_employees*100:.1f}%)")
print(f"Got Both from Top 12:      {got_both_top_12} ({got_both_top_12/total_employees*100:.1f}%)")
print(f"Got One from Top 12:       {got_one_top_12} ({got_one_top_12/total_employees*100:.1f}%)")
print(f"Got Bottom-6 Shift:        {got_bottom_6} ({got_bottom_6/total_employees*100:.1f}%)")

# Rank distribution
rank_counts = defaultdict(int)
for result in employee_results:
    for rank in result['ranks']:
        if isinstance(rank, int):
            if rank <= 3:
                rank_counts['Top 3'] += 1
            elif rank <= 6:
                rank_counts['4-6'] += 1
            elif rank <= 9:
                rank_counts['7-9'] += 1
            else:
                rank_counts['10-12'] += 1
        elif rank == 'BOTTOM-6':
            rank_counts['Bottom 6'] += 1
        else:
            rank_counts['Not Ranked'] += 1

print(f"\nRank Distribution (60 total shifts assigned):")
for rank_range, count in sorted(rank_counts.items()):
    print(f"  {rank_range}: {count} shifts")

# Average satisfaction
all_numeric_ranks = [r for result in employee_results for r in result['ranks'] if isinstance(r, int)]
overall_avg = sum(all_numeric_ranks) / len(all_numeric_ranks) if all_numeric_ranks else 0

print(f"\nOverall Average Rank: {overall_avg:.2f} (lower is better)")

print("\n" + "="*80)
print("WHO GOT SCREWED?")
print("="*80)

screwed_employees = [r for r in employee_results if r['got_screwed']]
if screwed_employees:
    for result in screwed_employees:
        ranks_str = ', '.join([f"#{r}" if isinstance(r, int) else str(r) for r in result['ranks']])
        print(f"😢 {result['name']:<15} got: {ranks_str}")
else:
    print("✅ Nobody got screwed! Everyone got at least one shift from their top 12.")

print("\n" + "="*80)
print("TOP PERFORMERS (Best average ranks)")
print("="*80)

top_5 = employee_results[:5]
for i, result in enumerate(top_5, 1):
    ranks_str = ', '.join([f"#{r}" if isinstance(r, int) else str(r) for r in result['ranks']])
    print(f"{i}. {result['name']:<15} Avg: {result['avg_rank']:.1f}  Got: {ranks_str}")

print("\n" + "="*80)
