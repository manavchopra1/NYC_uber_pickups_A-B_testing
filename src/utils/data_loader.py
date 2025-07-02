"""
NYC Uber Pickups Data Loader Utility
Author: Manav Chopra
Date: July 2024

This module provides utilities for loading and preprocessing the NYC Uber pickups dataset
for A/B testing analysis.
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class NYCUberDataLoader:
    """
    A comprehensive data loader for NYC Uber pickups dataset.
    
    This class handles loading, preprocessing, and feature engineering for
    the various A/B testing experiments planned for this project.
    """
    
    def __init__(self, data_path: str = 'data/raw/'):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the raw data directory
        """
        self.data_path = data_path
        self.nyc_boroughs = {
            'Manhattan': {'lat': (40.7, 40.8), 'lon': (-74.0, -73.9)},
            'Brooklyn': {'lat': (40.6, 40.7), 'lon': (-74.0, -73.9)},
            'Queens': {'lat': (40.7, 40.8), 'lon': (-73.9, -73.7)},
            'Bronx': {'lat': (40.8, 40.9), 'lon': (-73.9, -73.8)},
            'Staten Island': {'lat': (40.5, 40.6), 'lon': (-74.2, -74.0)}
        }
        
    def get_available_files(self) -> Dict[str, str]:
        """
        Get a list of all available CSV files in the data directory.
        
        Returns:
            Dictionary mapping service names to file paths
        """
        files = glob.glob(os.path.join(self.data_path, '*.csv'))
        file_mapping = {}
        
        for file in files:
            filename = os.path.basename(file)
            if 'uber-raw-data' in filename:
                # Extract month and year from filename
                if 'janjune-15' in filename:
                    service_name = 'Uber_JanJune_2015'
                else:
                    # Extract month and year from other uber files
                    parts = filename.replace('.csv', '').split('-')
                    if len(parts) >= 4:
                        month = parts[-2]
                        year = parts[-1]
                        service_name = f'Uber_{month}_{year}'
                    else:
                        service_name = 'Uber_Other'
            elif 'other-' in filename:
                # Extract service name from other files
                service_name = filename.replace('other-', '').replace('.csv', '')
            else:
                service_name = filename.replace('.csv', '')
                
            file_mapping[service_name] = file
            
        return file_mapping
    
    def load_uber_data(self, months: Optional[List[str]] = None, 
                      sample_size: Optional[int] = None) -> pd.DataFrame:
        """
        Load Uber data for specified months or all available months.
        
        Args:
            months: List of months to load (e.g., ['apr14', 'may14'])
            sample_size: If provided, load only this many rows per file
            
        Returns:
            Combined DataFrame with Uber data
        """
        print("🚗 Loading Uber pickup data...")
        
        uber_files = self.get_available_files()
        uber_files = {k: v for k, v in uber_files.items() if 'Uber' in k}
        
        if months:
            # Filter files based on requested months
            filtered_files = {}
            for month in months:
                for name, path in uber_files.items():
                    if month.lower() in name.lower():
                        filtered_files[name] = path
            uber_files = filtered_files
        
        all_data = []
        total_records = 0
        
        for service_name, file_path in uber_files.items():
            try:
                print(f"📁 Loading {service_name}...")
                
                if sample_size:
                    df = pd.read_csv(file_path, nrows=sample_size)
                else:
                    df = pd.read_csv(file_path)
                
                # Add service identifier
                df['service'] = service_name
                df['source_file'] = os.path.basename(file_path)
                
                all_data.append(df)
                total_records += len(df)
                
                print(f"   ✅ Loaded {len(df):,} records")
                
            except Exception as e:
                print(f"   ❌ Error loading {service_name}: {e}")
        
        if not all_data:
            raise ValueError("No Uber data files could be loaded!")
        
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        print(f"\n🎯 Total Uber records loaded: {total_records:,}")
        
        return combined_df
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the loaded data with feature engineering.
        
        Args:
            df: Raw DataFrame from load_uber_data
            
        Returns:
            Preprocessed DataFrame with engineered features
        """
        print("🔧 Preprocessing data and engineering features...")
        
        # Make a copy to avoid modifying original
        df_processed = df.copy()
        
        # Convert datetime
        df_processed['Date/Time'] = pd.to_datetime(df_processed['Date/Time'])
        
        # Extract temporal features
        df_processed['hour'] = df_processed['Date/Time'].dt.hour
        df_processed['day_of_week'] = df_processed['Date/Time'].dt.day_name()
        df_processed['day_of_week_num'] = df_processed['Date/Time'].dt.weekday
        df_processed['month'] = df_processed['Date/Time'].dt.month
        df_processed['year'] = df_processed['Date/Time'].dt.year
        df_processed['date'] = df_processed['Date/Time'].dt.date
        df_processed['is_weekend'] = df_processed['Date/Time'].dt.weekday >= 5
        
        # Time period features for A/B testing
        df_processed['is_friday_evening'] = (
            (df_processed['day_of_week'] == 'Friday') & 
            (df_processed['hour'] >= 18) & 
            (df_processed['hour'] <= 23)
        )
        
        df_processed['is_weekday_evening'] = (
            (df_processed['day_of_week'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday'])) & 
            (df_processed['hour'] >= 18) & 
            (df_processed['hour'] <= 23)
        )
        
        df_processed['is_late_night'] = (
            (df_processed['hour'] >= 0) & 
            (df_processed['hour'] < 4)
        )
        
        df_processed['is_early_morning'] = (
            (df_processed['hour'] >= 6) & 
            (df_processed['hour'] < 10)
        )
        
        # Geographic features
        df_processed['borough'] = df_processed.apply(
            lambda x: self._assign_borough(x['Lat'], x['Lon']), axis=1
        )
        
        # Business hour features
        df_processed['is_business_hours'] = (
            (df_processed['hour'] >= 9) & 
            (df_processed['hour'] <= 17) & 
            (~df_processed['is_weekend'])
        )
        
        # Peak hour features
        df_processed['is_peak_hour'] = (
            (df_processed['hour'] >= 7) & (df_processed['hour'] <= 9) |  # Morning peak
            (df_processed['hour'] >= 17) & (df_processed['hour'] <= 19)   # Evening peak
        )
        
        print("✅ Feature engineering completed!")
        print(f"   • Temporal features: hour, day_of_week, is_weekend, etc.")
        print(f"   • Geographic features: borough assignment")
        print(f"   • Business features: peak_hours, business_hours, etc.")
        
        return df_processed
    
    def _assign_borough(self, lat: float, lon: float) -> str:
        """
        Assign NYC borough based on coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Borough name or 'Other'
        """
        for borough, bounds in self.nyc_boroughs.items():
            if (bounds['lat'][0] <= lat <= bounds['lat'][1] and 
                bounds['lon'][0] <= lon <= bounds['lon'][1]):
                return borough
        return 'Other'
    
    def get_ab_test_data(self, test_type: str, 
                        sample_size: Optional[int] = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Get data specifically formatted for different A/B tests.
        
        Args:
            test_type: Type of A/B test ('rainy_clear', 'friday_night', 'manhattan_brooklyn')
            sample_size: Optional sample size for testing
            
        Returns:
            Tuple of (processed_data, test_config)
        """
        print(f"🎯 Preparing data for A/B Test: {test_type}")
        
        if test_type == 'rainy_clear':
            # For rainy vs clear days - need weather data
            df = self.load_uber_data(sample_size=sample_size)
            df = self.preprocess_data(df)
            
            # Group by date for daily analysis
            daily_data = df.groupby('date').agg({
                'service': 'count',
                'is_weekend': 'first',
                'month': 'first',
                'year': 'first'
            }).reset_index()
            daily_data.rename(columns={'service': 'pickup_count'}, inplace=True)
            
            test_config = {
                'treatment_group': 'rainy_days',  # Will be defined when weather data is added
                'control_group': 'clear_days',
                'metric': 'pickup_count',
                'test_type': 'two_sample_t_test'
            }
            
        elif test_type == 'friday_night':
            # Friday evening vs other weekday evenings
            df = self.load_uber_data(sample_size=sample_size)
            df = self.preprocess_data(df)
            
            # Filter for evening hours only
            evening_data = df[
                (df['hour'] >= 18) & (df['hour'] <= 23)
            ].copy()
            
            test_config = {
                'treatment_group': 'friday_evening',
                'control_group': 'weekday_evening',
                'metric': 'pickup_count',
                'test_type': 'two_sample_t_test'
            }
            
        elif test_type == 'manhattan_brooklyn':
            # Manhattan vs Brooklyn comparison
            df = self.load_uber_data(sample_size=sample_size)
            df = self.preprocess_data(df)
            
            # Filter for Manhattan and Brooklyn only
            borough_data = df[
                df['borough'].isin(['Manhattan', 'Brooklyn'])
            ].copy()
            
            test_config = {
                'treatment_group': 'Manhattan',
                'control_group': 'Brooklyn',
                'metric': 'pickup_count',
                'test_type': 'two_sample_t_test'
            }
            
        else:
            raise ValueError(f"Unknown test type: {test_type}. Available: 'rainy_clear', 'friday_night', 'manhattan_brooklyn'")
        
        print(f"✅ Data prepared for {test_type} A/B test")
        return df, test_config
    
    def get_data_summary(self) -> Dict:
        """
        Get a comprehensive summary of the available data.
        
        Returns:
            Dictionary with data summary statistics
        """
        print("📊 Generating data summary...")
        
        files = self.get_available_files()
        
        summary = {
            'total_files': len(files),
            'file_details': {},
            'total_records': 0,
            'date_range': None,
            'services': []
        }
        
        # Load a sample from each file to get basic info
        for service_name, file_path in files.items():
            try:
                # Get file size
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                
                # Get row count (quick method)
                with open(file_path, 'r') as f:
                    row_count = sum(1 for line in f) - 1  # Subtract header
                
                summary['file_details'][service_name] = {
                    'file_path': file_path,
                    'size_mb': round(file_size, 2),
                    'rows': row_count
                }
                
                summary['total_records'] += row_count
                summary['services'].append(service_name)
                
            except Exception as e:
                print(f"Error processing {service_name}: {e}")
        
        # Get date range from a sample file
        try:
            sample_df = pd.read_csv(list(files.values())[0], nrows=1000)
            sample_df['Date/Time'] = pd.to_datetime(sample_df['Date/Time'])
            summary['date_range'] = {
                'start': sample_df['Date/Time'].min().strftime('%Y-%m-%d'),
                'end': sample_df['Date/Time'].max().strftime('%Y-%m-%d')
            }
        except:
            summary['date_range'] = {'start': 'Unknown', 'end': 'Unknown'}
        
        return summary


# Convenience functions for quick access
def load_sample_data(sample_size: int = 10000) -> pd.DataFrame:
    """
    Quick function to load a sample of Uber data for testing.
    
    Args:
        sample_size: Number of records to load
        
    Returns:
        Preprocessed sample DataFrame
    """
    loader = NYCUberDataLoader()
    df = loader.load_uber_data(sample_size=sample_size)
    return loader.preprocess_data(df)


def get_data_summary() -> Dict:
    """
    Quick function to get data summary.
    
    Returns:
        Data summary dictionary
    """
    loader = NYCUberDataLoader()
    return loader.get_data_summary()


if __name__ == "__main__":
    # Test the data loader
    print("🧪 Testing NYC Uber Data Loader...")
    
    loader = NYCUberDataLoader()
    summary = loader.get_data_summary()
    
    print(f"\n📊 Data Summary:")
    print(f"Total files: {summary['total_files']}")
    print(f"Total records: {summary['total_records']:,}")
    print(f"Date range: {summary['date_range']['start']} to {summary['date_range']['end']}")
    print(f"Services: {', '.join(summary['services'][:5])}...")
    
    print("\n✅ Data loader test completed!") 