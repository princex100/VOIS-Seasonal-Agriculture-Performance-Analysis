"""
Seasonal Agriculture Performance Analysis
VOIS AICTE Internship (Batch 1 2026-2027) Major Project

Module: src/analyze_and_visualize.py
Performs:
1. Data Ingestion & Missing Value Imputation (grouped by Season & Crop).
2. KPI computation & Statistical Hypothesis Testing (ANOVA, Kruskal-Wallis).
3. Exporting 5 High-Resolution Publication-Quality Figures to results/.
4. Exporting cleaned data & summary metrics.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------
# Global Styling Configuration
# ---------------------------------------------------------
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['grid.color'] = '#EAEAEA'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.7

VOIS_RED = "#E60000"
VOIS_DARK = "#1C1C1C"
VOIS_SLATE = "#4A4A4A"
VOIS_ACCENT_TEAL = "#008B8B"
VOIS_ACCENT_ORANGE = "#FF7F0E"
VOIS_ACCENT_PURPLE = "#6A3D9A"
VOIS_ACCENT_GREEN = "#2CA02C"
VOIS_ACCENT_BLUE = "#1F77B4"

PALETTE_SEASONS = {"Kharif": "#E60000", "Rabi": "#1F77B4", "Zaid": "#FF7F0E"}
PALETTE_IRRIGATION = {"Drip": "#2CA02C", "Sprinkler": "#17BECF", "Rainfed": "#9467BD", "Flood": "#D62728"}

def setup_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    os.makedirs("notebooks", exist_ok=True)

def load_and_clean_data(raw_csv_path="data/seasonal_agriculture_performance_dataset (1).csv"):
    df = pd.read_csv(raw_csv_path)
    print(f"[1/5] Raw Dataset Loaded: {df.shape[0]} rows, {df.shape[1]} columns.")
    
    # Check missing values before imputation
    missing_before = df.isnull().sum()
    print("Missing values before imputation:")
    for col, count in missing_before[missing_before > 0].items():
        print(f"  - {col}: {count} missing ({count/len(df)*100:.2f}%)")
        
    # Group median imputation based on Season and Crop
    target_impute_cols = ['Rainfall_mm', 'Soil_Moisture_pct', 'Yield_Tonnes_Ha']
    for col in target_impute_cols:
        if col in df.columns:
            group_medians = df.groupby(['Season', 'Crop'])[col].transform('median')
            overall_median = df[col].median()
            df[col] = df[col].fillna(group_medians).fillna(overall_median)
            
    # Verify derived fields consistency
    # Production = Farm_Area_Hectares * Yield_Tonnes_Ha
    # Revenue = Production_Tonnes * Market_Price_INR_Tonne
    # Profit = Revenue_INR - Total_Cost_INR
    # Water_Efficiency = Production_Tonnes / (Water_Used_m3 / 1000)
    df['Production_Tonnes'] = (df['Farm_Area_Hectares'] * df['Yield_Tonnes_Ha']).round(2)
    df['Revenue_INR'] = (df['Production_Tonnes'] * df['Market_Price_INR_Tonne']).round(0)
    df['Profit_INR'] = (df['Revenue_INR'] - df['Total_Cost_INR']).round(0)
    df['Profit_Per_Ha_INR'] = (df['Profit_INR'] / df['Farm_Area_Hectares']).round(2)
    df['Cost_Per_Ha_INR'] = (df['Total_Cost_INR'] / df['Farm_Area_Hectares']).round(2)
    df['Revenue_Per_Ha_INR'] = (df['Revenue_INR'] / df['Farm_Area_Hectares']).round(2)
    
    # Recompute Water efficiency where valid
    water_k_m3 = df['Water_Used_m3'] / 1000.0
    df['Water_Efficiency_t_per_1000m3'] = np.where(water_k_m3 > 0, (df['Production_Tonnes'] / water_k_m3).round(3), df['Water_Efficiency_t_per_1000m3'])
    
    cleaned_csv_path = "data/cleaned_agricultural_data.csv"
    df.to_csv(cleaned_csv_path, index=False)
    print(f"[2/5] Cleaned data saved to {cleaned_csv_path} (Missing values remaining: {df.isnull().sum().sum()}).")
    return df

def run_statistical_tests(df):
    print("\n[3/5] Running Statistical Hypothesis Tests...")
    stats_results = {}
    
    # ANOVA & Kruskal-Wallis for Yield across Seasons
    kharif_yield = df[df['Season'] == 'Kharif']['Yield_Tonnes_Ha']
    rabi_yield = df[df['Season'] == 'Rabi']['Yield_Tonnes_Ha']
    zaid_yield = df[df['Season'] == 'Zaid']['Yield_Tonnes_Ha']
    
    anova_yield = stats.f_oneway(kharif_yield, rabi_yield, zaid_yield)
    kruskal_yield = stats.kruskal(kharif_yield, rabi_yield, zaid_yield)
    
    stats_results['yield_anova'] = {'F_stat': float(anova_yield.statistic), 'p_value': float(anova_yield.pvalue)}
    stats_results['yield_kruskal'] = {'H_stat': float(kruskal_yield.statistic), 'p_value': float(kruskal_yield.pvalue)}
    
    # ANOVA & Kruskal-Wallis for Profit across Seasons
    kharif_profit = df[df['Season'] == 'Kharif']['Profit_INR']
    rabi_profit = df[df['Season'] == 'Rabi']['Profit_INR']
    zaid_profit = df[df['Season'] == 'Zaid']['Profit_INR']
    
    anova_profit = stats.f_oneway(kharif_profit, rabi_profit, zaid_profit)
    kruskal_profit = stats.kruskal(kharif_profit, rabi_profit, zaid_profit)
    
    stats_results['profit_anova'] = {'F_stat': float(anova_profit.statistic), 'p_value': float(anova_profit.pvalue)}
    stats_results['profit_kruskal'] = {'H_stat': float(kruskal_profit.statistic), 'p_value': float(kruskal_profit.pvalue)}
    
    # Summary Metrics Table
    seasonal_summary = df.groupby('Season').agg(
        Count=('Farm_ID', 'count'),
        Avg_Yield_t_ha=('Yield_Tonnes_Ha', 'mean'),
        Median_Yield_t_ha=('Yield_Tonnes_Ha', 'median'),
        Avg_Rainfall_mm=('Rainfall_mm', 'mean'),
        Avg_Water_Efficiency=('Water_Efficiency_t_per_1000m3', 'mean'),
        Avg_Total_Cost_INR=('Total_Cost_INR', 'mean'),
        Avg_Revenue_INR=('Revenue_INR', 'mean'),
        Avg_Net_Profit_INR=('Profit_INR', 'mean'),
        Avg_Profit_Per_Ha=('Profit_Per_Ha_INR', 'mean'),
        Avg_Pest_Risk_pct=('Disease_Pest_Risk_pct', 'mean')
    ).round(2).reset_index()
    
    irrigation_summary = df.groupby('Irrigation_Method').agg(
        Count=('Farm_ID', 'count'),
        Avg_Water_Efficiency=('Water_Efficiency_t_per_1000m3', 'mean'),
        Median_Water_Efficiency=('Water_Efficiency_t_per_1000m3', 'median'),
        Avg_Net_Profit_INR=('Profit_INR', 'mean'),
        Avg_Profit_Per_Ha=('Profit_Per_Ha_INR', 'mean'),
        Avg_Cost_Per_Ha=('Cost_Per_Ha_INR', 'mean')
    ).round(2).reset_index()
    
    stats_results['seasonal_summary'] = seasonal_summary.to_dict(orient='records')
    stats_results['irrigation_summary'] = irrigation_summary.to_dict(orient='records')
    
    with open('results/statistical_summary.json', 'w', encoding='utf-8') as f:
        json.dump(stats_results, f, indent=4)
        
    print("Statistical ANOVA Yield F:", anova_yield.statistic, "p:", anova_yield.pvalue)
    print("Statistical ANOVA Profit F:", anova_profit.statistic, "p:", anova_profit.pvalue)
    print("Summary statistics saved to results/statistical_summary.json")
    return stats_results, seasonal_summary, irrigation_summary

def generate_visualizations(df, seasonal_summary, irrigation_summary):
    print("\n[4/5] Generating 5 Publication-Quality Visualization Figures in results/...")
    
    # -------------------------------------------------------------------------
    # Chart 1: Dual-Axis Seasonal Yield & Rainfall Dynamic
    # -------------------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
    seasons = ['Kharif', 'Rabi', 'Zaid']
    season_data = seasonal_summary.set_index('Season').loc[seasons]
    
    x = np.arange(len(seasons))
    width = 0.38
    
    # Bar for Rainfall
    bars = ax1.bar(x - width/2, season_data['Avg_Rainfall_mm'], width, label='Avg Rainfall (mm)',
                   color='#2B5B84', edgecolor='#1A364F', linewidth=1.2, alpha=0.9, zorder=3)
    ax1.set_ylabel('Mean Rainfall (mm)', fontsize=12, fontweight='bold', color='#2B5B84')
    ax1.tick_params(axis='y', labelcolor='#2B5B84', labelsize=10)
    ax1.set_ylim(0, season_data['Avg_Rainfall_mm'].max() * 1.25)
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    
    # Value annotations on bars
    for bar in bars:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f} mm', xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points", ha='center', va='bottom',
                     fontsize=10, fontweight='bold', color='#1A364F')
    
    # Line for Yield on secondary axis
    ax2 = ax1.twinx()
    line = ax2.plot(x + width/2, season_data['Avg_Yield_t_ha'], color=VOIS_RED, marker='o',
                    linewidth=3.0, markersize=9, label='Avg Crop Yield (Tonnes/Ha)', zorder=4)
    ax2.set_ylabel('Mean Yield (Tonnes/Ha)', fontsize=12, fontweight='bold', color=VOIS_RED)
    ax2.tick_params(axis='y', labelcolor=VOIS_RED, labelsize=10)
    ax2.set_ylim(0, season_data['Avg_Yield_t_ha'].max() * 1.35)
    
    for i, val in enumerate(season_data['Avg_Yield_t_ha']):
        ax2.annotate(f'{val:.2f} t/ha', xy=(x[i] + width/2, val),
                     xytext=(0, 8), textcoords="offset points", ha='center', va='bottom',
                     fontsize=10, fontweight='bold', color=VOIS_RED,
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=VOIS_RED, alpha=0.9))
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(seasons, fontsize=12, fontweight='bold')
    ax1.set_xlabel('Agricultural Season', fontsize=12, fontweight='bold', labelpad=10)
    
    plt.title('Seasonal Agronomic Dynamics: Mean Rainfall vs. Average Crop Yield',
              fontsize=14, fontweight='bold', pad=15, color=VOIS_DARK)
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)
    
    plt.tight_layout()
    chart1_path = "results/01_seasonal_yield_rainfall.png"
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved {chart1_path}")
    
    # -------------------------------------------------------------------------
    # Chart 2: Irrigation Method Water Efficiency vs. Net Profit
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    irr_df = df.groupby('Irrigation_Method').agg({
        'Water_Efficiency_t_per_1000m3': 'mean',
        'Profit_Per_Ha_INR': 'mean',
        'Farm_ID': 'count'
    }).reset_index().rename(columns={'Farm_ID': 'Sample_Count'})
    
    scatter = sns.scatterplot(
        data=irr_df,
        x='Water_Efficiency_t_per_1000m3',
        y='Profit_Per_Ha_INR',
        hue='Irrigation_Method',
        palette=PALETTE_IRRIGATION,
        s=350,
        edgecolor='black',
        linewidth=1.5,
        ax=ax,
        zorder=5
    )
    
    # Draw reference cross lines at median
    med_eff = irr_df['Water_Efficiency_t_per_1000m3'].median()
    med_prof = irr_df['Profit_Per_Ha_INR'].median()
    ax.axvline(med_eff, color='gray', linestyle=':', alpha=0.7, zorder=2)
    ax.axhline(med_prof, color='gray', linestyle=':', alpha=0.7, zorder=2)
    
    for _, row in irr_df.iterrows():
        ax.annotate(
            f"{row['Irrigation_Method']}\n({row['Water_Efficiency_t_per_1000m3']:.2f} t/k m³, ₹{row['Profit_Per_Ha_INR']:,.0f}/ha)",
            xy=(row['Water_Efficiency_t_per_1000m3'], row['Profit_Per_Ha_INR']),
            xytext=(10, 8),
            textcoords="offset points",
            fontsize=10,
            fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#F7F9FA", edgecolor="#D1D5DB", alpha=0.9)
        )
        
    ax.set_title('Irrigation Efficiency vs. Net Profitability per Hectare', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Water Efficiency (Tonnes produced per 1,000 m³ water)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('Average Net Profit per Hectare (INR)', fontsize=12, fontweight='bold', labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(title='Irrigation Method', loc='upper left', frameon=True)
    
    plt.tight_layout()
    chart2_path = "results/02_irrigation_profit_efficiency.png"
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved {chart2_path}")
    
    # -------------------------------------------------------------------------
    # Chart 3: Economic Returns across Kharif, Rabi, and Zaid (Cost, Revenue, Profit)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    econ_data = seasonal_summary.set_index('Season').loc[['Kharif', 'Rabi', 'Zaid']]
    seasons = econ_data.index.tolist()
    x = np.arange(len(seasons))
    bar_width = 0.25
    
    cost_bars = ax.bar(x - bar_width, econ_data['Avg_Total_Cost_INR'] / 1000, bar_width,
                       label='Total Cost (₹ Thousands)', color='#E74C3C', edgecolor='#922B21', alpha=0.9, zorder=3)
    rev_bars = ax.bar(x, econ_data['Avg_Revenue_INR'] / 1000, bar_width,
                      label='Revenue (₹ Thousands)', color='#2ECC71', edgecolor='#196F3D', alpha=0.9, zorder=3)
    prof_bars = ax.bar(x + bar_width, econ_data['Avg_Net_Profit_INR'] / 1000, bar_width,
                       label='Net Profit (₹ Thousands)', color='#3498DB', edgecolor='#1F618D', alpha=0.9, zorder=3)
    
    # Annotations
    for bar_group in [cost_bars, rev_bars, prof_bars]:
        for bar in bar_group:
            h = bar.get_height()
            va = 'bottom' if h >= 0 else 'top'
            ax.annotate(f'₹{h:.0f}k',
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3 if h >= 0 else -10),
                        textcoords="offset points",
                        ha='center', va=va,
                        fontsize=9, fontweight='bold')
            
    ax.axhline(0, color='black', linewidth=1.0, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels(seasons, fontsize=12, fontweight='bold')
    ax.set_ylabel('Financial Valuation (INR Thousands)', fontsize=12, fontweight='bold')
    ax.set_title('Seasonal Economic Performance: Financial Return Breakdown', fontsize=14, fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.95)
    
    plt.tight_layout()
    chart3_path = "results/03_economic_returns_season.png"
    plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved {chart3_path}")
    
    # -------------------------------------------------------------------------
    # Chart 4: Scatter / Regression: Chemical Application vs Disease/Pest Risk %
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    
    # Subplot A: Pesticide vs Pest Risk
    sns.regplot(
        data=df,
        x='Pesticide_Litre_ha',
        y='Disease_Pest_Risk_pct',
        scatter_kws={'alpha': 0.35, 'color': '#34495E', 's': 25},
        line_kws={'color': VOIS_RED, 'linewidth': 2.5, 'label': 'Regression Trend'},
        ax=ax1
    )
    slope_pest, intercept_pest, r_val_pest, p_val_pest, _ = stats.linregress(df['Pesticide_Litre_ha'], df['Disease_Pest_Risk_pct'])
    ax1.set_title('Pesticide Application vs. Disease/Pest Risk', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Pesticide Application (Litre/Ha)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Disease/Pest Risk (%)', fontsize=11, fontweight='bold')
    ax1.annotate(f'r = {r_val_pest:.3f} | p = {p_val_pest:.3e}', xy=(0.05, 0.90), xycoords='axes fraction',
                 fontsize=10, fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right')
    
    # Subplot B: Fertilizer vs Pest Risk
    sns.regplot(
        data=df,
        x='Fertilizer_kg_ha',
        y='Disease_Pest_Risk_pct',
        scatter_kws={'alpha': 0.35, 'color': '#27AE60', 's': 25},
        line_kws={'color': '#D35400', 'linewidth': 2.5, 'label': 'Regression Trend'},
        ax=ax2
    )
    slope_fert, intercept_fert, r_val_fert, p_val_fert, _ = stats.linregress(df['Fertilizer_kg_ha'], df['Disease_Pest_Risk_pct'])
    ax2.set_title('Fertilizer Dosage vs. Disease/Pest Risk', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Fertilizer Dosage (kg/Ha)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Disease/Pest Risk (%)', fontsize=11, fontweight='bold')
    ax2.annotate(f'r = {r_val_fert:.3f} | p = {p_val_fert:.3e}', xy=(0.05, 0.90), xycoords='axes fraction',
                 fontsize=10, fontweight='bold', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='lower right')
    
    fig.suptitle('Agrochemical Input Intensity vs. Environmental Pest Risk Dynamics', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    chart4_path = "results/04_pesticide_fertilizer_pest_risk.png"
    plt.savefig(chart4_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved {chart4_path}")
    
    # -------------------------------------------------------------------------
    # Chart 5: Crop Performance Matrix across Seasons (Heatmap)
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=300)
    
    # Pivot 1: Average Profit per Hectare
    profit_matrix = df.pivot_table(index='Crop', columns='Season', values='Profit_Per_Ha_INR', aggfunc='mean')[['Kharif', 'Rabi', 'Zaid']]
    sns.heatmap(
        profit_matrix,
        annot=True,
        fmt=',.0f',
        cmap='YlGnBu',
        cbar_kws={'label': 'Net Profit (₹/Ha)'},
        linewidths=1.0,
        ax=ax1
    )
    ax1.set_title('Crop Net Profitability per Hectare (INR)', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel('Season', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Crop Category', fontsize=11, fontweight='bold')
    
    # Pivot 2: Average Yield (Tonnes/Ha)
    yield_matrix = df.pivot_table(index='Crop', columns='Season', values='Yield_Tonnes_Ha', aggfunc='mean')[['Kharif', 'Rabi', 'Zaid']]
    sns.heatmap(
        yield_matrix,
        annot=True,
        fmt='.2f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Mean Yield (t/Ha)'},
        linewidths=1.0,
        ax=ax2
    )
    ax2.set_title('Crop Mean Productivity (Tonnes/Ha)', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel('Season', fontsize=11, fontweight='bold')
    ax2.set_ylabel('')
    
    fig.suptitle('Seasonal Crop Performance Matrix: Profitability vs. Agronomic Yield', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    chart5_path = "results/05_crop_performance_matrix.png"
    plt.savefig(chart5_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  -> Saved {chart5_path}")
    print("[5/5] All 5 figures generated and verified successfully!")

if __name__ == "__main__":
    setup_directories()
    df = load_and_clean_data()
    stats_results, seasonal_summary, irrigation_summary = run_statistical_tests(df)
    generate_visualizations(df, seasonal_summary, irrigation_summary)
