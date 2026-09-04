import pandas as pd
import json
import csv
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataLoader:
    """Multi-source data loader with validation and preprocessing"""
    
    def __init__(self):
        self.data_schemas = {
            'cases': ['case_id', 'case_number', 'title', 'description', 
                      'fir_number', 'police_station', 'district', 'state',
                      'date_registered', 'status', 'priority'],
            
            'persons': ['person_id', 'name', 'alias', 'gender', 'age',
                        'dob', 'address', 'city', 'state', 'pincode',
                        'phone_numbers', 'aadhaar', 'pan', 'occupation'],
            
            'phones': ['phone_id', 'phone_number', 'owner_id', 'owner_type',
                       'sim_provider', 'imei1', 'imei2', 'registered_at',
                       'last_active', 'status'],
            
            'cdr': ['cdr_id', 'caller_number', 'receiver_number',
                    'call_time', 'duration', 'call_type', 'tower_location',
                    'latitude', 'longitude'],
            
            'transactions': ['transaction_id', 'from_account', 'to_account',
                             'amount', 'currency', 'transaction_date',
                             'transaction_type', 'bank_name', 'branch_code'],
            
            'vehicles': ['vehicle_id', 'registration_number', 'owner_id',
                         'owner_type', 'make', 'model', 'year', 'color',
                         'chassis_number', 'engine_number'],
            
            'locations': ['location_id', 'name', 'type', 'address',
                          'latitude', 'longitude', 'district', 'state',
                          'pincode'],
            
            'reports': ['report_id', 'case_id', 'report_type', 'report_text',
                        'source', 'date_reported', 'priority', 'status']
        }
    
    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """Load CSV file with auto-detection"""
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            return df
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='latin1')
            return df
        except Exception as e:
            logger.error(f"Error loading {file_path}: {str(e)}")
            raise
    
    def load_json(self, file_path: Path) -> Dict:
        """Load JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_excel(self, file_path: Path) -> pd.DataFrame:
        """Load Excel file"""
        return pd.read_excel(file_path)
    
    def load_multiple_files(self, directory: Path, file_pattern: str = "*.csv") -> Dict[str, pd.DataFrame]:
        """Load all files matching pattern from directory"""
        data = {}
        for file_path in directory.glob(file_pattern):
            name = file_path.stem
            if name in self.data_schemas:
                data[name] = self.load_csv(file_path)
        return data
    
    def validate_schema(self, df: pd.DataFrame, schema_name: str) -> bool:
        """Validate dataframe against schema"""
        if schema_name not in self.data_schemas:
            return True
        
        required_cols = self.data_schemas[schema_name]
        missing_cols = set(required_cols) - set(df.columns)
        
        if missing_cols:
            logger.warning(f"Missing columns for {schema_name}: {missing_cols}")
            return False
        
        return True
    
    def preprocess_dates(self, df: pd.DataFrame, date_columns: List[str]) -> pd.DataFrame:
        """Convert string dates to datetime"""
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
        return df
    
    def clean_phone_numbers(self, df: pd.DataFrame, phone_column: str) -> pd.DataFrame:
        """Standardize phone numbers to 10-digit format"""
        if phone_column in df.columns:
            df[phone_column] = df[phone_column].astype(str).str.replace('[^0-9]', '', regex=True)
            df[phone_column] = df[phone_column].str[-10:]  # Get last 10 digits
        return df
    
    def load_all_data(self, data_dir: Path) -> Dict[str, pd.DataFrame]:
        """Load and preprocess all data from directory"""
        all_data = self.load_multiple_files(data_dir)
        
        # Preprocess each dataframe
        for name, df in all_data.items():
            if name == 'cdr':
                df = self.preprocess_dates(df, ['call_time'])
                df = self.clean_phone_numbers(df, 'caller_number')
                df = self.clean_phone_numbers(df, 'receiver_number')
            elif name == 'transactions':
                df = self.preprocess_dates(df, ['transaction_date'])
            elif name == 'persons':
                df = self.clean_phone_numbers(df, 'phone_numbers')
        
        return all_data

class DataValidator:
    """Data validation and quality checks"""
    
    @staticmethod
    def check_missing_values(df: pd.DataFrame) -> Dict[str, int]:
        """Check for missing values in dataframe"""
        missing = df.isnull().sum().to_dict()
        return {k: v for k, v in missing.items() if v > 0}
    
    @staticmethod
    def check_duplicates(df: pd.DataFrame, key_column: str) -> int:
        """Check for duplicate entries"""
        if key_column in df.columns:
            duplicates = df[key_column].duplicated().sum()
            return duplicates
        return 0
    
    @staticmethod
    def validate_relationships(case_df: pd.DataFrame, person_df: pd.DataFrame) -> Dict:
        """Validate referential integrity between tables"""
        issues = {}
        
        # Check if cases reference valid persons
        if 'case_id' in person_df.columns:
            valid_cases = set(case_df['case_id'])
            case_refs = set(person_df[person_df['case_id'].notna()]['case_id'])
            invalid = case_refs - valid_cases
            if invalid:
                issues['invalid_case_references'] = list(invalid)
        
        return issues