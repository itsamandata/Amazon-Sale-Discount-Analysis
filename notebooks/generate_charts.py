import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set visual style
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 150

df = pd.read_csv('c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/data/ecommerce_sale_discount_data.csv')

# Chart 1: Deal Type Breakdown
plt.figure(figsize=(7, 5))
deal_counts = df['deal_type'].value_counts()
colors = ['#2ecc71', '#f39c12', '#e74c3c']
plt.pie(deal_counts, labels=deal_counts.index, autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.05, 0.05, 0.05), shadow=True)
plt.title('Distribution of Sale Deals: Genuine vs Deceptive Marketing', fontsize=12, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/images/deal_breakdown.png')
plt.close()

# Chart 2: Advertised vs Real Discount by Category
cat_summary = df.groupby('category')[['advertised_discount_pct', 'actual_real_discount_pct']].mean().reset_index()
cat_summary_melted = cat_summary.melt(id_vars='category', var_name='Discount_Type', value_name='Discount_Pct')
cat_summary_melted['Discount_Type'] = cat_summary_melted['Discount_Type'].replace({
    'advertised_discount_pct': 'Advertised Discount (MRP)',
    'actual_real_discount_pct': 'Actual Real Discount (30d Avg)'
})

plt.figure(figsize=(10, 5.5))
bar_plot = sns.barplot(data=cat_summary_melted, x='category', y='Discount_Pct', hue='Discount_Type', palette=['#3498db', '#e67e22'])
plt.title('Advertised Discount (MRP) vs Actual Real Discount (30-Day Pre-Sale Avg)', fontsize=13, fontweight='bold', pad=12)
plt.ylabel('Average Discount (%)', fontsize=11)
plt.xlabel('Category', fontsize=11)
plt.xticks(rotation=15, ha='right')
plt.legend(title='')
for p in bar_plot.patches:
    h = p.get_height()
    if h > 0:
        bar_plot.annotate(f'{h:.1f}%', (p.get_x() + p.get_width() / 2., h / 2),
                         ha='center', va='center', color='white', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig('c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/images/advertised_vs_real_discount.png')
plt.close()

# Chart 3: The Discount Trap (High Advertised Discount vs Return Rate)
plt.figure(figsize=(9, 5.5))
sns.scatterplot(
    data=df, 
    x='advertised_discount_pct', 
    y='return_rate_pct', 
    hue='deal_type', 
    palette={'Genuine Deal': '#2ecc71', 'Artificial / Slight Hike': '#f39c12', 'Fake Discount (Hidden Markup)': '#e74c3c'}, 
    alpha=0.75, 
    s=60
)
plt.axvline(x=40, color='gray', linestyle='--', alpha=0.7, label='40%+ Discount Threshold')
plt.axhline(y=15, color='red', linestyle='--', alpha=0.7, label='15%+ High Return Rate')
plt.title('The Discount Trap: High Advertised Discounts vs Customer Return Rate', fontsize=12, fontweight='bold', pad=12)
plt.xlabel('Advertised Discount (%)', fontsize=11)
plt.ylabel('Product Return Rate (%)', fontsize=11)
plt.legend(title='Deal Classification', loc='upper left')
plt.tight_layout()
plt.savefig('c:/Users/aman1/OneDrive/Documents/projects/Amazon-Sale-Discount-Analysis/images/discount_trap_analysis.png')
plt.close()

print('All 3 analytical charts generated successfully!')
