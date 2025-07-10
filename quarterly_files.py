import pandas as pd
import numpy as np

def fix_quarterly_data_files():
    """
    Fix the column naming issue in quarterly data files
    """
    
    print("🔧 Fixing quarterly data files...")
    
    # Fix announcement dates
    print("\n📅 Fixing announcement dates file...")
    try:
        # Read the original Excel file properly
        df_announce = pd.read_excel("announcemnet date.xlsx")
        
        # The issue: first row contains headers, second row contains actual column names
        # Let's fix this properly
        
        # Get the actual column names from row 2 (index 1)
        actual_columns = df_announce.iloc[0].values  # This should be ['年/月', '1101 台泥', '1102 亞泥', ...]
        
        # Get the data starting from row 3 (index 2)
        data_rows = df_announce.iloc[1:].reset_index(drop=True)
        data_rows.columns = actual_columns
        
        print(f"Found {len(data_rows)} periods and {len(actual_columns)-1} stocks")
        
        # Now convert to long format properly
        date_col = actual_columns[0]  # Should be '年/月'
        stock_cols = actual_columns[1:]
        
        long_df = data_rows.melt(
            id_vars=[date_col],
            value_vars=stock_cols,
            var_name='Stock',
            value_name='AnnouncementDate'
        )
        
        # Rename and clean
        long_df = long_df.rename(columns={date_col: 'Date'})
        long_df = long_df.dropna(subset=['AnnouncementDate'])
        long_df = long_df[long_df['AnnouncementDate'] != '-']
        long_df = long_df[long_df['AnnouncementDate'] != '']
        
        # Save fixed file
        long_df.to_csv("announcement_dates_fixed.csv", index=False)
        print(f"✅ Fixed announcement dates: {len(long_df):,} rows saved")
        print("Sample data:")
        print(long_df.head(3))
        
    except Exception as e:
        print(f"❌ Error fixing announcement dates: {e}")
    
    # Fix book values
    print("\n💰 Fixing book values file...")
    try:
        # Read the original Excel file properly
        df_book = pd.read_excel("book value.xlsx")
        
        # Same fix as above
        actual_columns = df_book.iloc[0].values
        data_rows = df_book.iloc[1:].reset_index(drop=True)
        data_rows.columns = actual_columns
        
        print(f"Found {len(data_rows)} periods and {len(actual_columns)-1} stocks")
        
        # Convert to long format
        date_col = actual_columns[0]
        stock_cols = actual_columns[1:]
        
        long_df = data_rows.melt(
            id_vars=[date_col],
            value_vars=stock_cols,
            var_name='Stock',
            value_name='BookValue'
        )
        
        # Rename and clean
        long_df = long_df.rename(columns={date_col: 'Date'})
        long_df = long_df.dropna(subset=['BookValue'])
        long_df = long_df[long_df['BookValue'] != '-']
        long_df = long_df[long_df['BookValue'] != '']
        
        # Clean numeric values (remove commas)
        long_df['BookValue'] = long_df['BookValue'].astype(str).str.replace(',', '')
        long_df['BookValue'] = pd.to_numeric(long_df['BookValue'], errors='coerce')
        long_df = long_df.dropna(subset=['BookValue'])
        
        # Save fixed file
        long_df.to_csv("book_values_fixed.csv", index=False)
        print(f"✅ Fixed book values: {len(long_df):,} rows saved")
        print("Sample data:")
        print(long_df.head(3))
        
        # Show some statistics
        print(f"\n📊 Book Value Statistics:")
        print(f"   Min: {long_df['BookValue'].min():,.0f}")
        print(f"   Max: {long_df['BookValue'].max():,.0f}")
        print(f"   Mean: {long_df['BookValue'].mean():,.0f}")
        
    except Exception as e:
        print(f"❌ Error fixing book values: {e}")

def verify_daily_files():
    """
    Quick verification that daily files (TV, Market Cap) converted correctly
    """
    print("\n🔍 Verifying daily data files...")
    
    files_to_check = [
        "tv_volume_long_format.csv",
        "mkt cap_market_cap_long_format.csv"
    ]
    
    for filename in files_to_check:
        try:
            df = pd.read_csv(filename)
            print(f"\n📊 {filename}:")
            print(f"   Rows: {len(df):,}")
            print(f"   Columns: {list(df.columns)}")
            print(f"   Unique dates: {df['Date'].nunique()}")
            print(f"   Unique stocks: {df['Stock'].nunique()}")
            print("   Sample:")
            print(df.head(2))
            
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")

if __name__ == "__main__":
    print("🔧 Taiwan Stock Data - Fix Column Issues")
    print("=" * 50)
    
    # Fix the quarterly data files
    fix_quarterly_data_files()
    
    # Verify daily files are okay
    verify_daily_files()
    
    print("\n🎉 All files should now be properly formatted!")
    print("\nYour corrected files:")
    print("✅ announcement_dates_fixed.csv")
    print("✅ book_values_fixed.csv") 
    print("✅ tv_volume_long_format.csv (if exists)")
    print("✅ mkt cap_market_cap_long_format.csv (if exists)")