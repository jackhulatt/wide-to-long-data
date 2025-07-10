import pandas as pd
import numpy as np
import os
from datetime import datetime

def convert_stock_file_to_long(file_path, output_suffix="", value_column_name="Value"):
    """
    Convert any stock data file from wide to long format
    
    Parameters:
    - file_path: Path to the Excel file
    - output_suffix: Suffix to add to output filename (e.g., "_prices", "_volume")
    - value_column_name: Name for the value column (e.g., "Price", "Volume", "MarketCap")
    """
    
    print(f"📊 Converting {file_path}...")
    
    # Read the Excel file
    print("📂 Reading Excel file...")
    df = pd.read_excel(file_path)
    
    # Get column names
    date_col = df.columns[0]  # First column is date/period
    stock_cols = df.columns[1:]  # All other columns are stocks
    
    print(f"📈 Found {len(df)} rows × {len(stock_cols)} stocks")
    print(f"📅 Period range: {df[date_col].min()} to {df[date_col].max()}")
    
    # Convert to long format using pandas melt
    print("🔄 Converting to long format...")
    long_df = df.melt(
        id_vars=[date_col],
        value_vars=stock_cols,
        var_name='Stock',
        value_name=value_column_name
    )
    
    # Rename date column to English
    long_df = long_df.rename(columns={date_col: 'Date'})
    
    # Clean the data
    print("🧹 Cleaning data...")
    initial_rows = len(long_df)
    
    # Remove rows with missing values
    long_df = long_df.dropna(subset=[value_column_name])
    long_df = long_df[long_df[value_column_name] != '-']
    long_df = long_df[long_df[value_column_name] != '']
    
    # Clean numeric data (remove commas from numbers like "63,292,145")
    if long_df[value_column_name].dtype == 'object':
        # Try to clean and convert to numeric
        long_df[value_column_name] = long_df[value_column_name].astype(str).str.replace(',', '')
        # Try to convert to numeric, keeping original if conversion fails
        numeric_values = pd.to_numeric(long_df[value_column_name], errors='coerce')
        # Only replace if we successfully converted most values
        if numeric_values.notna().sum() > len(numeric_values) * 0.8:
            long_df[value_column_name] = numeric_values
            long_df = long_df.dropna(subset=[value_column_name])
    
    # Reset index
    long_df = long_df.reset_index(drop=True)
    
    final_rows = len(long_df)
    removed_rows = initial_rows - final_rows
    
    print(f"🗑️  Removed {removed_rows:,} empty/invalid rows")
    print(f"✅ Conversion complete! {final_rows:,} data points created")
    
    # Generate output filename
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    csv_filename = f"{base_name}{output_suffix}_long_format.csv"
    
    # Save as CSV
    print(f"💾 Saving to {csv_filename}...")
    long_df.to_csv(csv_filename, index=False)
    print(f"✅ CSV file saved successfully!")
    
    # Show summary statistics
    print(f"\n📊 Dataset Summary:")
    print(f"   Total data points: {len(long_df):,}")
    print(f"   Unique stocks: {long_df['Stock'].nunique():,}")
    print(f"   Unique dates/periods: {long_df['Date'].nunique():,}")
    print(f"   Date range: {long_df['Date'].min()} to {long_df['Date'].max()}")
    
    # Show sample data
    print(f"\n📋 Sample of converted data:")
    print(long_df.head(5).to_string(index=False))
    
    # Show value statistics if numeric
    if pd.api.types.is_numeric_dtype(long_df[value_column_name]):
        print(f"\n📈 {value_column_name} Statistics:")
        print(f"   Min: {long_df[value_column_name].min():,.2f}")
        print(f"   Max: {long_df[value_column_name].max():,.2f}")
        print(f"   Mean: {long_df[value_column_name].mean():,.2f}")
        print(f"   Median: {long_df[value_column_name].median():,.2f}")
    
    # Show file size
    try:
        file_size = os.path.getsize(csv_filename)
        file_size_mb = file_size / (1024 * 1024)
        print(f"\n📁 File size: {file_size_mb:.1f} MB")
    except:
        pass
    
    return long_df, csv_filename

def convert_all_stock_files():
    """
    Convert all stock data files to long format
    """
    
    # Define files and their configurations
    files_config = [
        {
            "file": "stock price.xlsx",
            "suffix": "_prices", 
            "value_name": "Price",
            "description": "Stock Prices"
        },
        {
            "file": "tv.xlsx",
            "suffix": "_volume", 
            "value_name": "Volume",
            "description": "Trading Volume"
        },
        {
            "file": "mkt cap.xlsx",
            "suffix": "_market_cap", 
            "value_name": "MarketCap",
            "description": "Market Capitalization"
        },
        {
            "file": "book value.xlsx",
            "suffix": "_book_value", 
            "value_name": "BookValue",
            "description": "Book Value (Quarterly)"
        },
        {
            "file": "announcemnet date.xlsx",  # Note: keeping original spelling
            "suffix": "_announcement", 
            "value_name": "AnnouncementDate",
            "description": "Announcement Dates"
        }
    ]
    
    print("🚀 Starting batch conversion of all stock data files...")
    print("="*60)
    
    results = []
    
    for config in files_config:
        try:
            if os.path.exists(config["file"]):
                print(f"\n📁 Processing: {config['description']}")
                print("-" * 40)
                
                df, filename = convert_stock_file_to_long(
                    config["file"], 
                    config["suffix"], 
                    config["value_name"]
                )
                
                results.append({
                    "original_file": config["file"],
                    "output_file": filename,
                    "description": config["description"],
                    "rows": len(df),
                    "success": True
                })
                
            else:
                print(f"⚠️  File not found: {config['file']}")
                results.append({
                    "original_file": config["file"],
                    "output_file": None,
                    "description": config["description"],
                    "rows": 0,
                    "success": False
                })
                
        except Exception as e:
            print(f"❌ Error processing {config['file']}: {e}")
            results.append({
                "original_file": config["file"],
                "output_file": None,
                "description": config["description"],
                "rows": 0,
                "success": False,
                "error": str(e)
            })
    
    # Summary report
    print("\n" + "="*60)
    print("📋 CONVERSION SUMMARY REPORT")
    print("="*60)
    
    successful = 0
    total_rows = 0
    
    for result in results:
        status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
        rows_text = f"{result['rows']:,} rows" if result["success"] else "0 rows"
        
        print(f"{status} | {result['description']:<25} | {rows_text}")
        if result["success"]:
            print(f"          📄 Output: {result['output_file']}")
            successful += 1
            total_rows += result["rows"]
        elif "error" in result:
            print(f"          ❌ Error: {result['error']}")
    
    print("-" * 60)
    print(f"📊 Summary: {successful}/{len(files_config)} files converted successfully")
    print(f"📈 Total data points created: {total_rows:,}")
    print("\n🎉 Batch conversion completed!")
    
    return results

if __name__ == "__main__":
    print("🔄 Taiwan Stock Data Multi-File Converter")
    print("=" * 50)
    
    # Option 1: Convert all files at once
    convert_all_stock_files()
    
    # Option 2: Convert individual files (uncomment as needed)
    # convert_stock_file_to_long("tv.xlsx", "_volume", "Volume")
    # convert_stock_file_to_long("mkt cap.xlsx", "_market_cap", "MarketCap")
    # convert_stock_file_to_long("book value.xlsx", "_book_value", "BookValue")
    # convert_stock_file_to_long("announcemnet date.xlsx", "_announcement", "AnnouncementDate")