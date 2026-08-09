"""
Project 2: Exploratory Data Analysis Pipeline
Author: Rutuja Shinde
Industrial Training Kit DecodeLabs (Batch 2026)

This script performs end to end exploratory data analysis on Cleaned_Dataset.csv
following the DecodeLabs Forensic EDA Framework. It outputs detailed descriptive 
statistics, outlier forensics (IQR vs Z score), correlation analysis, segment 
breakdowns, financial leak analysis, and 8 high resolution publication ready charts.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set styling for publication ready visual assets
plt.style.use('dark_background')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['grid.color'] = '#262626'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.6

class EDAEngine:
    def __init__(self, csv_path: str, output_dir: str):
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.charts_dir = os.path.join(output_dir, 'charts')
        os.makedirs(self.charts_dir, exist_ok=True)
        self.df = None

    def load_and_preprocess(self):
        """Loads dataset and ensures proper datatypes."""
        self.df = pd.read_csv(self.csv_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['YearMonth'] = self.df['Date'].dt.to_period('M')
        return self.df

    def audit_schema(self) -> dict:
        """Audits dataset schema, nulls, duplicates, and ranges."""
        audit = {
            'total_records': len(self.df),
            'total_features': len(self.df.columns),
            'unique_orders': self.df['OrderID'].nunique(),
            'unique_customers': self.df['CustomerID'].nunique(),
            'null_counts': self.df.isnull().sum().to_dict(),
            'date_min': self.df['Date'].min().strftime('%Y-%m-%d'),
            'date_max': self.df['Date'].max().strftime('%Y-%m-%d')
        }
        return audit

    def compute_five_number_summary(self) -> pd.DataFrame:
        """Computes 5-number summary (Min, Q1, Median, Q3, Max) plus Mean, Std, and Skewness."""
        numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
        summary_data = []

        for col in numeric_cols:
            s = self.df[col]
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            iqr = q3 - q1
            summary_data.append({
                'Feature': col,
                'Count': int(s.count()),
                'Mean': float(s.mean()),
                'StdDev': float(s.std()),
                'Min (Floor)': float(s.min()),
                'Q1 (25th %)': float(q1),
                'Median (50th %)': float(s.median()),
                'Q3 (75th %)': float(q3),
                'Max (Ceiling)': float(s.max()),
                'IQR': float(iqr),
                'Skewness': float(s.skew())
            })
        return pd.DataFrame(summary_data)

    def detect_outliers(self) -> dict:
        """Compares IQR Method vs Z-Score Method for outlier detection."""
        numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
        results = {}

        for col in numeric_cols:
            s = self.df[col]
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            iqr_outliers = self.df[(s < lower_bound) | (s > upper_bound)]

            z_scores = (s - s.mean()) / s.std()
            z_outliers = self.df[np.abs(z_scores) > 3.0]

            results[col] = {
                'iqr_count': len(iqr_outliers),
                'iqr_lower_bound': lower_bound,
                'iqr_upper_bound': upper_bound,
                'iqr_outlier_ids': iqr_outliers['OrderID'].tolist(),
                'zscore_count': len(z_outliers),
                'zscore_outlier_ids': z_outliers['OrderID'].tolist()
            }
        return results

    def compute_correlation_matrix(self) -> pd.DataFrame:
        """Calculates Pearson Correlation Matrix."""
        numeric_cols = ['Quantity', 'UnitPrice', 'ItemsInCart', 'TotalPrice']
        return self.df[numeric_cols].corr()

    def analyze_financial_impact(self) -> pd.DataFrame:
        """Calculates financial breakdown by Order Status."""
        status_df = self.df.groupby('OrderStatus').agg(
            Order_Count=('OrderID', 'count'),
            Total_Revenue=('TotalPrice', 'sum'),
            Avg_Order_Value=('TotalPrice', 'mean')
        ).reset_index()

        total_gross = self.df['TotalPrice'].sum()
        status_df['Revenue_Share_Pct'] = (status_df['Total_Revenue'] / total_gross) * 100
        return status_df

    def analyze_segments(self) -> dict:
        """Aggregates metrics by Product, PaymentMethod, CouponCode, and ReferralSource."""
        segments = {}
        for dim in ['Product', 'PaymentMethod', 'CouponCode', 'ReferralSource']:
            agg = self.df.groupby(dim).agg(
                Order_Count=('OrderID', 'count'),
                Total_Revenue=('TotalPrice', 'sum'),
                Avg_Order_Value=('TotalPrice', 'mean'),
                Return_Count=('OrderStatus', lambda x: (x == 'Returned').sum()),
                Cancellation_Count=('OrderStatus', lambda x: (x == 'Cancelled').sum())
            ).reset_index()
            agg['Return_Rate_Pct'] = (agg['Return_Count'] / agg['Order_Count']) * 100
            agg['Cancellation_Rate_Pct'] = (agg['Cancellation_Count'] / agg['Order_Count']) * 100
            segments[dim] = agg
        return segments

    # Visualization Methods

    def generate_chart_01_univariate(self):
        """Chart 01: Univariate Distributions and Density (Histograms and KDE)."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Univariate Distributions and Density Analysis', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.96)

        cols = [('Quantity', '#4cc9f0'), ('UnitPrice', '#f72585'), ('ItemsInCart', '#7209b7'), ('TotalPrice', '#4361ee')]

        for ax, (col, color) in zip(axes.flatten(), cols):
            sns.histplot(self.df[col], kde=True, ax=ax, color=color, bins=25, edgecolor='none', alpha=0.6)
            skew_val = self.df[col].skew()
            ax.set_title(f'{col} (Skewness: {skew_val:.3f})', fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel(col, fontsize=10)
            ax.set_ylabel('Frequency', fontsize=10)
            ax.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '01_univariate_distributions.png'), dpi=300)
        plt.close(fig)

    def generate_chart_02_five_number_summary(self):
        """Chart 02: Five-Number Summary and IQR Boxplots."""
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Five Number Summary and Distribution Spread (Boxplots)', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.98)

        # Plot 1: UnitPrice Boxplot
        sns.boxplot(y=self.df['UnitPrice'], ax=axes[0], color='#4cc9f0', width=0.4, fliersize=6)
        axes[0].set_title('UnitPrice ($) Range and Median', fontsize=13, fontweight='bold')
        axes[0].set_ylabel('Unit Price ($)', fontsize=11)
        axes[0].grid(True, linestyle='--', alpha=0.3)

        # Plot 2: TotalPrice Boxplot (Showing IQR Outliers)
        sns.boxplot(y=self.df['TotalPrice'], ax=axes[1], color='#f72585', width=0.4, fliersize=6,
                    flierprops=dict(marker='o', markerfacecolor='#ff4d6d', markeredgecolor='white', markersize=8))
        axes[1].set_title('TotalPrice ($) Distribution (8 IQR Outliers Detected)', fontsize=13, fontweight='bold')
        axes[1].set_ylabel('Total Price ($)', fontsize=11)
        axes[1].grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '02_five_number_summary_boxplots.png'), dpi=300)
        plt.close(fig)

    def generate_chart_03_outlier_comparison(self):
        """Chart 03: Outlier Detection Method Comparison (IQR vs Z-Score)."""
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.suptitle('Outlier Detection Forensic: IQR Method vs Z-Score Method', fontsize=16, fontweight='bold', color='#4cc9f0')

        s = self.df['TotalPrice']
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        iqr_limit = q3 + 1.5 * iqr

        z_scores = np.abs((s - s.mean()) / s.std())
        z_limit = s.mean() + 3.0 * s.std()

        x = range(len(self.df))
        ax.scatter(x, s, c='#4cc9f0', alpha=0.4, s=25, label='Normal Transaction')

        iqr_mask = s > iqr_limit
        ax.scatter(np.where(iqr_mask)[0], s[iqr_mask], c='#ff4d6d', s=80, edgecolors='white', zorder=5, label=f'IQR Flagged Outliers (n=8 > ${iqr_limit:,.2f})')

        ax.axhline(iqr_limit, color='#ff4d6d', linestyle='--', linewidth=2, label=f'IQR Upper Limit (${iqr_limit:,.2f})')
        ax.axhline(z_limit, color='#fee440', linestyle=':', linewidth=2, label=f'Z-Score Threshold |Z|>3 (${z_limit:,.2f}) [0 Flagged]')

        ax.set_title('TotalPrice ($) Outliers: IQR Identifies Right Skewed VIP Transactions Where Z-Score Fails', fontsize=12, pad=10)
        ax.set_xlabel('Order Index', fontsize=11)
        ax.set_ylabel('Total Price ($)', fontsize=11)
        ax.legend(loc='upper right', facecolor='#111111', edgecolor='#333333', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.3)

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '03_outlier_iqr_vs_zscore.png'), dpi=300)
        plt.close(fig)

    def generate_chart_04_correlation(self):
        """Chart 04: Pearson Correlation Heatmap."""
        fig, ax = plt.subplots(figsize=(9, 7))
        fig.suptitle('Mapping Relationships: Pearson Correlation Matrix (r)', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.97)

        corr = self.compute_correlation_matrix()
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        sns.heatmap(corr, annot=True, fmt='.3f', cmap=cmap, vmin=-1, vmax=1, center=0,
                    square=True, linewidths=1.5, cbar_kws={"shrink": .8}, ax=ax, annot_kws={"size": 11, "weight": "bold"})

        ax.set_title('Strongest Drivers: UnitPrice (r = 0.717) and Quantity (r = 0.615) driving TotalPrice', fontsize=11, pad=12)

        plt.tight_layout(rect=[0, 0, 1, 0.93])
        fig.savefig(os.path.join(self.charts_dir, '04_correlation_heatmap.png'), dpi=300)
        plt.close(fig)

    def generate_chart_05_financial_impact(self):
        """Chart 05: Revenue Leak and Order Status Financial Impact."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        fig.suptitle('Financial Diagnosis: $519.7k Gross Revenue Leak (Cancellations and Returns)', fontsize=16, fontweight='bold', color='#ff4d6d', y=0.98)

        status_df = self.analyze_financial_impact()
        colors = {'Delivered': '#06d6a0', 'Shipped': '#118ab2', 'Pending': '#ffd166', 'Returned': '#f78c6b', 'Cancelled': '#ef476f'}
        status_colors = [colors.get(s, '#ffffff') for s in status_df['OrderStatus']]

        # Bar chart: Total Revenue by Order Status
        bars = ax1.bar(status_df['OrderStatus'], status_df['Total_Revenue'], color=status_colors, edgecolor='none', width=0.55)
        ax1.set_title('Gross Revenue Breakdown by Status ($)', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Total Revenue ($)', fontsize=11)
        ax1.grid(True, linestyle='--', alpha=0.3, axis='y')

        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 5000, f'${height:,.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Donut Chart: Revenue Share
        wedges, texts, autotexts = ax2.pie(
            status_df['Total_Revenue'], labels=status_df['OrderStatus'], colors=status_colors,
            autopct='%1.1f%%', startangle=140, pctdistance=0.75, textprops=dict(color='white', fontweight='bold')
        )
        centre_circle = plt.Circle((0, 0), 0.50, fc='#111111')
        ax2.add_artist(centre_circle)
        ax2.set_title('Revenue Share Distribution (%)\n41.09% Leakage', fontsize=13, fontweight='bold')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '05_order_status_financial_impact.png'), dpi=300)
        plt.close(fig)

    def generate_chart_06_product_performance(self):
        """Chart 06: Product Category Performance and Loss Rates."""
        fig, ax1 = plt.subplots(figsize=(14, 7))
        fig.suptitle('Product Performance: Revenue and Order Frequencies', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.98)

        prod_df = self.analyze_segments()['Product'].sort_values(by='Total_Revenue', ascending=False)

        x = np.arange(len(prod_df))
        width = 0.35

        rects1 = ax1.bar(x - width/2, prod_df['Total_Revenue'], width, label='Total Revenue ($)', color='#4cc9f0')
        ax1.set_ylabel('Total Revenue ($)', fontsize=11, color='#4cc9f0')
        ax1.set_xticks(x)
        ax1.set_xticklabels(prod_df['Product'], fontsize=11, fontweight='bold')
        ax1.grid(True, linestyle='--', alpha=0.3, axis='y')

        ax2 = ax1.twinx()
        rects2 = ax2.bar(x + width/2, prod_df['Order_Count'], width, label='Order Volume', color='#7209b7')
        ax2.set_ylabel('Order Count', fontsize=11, color='#7209b7')

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', facecolor='#111111')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '06_product_performance_returns.png'), dpi=300)
        plt.close(fig)

    def generate_chart_07_referral_coupon_matrix(self):
        """Chart 07: Referral Channel and Coupon Code Conversion Matrix."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Marketing and Promotion Analysis: Channel and Coupon Impact', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.98)

        ref_df = self.analyze_segments()['ReferralSource'].sort_values(by='Total_Revenue', ascending=False)
        sns.barplot(data=ref_df, x='ReferralSource', y='Total_Revenue', ax=ax1, hue='ReferralSource', palette='Blues_r', legend=False)
        ax1.set_title('Revenue by Referral Source ($)', fontsize=13, fontweight='bold')
        ax1.set_xlabel('Referral Channel', fontsize=11)
        ax1.set_ylabel('Total Revenue ($)', fontsize=11)
        ax1.grid(True, linestyle='--', alpha=0.3, axis='y')

        coupon_df = self.analyze_segments()['CouponCode'].sort_values(by='Total_Revenue', ascending=False)
        sns.barplot(data=coupon_df, x='CouponCode', y='Total_Revenue', ax=ax2, hue='CouponCode', palette='Purples_r', legend=False)
        ax2.set_title('Revenue by Coupon Code Used ($)', fontsize=13, fontweight='bold')
        ax2.set_xlabel('Coupon Code', fontsize=11)
        ax2.set_ylabel('Total Revenue ($)', fontsize=11)
        ax2.grid(True, linestyle='--', alpha=0.3, axis='y')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '07_referral_coupon_matrix.png'), dpi=300)
        plt.close(fig)

    def generate_chart_08_monthly_trends(self):
        """Chart 08: Monthly Revenue and Order Volume Trends (2023 to 2025)."""
        fig, ax1 = plt.subplots(figsize=(15, 7))
        fig.suptitle('Temporal Dynamics: Monthly Revenue and Order Volume Trends (Jan 2023 to Jun 2025)', fontsize=16, fontweight='bold', color='#4cc9f0', y=0.98)

        monthly = self.df.groupby('YearMonth').agg(
            Total_Revenue=('TotalPrice', 'sum'),
            Order_Count=('OrderID', 'count')
        ).reset_index()
        monthly['MonthStr'] = monthly['YearMonth'].astype(str)

        ax1.plot(monthly['MonthStr'], monthly['Total_Revenue'], marker='o', linewidth=2.5, color='#06d6a0', label='Monthly Gross Revenue ($)')
        ax1.set_ylabel('Monthly Revenue ($)', fontsize=11, color='#06d6a0')
        ax1.set_xlabel('Year Month', fontsize=11)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, linestyle='--', alpha=0.3)

        ax2 = ax1.twinx()
        ax2.plot(monthly['MonthStr'], monthly['Order_Count'], marker='s', linewidth=2, linestyle='--', color='#ff4d6d', label='Monthly Order Count')
        ax2.set_ylabel('Order Count', fontsize=11, color='#ff4d6d')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor='#111111')

        plt.tight_layout(rect=[0, 0, 1, 0.94])
        fig.savefig(os.path.join(self.charts_dir, '08_monthly_sales_trend.png'), dpi=300)
        plt.close(fig)

    def run_pipeline(self):
        """Executes full analysis pipeline and exports all visual assets."""
        print("Starting Project 2 Exploratory Data Analysis Pipeline...")
        self.load_and_preprocess()
        print("Dataset loaded successfully.")

        schema = self.audit_schema()
        print(f"Schema Audit: {schema['total_records']} rows, {schema['total_features']} columns.")

        five_num = self.compute_five_number_summary()
        print("\nFive-Number Summary and Descriptive Statistics:")
        print(five_num.to_string(index=False))

        outliers = self.detect_outliers()
        print("\nOutlier Forensics (IQR vs Z-Score):")
        for col, data in outliers.items():
            print(f"{col}: IQR Method = {data['iqr_count']} outliers | Z-Score Method = {data['zscore_count']} outliers")

        corr = self.compute_correlation_matrix()
        print("\nPearson Correlation Matrix:")
        print(corr.to_string())

        print(r"Generating 8 high-resolution charts in R:\Projects\Internship\Project_2\charts...")
        self.generate_chart_01_univariate()
        self.generate_chart_02_five_number_summary()
        self.generate_chart_03_outlier_comparison()
        self.generate_chart_04_correlation()
        self.generate_chart_05_financial_impact()
        self.generate_chart_06_product_performance()
        self.generate_chart_07_referral_coupon_matrix()
        self.generate_chart_08_monthly_trends()

        print("Pipeline complete. All visual assets and statistics generated successfully.")

if __name__ == '__main__':
    csv_file = r'R:\Projects\Internship\Project_2\Cleaned_Dataset.csv'
    output_directory = r'R:\Projects\Internship\Project_2'
    engine = EDAEngine(csv_file, output_directory)
    engine.run_pipeline()

