import pandas as pd
import numpy as np
from datetime import datetime

def convert_wide_to_long_csv(file_path):
    """
    Convert wide format Taiwan stock data to long format and save as CSV
    """
    print("📊 Starting conversion...")
    
    # Read the Excel file
    print("📂 Reading Excel file...")
    df = pd.read_excel(file_path)
    
    # Get column names
    date_col = df.columns[0]  # First column is date
    stock_cols = df.columns[1:]  # All other columns are stocks
    
    print(f"📈 Found {len(df)} rows × {len(stock_cols)} stocks")
    print(f"📅 Date range: {df[date_col].min()} to {df[date_col].max()}")
    
    # Convert to long format using pandas melt
    print("🔄 Converting to long format...")
    long_df = df.melt(
        id_vars=[date_col],
        value_vars=stock_cols,
        var_name='Stock',
        value_name='Price'
    )
    
    # Rename date column to English
    long_df = long_df.rename(columns={date_col: 'Date'})
    
    # Clean the data
    print("🧹 Cleaning data...")
    initial_rows = len(long_df)
    
    # Remove rows with missing prices
    long_df = long_df.dropna(subset=['Price'])
    long_df = long_df[long_df['Price'] != '-']
    long_df = long_df[long_df['Price'] != '']
    
    # Reset index
    long_df = long_df.reset_index(drop=True)
    
    final_rows = len(long_df)
    removed_rows = initial_rows - final_rows
    
    print(f"🗑️  Removed {removed_rows:,} empty/invalid rows")
    print(f"✅ Conversion complete! {final_rows:,} data points created")
    
    # Save as CSV
    csv_filename = "taiwan_stocks_long_format.csv"
    print(f"💾 Saving to {csv_filename}...")
    
    long_df.to_csv(csv_filename, index=False)
    
    print(f"✅ CSV file saved successfully!")
    
    # Show summary statistics
    print("\n📊 Dataset Summary:")
    print(f"   Total data points: {len(long_df):,}")
    print(f"   Unique stocks: {long_df['Stock'].nunique():,}")
    print(f"   Unique dates: {long_df['Date'].nunique():,}")
    print(f"   Date range: {long_df['Date'].min()} to {long_df['Date'].max()}")
    
    # Show sample data
    print("\n📋 Sample of converted data:")
    print(long_df.head(10).to_string(index=False))
    
    # Show file size
    try:
        import os
        file_size = os.path.getsize(csv_filename)
        file_size_mb = file_size / (1024 * 1024)
        print(f"\n📁 File size: {file_size_mb:.1f} MB")
    except:
        pass
    
    return long_df

def quick_analysis(csv_file="taiwan_stocks_long_format.csv"):
    """
    Quick analysis of the converted CSV data
    """
    print("🔍 Loading CSV for quick analysis...")
    df = pd.read_csv(csv_file)
    
    print(f"\n📊 Quick Analysis:")
    print(f"   Dataset shape: {df.shape}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # Top 10 stocks by data points
    print(f"\n🏆 Top 10 stocks by data availability:")
    top_stocks = df['Stock'].value_counts().head(10)
    for stock, count in top_stocks.items():
        print(f"   {stock}: {count:,} data points")
    
    # Sample stock analysis
    sample_stock = top_stocks.index[0]
    sample_data = df[df['Stock'] == sample_stock]
    print(f"\n📈 Sample analysis for {sample_stock}:")
    print(f"   Date range: {sample_data['Date'].min()} to {sample_data['Date'].max()}")
    print(f"   Price range: {sample_data['Price'].min():.2f} to {sample_data['Price'].max():.2f}")
    print(f"   Average price: {sample_data['Price'].mean():.2f}")

if __name__ == "__main__":
    # Main conversion
    file_path = "stock price.xlsx"  # Update this path if needed
    
    try:
        # Convert to CSV
        long_data = convert_wide_to_long_csv(file_path)
        
        # Optional: Run quick analysis
        print("\n" + "="*50)
        quick_analysis()
        
        print("\n🎉 Conversion completed successfully!")
        print("📄 Your CSV file is ready to use for analysis!")
        
    except FileNotFoundError:
        print("❌ Error: Could not find 'stock price.xlsx'")
        print("   Make sure the file is in the same directory as this script")
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        print("   Please check your data file and try again")