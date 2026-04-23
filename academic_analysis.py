import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Styling ────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
})
PALETTE = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0', '#FF9800', '#00BCD4']
PASS_COLOR = '#4CAF50'
FAIL_COLOR = '#F44336'
NEUTRAL_COLOR = '#2196F3'

# ── Raw Data ───────────────────────────────────────────────────────────────
records = [
    # (cal_year, study_year, semester_num, semester_label, course, code, marks, pass_fail)
    (2021, 'Year 1', 1, 'Y1-S1', 'Introduction to Computing',          'ICG',  61, 'Pass'),
    (2021, 'Year 1', 1, 'Y1-S1', 'Design Thinking',                    'DST',  60, 'Pass'),
    (2021, 'Year 1', 1, 'Y1-S1', 'Database Fundamentals',              'DBF',  53, 'Pass'),
    (2021, 'Year 1', 1, 'Y1-S1', 'Math for Computing 1',               'MCI',  55, 'Pass'),
    (2021, 'Year 1', 1, 'Y1-S1', 'Business Management Info Systems',   'BMC',  57, 'Pass'),
    (2021, 'Year 1', 2, 'Y1-S2', 'Database Programming',               'DGP',  50, 'Pass'),
    (2021, 'Year 1', 2, 'Y1-S2', 'Computer Organisation & Architecture','COA', 56, 'Pass'),
    (2021, 'Year 1', 2, 'Y1-S2', 'Data Structures & Algorithm 1',      'DSA1', 50, 'Pass'),
    (2021, 'Year 1', 2, 'Y1-S2', 'Math for Computing 2',               'MCI2', 70, 'Pass'),
    (2021, 'Year 1', 2, 'Y1-S2', 'Programming 1',                      'PRG1', 61, 'Pass'),
    # 2022 – first attempt at Sem 3 & 4
    (2022, 'Year 2', 3, 'Y2-S3a','Applied Statistics & Probability',   'ASP',  36, 'Fail'),
    (2022, 'Year 2', 3, 'Y2-S3a','Data Networks',                      'DTN',  None,'Fail'),
    (2022, 'Year 2', 3, 'Y2-S3a','Information System Security',        'ISS',  57, 'Pass'),
    (2022, 'Year 2', 3, 'Y2-S3a','Operating Systems',                  'OPS',  50, 'Pass'),
    (2022, 'Year 2', 3, 'Y2-S3a','Programming 2',                      'PRG2', 30, 'Fail'),
    (2022, 'Year 2', 3, 'Y2-S3a','English for Academic Purposes',      'EAP',  50, 'Pass'),
    (2022, 'Year 2', 4, 'Y2-S4a','Ethics for Computing',               'EFC',  60, 'Pass'),
    (2022, 'Year 2', 4, 'Y2-S4a','Innovation Creativity & Entre',      'ICE',  34, 'Fail'),
    # 2023 – retakes + new modules
    (2023, 'Year 2', 3, 'Y2-S3b','Applied Statistics & Probability',   'ASP',  58, 'Pass'),
    (2023, 'Year 2', 3, 'Y2-S3b','Data Networks',                      'DTN',  None,'Fail'),
    (2023, 'Year 2', 3, 'Y2-S3b','Programming 2',                      'PRG2', 16, 'Fail'),
    (2023, 'Year 2', 4, 'Y2-S4b','Data Analytics',                     'DTA',  52, 'Pass'),
    (2023, 'Year 2', 4, 'Y2-S4b','Innovation Creativity & Entre',      'ICE',  66, 'Pass'),
    # 2024 – Year 3
    (2024, 'Year 3', 5, 'Y3-S5', 'Data Structures & Algorithm 2',      'DSA2', 74, 'Pass'),
    (2024, 'Year 3', 5, 'Y3-S5', 'Software Processes',                 'SPS',  53, 'Pass'),
    (2024, 'Year 3', 5, 'Y3-S5', 'Software Verification & Validation', 'SVV',  28, 'Fail'),
    (2024, 'Year 3', 5, 'Y3-S5', 'Programming 2',                      'PRG2', 75, 'Pass'),
    (2024, 'Year 3', 6, 'Y3-S6', 'Project Management for IT',          'PTM',  66, 'Pass'),
    (2024, 'Year 3', 6, 'Y3-S6', 'Sustainability & Development',        'SYD', 68, 'Pass'),
    (2024, 'Year 3', 6, 'Y3-S6', 'Web Development',                    'WAD',  63, 'Pass'),
    (2024, 'Year 3', 6, 'Y3-S6', 'Distributed Systems & Applications', 'DSA',  62, 'Pass'),
    # 2025 – Year 4
    (2025, 'Year 4', 7, 'Y4-S7', 'Artificial Intelligence',            'ARI',  65, 'Pass'),
    (2025, 'Year 4', 7, 'Y4-S7', 'Compiler Techniques',                'CTE',  73, 'Pass'),
    (2025, 'Year 4', 7, 'Y4-S7', 'Mobile Application Development',     'MAP',  53, 'Pass'),
    (2025, 'Year 4', 7, 'Y4-S7', 'Data Networks',                      'DTN',  38, 'Fail'),
    (2025, 'Year 4', 7, 'Y4-S7', 'Software Verification & Validation', 'SVV',  60, 'Pass'),
]

cols = ['Cal_Year', 'Study_Year', 'Sem_Num', 'Sem_Label', 'Course', 'Code', 'Marks', 'Result']
df = pd.DataFrame(records, columns=cols)
df_graded = df[df['Marks'].notna()].copy()  # exclude N/A marks rows

# ── Derived columns ────────────────────────────────────────────────────────
def grade_letter(m):
    if pd.isna(m): return 'N/A'
    if m >= 75: return 'A'
    if m >= 65: return 'B'
    if m >= 55: return 'C'
    if m >= 50: return 'D'
    return 'F'

df_graded['Grade'] = df_graded['Marks'].apply(grade_letter)
df_graded['Passed'] = df_graded['Result'] == 'Pass'

# ── Summary stats ──────────────────────────────────────────────────────────
print("=" * 60)
print("  SHAPOPI PHELLEP — ACADEMIC ANALYSIS REPORT")
print("  NUST | BSc Computer Science (Software Development)")
print("=" * 60)

total = len(df)
graded = len(df_graded)
passed = df_graded['Passed'].sum()
failed = (~df_graded['Passed']).sum()
avg = df_graded['Marks'].mean()
median = df_graded['Marks'].median()
best_mark = df_graded['Marks'].max()
best_course = df_graded.loc[df_graded['Marks'].idxmax(), 'Course']
worst_mark = df_graded['Marks'].min()
worst_course = df_graded.loc[df_graded['Marks'].idxmin(), 'Course']

print(f"\nOverall Modules Attempted : {total}")
print(f"Modules with Final Marks  : {graded}")
print(f"Pass / Fail               : {passed} / {failed}")
print(f"Pass Rate                 : {100*passed/graded:.1f}%")
print(f"Mean Mark                 : {avg:.1f}%")
print(f"Median Mark               : {median:.1f}%")
print(f"Highest Mark              : {best_mark}% — {best_course}")
print(f"Lowest Mark               : {worst_mark}% — {worst_course}")

print("\nBy Study Year:")
for yr in ['Year 1', 'Year 2', 'Year 3', 'Year 4']:
    sub = df_graded[df_graded['Study_Year'] == yr]
    if len(sub):
        pr = 100 * sub['Passed'].sum() / len(sub)
        print(f"  {yr}: avg={sub['Marks'].mean():.1f}%  pass={pr:.0f}%  n={len(sub)}")

print("\nRetaken Modules:")
retakes = df.groupby('Code').filter(lambda g: len(g) > 1)
for code in retakes['Code'].unique():
    rows = df[df['Code'] == code][['Cal_Year', 'Marks', 'Result']].values
    attempts = ' -> '.join(
        f"{r[0]}: {r[1] if r[1] else 'N/A'} ({r[2]})" for r in rows
    )
    print(f"  {code}: {attempts}")

# ── CHART 1: Marks per Course (all attempts) ───────────────────────────────
fig, ax = plt.subplots(figsize=(14, 6))
colors = [PASS_COLOR if r == 'Pass' else FAIL_COLOR for r in df_graded['Result']]
labels = [f"{r['Code']}\n{r['Cal_Year']}" for _, r in df_graded.iterrows()]
bars = ax.bar(range(len(df_graded)), df_graded['Marks'], color=colors, edgecolor='white', linewidth=0.5)
ax.set_xticks(range(len(df_graded)))
ax.set_xticklabels(labels, fontsize=7, rotation=45, ha='right')
ax.axhline(50, color='gray', linestyle='--', linewidth=1, label='Pass mark (50%)')
ax.axhline(avg, color=NEUTRAL_COLOR, linestyle=':', linewidth=1.5, label=f'Overall avg ({avg:.1f}%)')
ax.set_ylim(0, 100)
ax.set_ylabel('Final Mark (%)')
ax.set_title('Final Marks — All Modules (All Attempts)', fontsize=13, fontweight='bold')
pass_patch = mpatches.Patch(color=PASS_COLOR, label='Pass')
fail_patch = mpatches.Patch(color=FAIL_COLOR, label='Fail')
ax.legend(handles=[pass_patch, fail_patch] + ax.get_legend_handles_labels()[0][2:])
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart1_all_marks.png')
plt.close()
print("\n[Saved] chart1_all_marks.png")

# ── CHART 2: Average Mark by Study Year ───────────────────────────────────
year_stats = df_graded.groupby('Study_Year').agg(
    avg_mark=('Marks', 'mean'),
    pass_rate=('Passed', lambda x: 100 * x.mean()),
    n=('Marks', 'count')
).reset_index()

fig, ax1 = plt.subplots(figsize=(8, 5))
x = np.arange(len(year_stats))
bars = ax1.bar(x, year_stats['avg_mark'], color=PALETTE[:len(year_stats)], alpha=0.85, width=0.5)
ax1.set_xticks(x)
ax1.set_xticklabels(year_stats['Study_Year'])
ax1.set_ylabel('Average Mark (%)')
ax1.set_ylim(0, 100)
ax1.axhline(50, color='gray', linestyle='--', linewidth=1)
for bar, val in zip(bars, year_stats['avg_mark']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val:.1f}%',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2 = ax1.twinx()
ax2.plot(x, year_stats['pass_rate'], 'o-', color='#E91E63', linewidth=2, markersize=7, label='Pass Rate')
ax2.set_ylabel('Pass Rate (%)', color='#E91E63')
ax2.tick_params(axis='y', labelcolor='#E91E63')
ax2.set_ylim(0, 110)
ax1.set_title('Average Mark & Pass Rate by Study Year', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart2_year_avg.png')
plt.close()
print("[Saved] chart2_year_avg.png")

# ── CHART 3: Performance Trend over Calendar Years ─────────────────────────
year_trend = df_graded.groupby('Cal_Year')['Marks'].mean().reset_index()
slope, intercept, r, p, _ = stats.linregress(year_trend['Cal_Year'], year_trend['Marks'])

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(year_trend['Cal_Year'], year_trend['Marks'], 'o-', color=NEUTRAL_COLOR,
        linewidth=2.5, markersize=9, label='Annual Average')
trend_y = [slope * y + intercept for y in year_trend['Cal_Year']]
ax.plot(year_trend['Cal_Year'], trend_y, '--', color='#FF9800', linewidth=1.5,
        label=f'Trend (slope={slope:+.1f}/yr, r²={r**2:.2f})')
for x_val, y_val in zip(year_trend['Cal_Year'], year_trend['Marks']):
    ax.annotate(f'{y_val:.1f}%', (x_val, y_val), textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=10)
ax.axhline(50, color='gray', linestyle=':', linewidth=1)
ax.set_xlabel('Calendar Year')
ax.set_ylabel('Average Mark (%)')
ax.set_title('Performance Trend (2021–2025)', fontsize=13, fontweight='bold')
ax.legend()
ax.set_ylim(30, 90)
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart3_trend.png')
plt.close()
print("[Saved] chart3_trend.png")

# ── CHART 4: Pass / Fail Pie ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 5))

# Overall pie
overall_counts = [passed, failed]
axes[0].pie(overall_counts, labels=[f'Pass ({passed})', f'Fail ({failed})'],
            colors=[PASS_COLOR, FAIL_COLOR], autopct='%1.1f%%', startangle=90,
            wedgeprops={'edgecolor': 'white', 'linewidth': 2})
axes[0].set_title('Overall Pass / Fail\n(graded modules)', fontsize=12, fontweight='bold')

# Per year stacked bar
year_pf = df_graded.groupby(['Study_Year', 'Passed']).size().unstack(fill_value=0)
year_pf.columns = ['Fail', 'Pass']
year_pf[['Pass', 'Fail']].plot(kind='bar', ax=axes[1],
    color=[PASS_COLOR, FAIL_COLOR], edgecolor='white', linewidth=0.5)
axes[1].set_xlabel('')
axes[1].set_ylabel('Module Count')
axes[1].set_title('Pass / Fail Count by Study Year', fontsize=12, fontweight='bold')
axes[1].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart4_pass_fail.png')
plt.close()
print("[Saved] chart4_pass_fail.png")

# ── CHART 5: Grade Distribution ───────────────────────────────────────────
grade_order = ['A', 'B', 'C', 'D', 'F']
grade_colors = ['#1B5E20', '#388E3C', '#F9A825', '#FB8C00', '#C62828']
grade_counts = df_graded['Grade'].value_counts().reindex(grade_order, fill_value=0)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(grade_order, grade_counts, color=grade_colors, edgecolor='white', linewidth=0.5, width=0.55)
for bar, val in zip(bars, grade_counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, str(val),
            ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_xlabel('Grade (A≥75, B≥65, C≥55, D≥50, F<50)')
ax.set_ylabel('Number of Modules')
ax.set_title('Grade Distribution — All Graded Modules', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart5_grades.png')
plt.close()
print("[Saved] chart5_grades.png")

# ── CHART 6: Retake Analysis ───────────────────────────────────────────────
retake_codes = df.groupby('Code').filter(lambda g: len(g) > 1)['Code'].unique()

fig, ax = plt.subplots(figsize=(10, 5))
retake_df = df[df['Code'].isin(retake_codes)].copy()
retake_df_graded = retake_df[retake_df['Marks'].notna()].copy()
retake_df_graded = retake_df_graded.sort_values(['Code', 'Cal_Year'])

x_base = 0
xticks, xlabels = [], []
for code in retake_codes:
    sub = retake_df_graded[retake_df_graded['Code'] == code].reset_index(drop=True)
    positions = [x_base + i for i in range(len(sub))]
    bar_colors = [PASS_COLOR if r == 'Pass' else FAIL_COLOR for r in sub['Result']]
    ax.bar(positions, sub['Marks'], color=bar_colors, edgecolor='white', width=0.6)
    for pos, row in zip(positions, sub.itertuples()):
        ax.text(pos, row.Marks + 1, f"{row.Marks}\n({row.Cal_Year})",
                ha='center', va='bottom', fontsize=8)
    mid = x_base + (len(sub) - 1) / 2
    xticks.append(mid)
    xlabels.append(code)
    x_base += len(sub) + 1

ax.set_xticks(xticks)
ax.set_xticklabels(xlabels, fontsize=11)
ax.axhline(50, color='gray', linestyle='--', linewidth=1)
ax.set_ylim(0, 100)
ax.set_ylabel('Final Mark (%)')
ax.set_title('Retaken Modules — Attempt Comparison', fontsize=13, fontweight='bold')
pass_patch = mpatches.Patch(color=PASS_COLOR, label='Pass')
fail_patch = mpatches.Patch(color=FAIL_COLOR, label='Fail')
ax.legend(handles=[pass_patch, fail_patch])
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart6_retakes.png')
plt.close()
print("[Saved] chart6_retakes.png")

# ── CHART 7: Heatmap — Marks by Semester × Year ───────────────────────────
# Use only unique final-attempt marks for a clean heatmap
final_df = df_graded.sort_values('Cal_Year').drop_duplicates(subset=['Code'], keep='last')
pivot = final_df.pivot_table(index='Study_Year', columns='Code', values='Marks', aggfunc='first')
pivot = pivot.reindex(['Year 1', 'Year 2', 'Year 3', 'Year 4'])

fig, ax = plt.subplots(figsize=(14, 5))
mask = pivot.isna()
sns.heatmap(pivot, ax=ax, cmap='RdYlGn', vmin=0, vmax=100,
            annot=True, fmt='.0f', linewidths=0.5, linecolor='white',
            mask=mask, cbar_kws={'label': 'Final Mark (%)'})
ax.set_title('Module Marks Heatmap (Best/Final Attempt per Module)', fontsize=13, fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart7_heatmap.png')
plt.close()
print("[Saved] chart7_heatmap.png")

# ── CHART 8: Box Plot — Score Distribution by Year ────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
groups = [df_graded[df_graded['Study_Year'] == yr]['Marks'].dropna().tolist()
          for yr in ['Year 1', 'Year 2', 'Year 3', 'Year 4']]
bp = ax.boxplot(groups, patch_artist=True, notch=False, widths=0.5)
for patch, color in zip(bp['boxes'], PALETTE):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_xticklabels(['Year 1', 'Year 2', 'Year 3', 'Year 4'])
ax.axhline(50, color='gray', linestyle='--', linewidth=1, label='Pass Mark')
ax.set_ylabel('Final Mark (%)')
ax.set_title('Mark Distribution by Study Year', fontsize=13, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart8_boxplot.png')
plt.close()
print("[Saved] chart8_boxplot.png")

# ── CHART 9: Best vs Worst Modules (final attempt only) ───────────────────
final_df_sorted = final_df.sort_values('Marks')
top5 = final_df_sorted.tail(5)
bot5 = final_df_sorted.head(5)
highlight = pd.concat([bot5, top5])

fig, ax = plt.subplots(figsize=(10, 6))
colors_hw = [FAIL_COLOR if r == 'Fail' else PASS_COLOR for r in highlight['Result']]
bars = ax.barh(highlight['Course'], highlight['Marks'], color=colors_hw, edgecolor='white')
ax.axvline(50, color='gray', linestyle='--', linewidth=1)
ax.axvline(avg, color=NEUTRAL_COLOR, linestyle=':', linewidth=1.5, label=f'Overall avg ({avg:.1f}%)')
for bar, val in zip(bars, highlight['Marks']):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val}%',
            va='center', fontsize=9)
ax.set_xlabel('Final Mark (%)')
ax.set_title('Top 5 & Bottom 5 Modules (Final Attempt)', fontsize=13, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(r'C:\Users\AdminTC\OneDrive - NUST\Documents\Academic Track\chart9_best_worst.png')
plt.close()
print("[Saved] chart9_best_worst.png")

print("\n" + "=" * 60)
print("  All 9 charts saved successfully.")
print("=" * 60)
