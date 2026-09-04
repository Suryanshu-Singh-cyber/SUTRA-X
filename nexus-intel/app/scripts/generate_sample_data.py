import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta
import names
import os
from pathlib import Path

def generate_sample_data():
    """Generate realistic sample investigation data"""
    
    np.random.seed(42)
    random.seed(42)
    
    # Generate cases
    cases = []
    for i in range(10):
        case = {
            'case_id': f'CASE-{i+1:03d}',
            'case_number': f'CN-2026-{i+1:04d}',
            'title': f'Investigation Case {i+1}',
            'description': f'Sample investigation case {i+1} involving multiple entities',
            'fir_number': f'FIR-{i+1:04d}',
            'police_station': f'Police Station {random.randint(1,10)}',
            'district': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']),
            'state': random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana']),
            'date_registered': datetime.now() - timedelta(days=random.randint(1, 365)),
            'status': random.choice(['active', 'pending', 'closed']),
            'priority': random.choice(['high', 'medium', 'low'])
        }
        cases.append(case)
    
    df_cases = pd.DataFrame(cases)
    
    # Generate persons
    persons = []
    for i in range(50):
        person = {
            'person_id': f'P-{i+1:04d}',
            'name': names.get_full_name(),
            'alias': f'Alias {random.randint(1,5)}' if random.random() > 0.6 else None,
            'gender': random.choice(['M', 'F']),
            'age': random.randint(18, 65),
            'dob': datetime.now() - timedelta(days=random.randint(365*18, 365*65)),
            'address': f'{random.randint(1,100)} Main Street',
            'city': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']),
            'state': random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana']),
            'pincode': f'{random.randint(100000, 999999)}',
            'phone_numbers': f'98{random.randint(10000000, 99999999)}',
            'aadhaar': f'{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}',
            'pan': f'{random.choice(["A","B","C","D","E","F","G","H","I","J"])}{random.choice(["A","B","C","D","E","F","G","H","I","J"])}{random.choice(["A","B","C","D","E","F","G","H","I","J"])}{random.randint(1000,9999)}{random.choice(["A","B","C","D","E","F","G","H","I","J"])}',
            'occupation': random.choice(['Business', 'Student', 'Government', 'Private', 'Unemployed'])
        }
        persons.append(person)
    
    df_persons = pd.DataFrame(persons)
    
    # Generate phones
    phones = []
    for i in range(30):
        phone = {
            'phone_id': f'PH-{i+1:04d}',
            'phone_number': f'98{random.randint(10000000, 99999999)}',
            'owner_id': random.choice(df_persons['person_id'].tolist()),
            'owner_type': 'PERSON',
            'sim_provider': random.choice(['Jio', 'Airtel', 'Vodafone', 'BSNL']),
            'imei1': f'{random.randint(100000, 999999)}-{random.randint(100000, 999999)}-{random.randint(100000, 999999)}',
            'imei2': f'{random.randint(100000, 999999)}-{random.randint(100000, 999999)}-{random.randint(100000, 999999)}',
            'registered_at': datetime.now() - timedelta(days=random.randint(1, 1000)),
            'last_active': datetime.now() - timedelta(days=random.randint(1, 30)),
            'status': random.choice(['active', 'inactive'])
        }
        phones.append(phone)
    
    df_phones = pd.DataFrame(phones)
    
    # Generate CDR data
    cdr = []
    for i in range(100):
        call = {
            'cdr_id': f'CDR-{i+1:05d}',
            'caller_number': random.choice(df_phones['phone_number'].tolist()),
            'receiver_number': random.choice(df_phones['phone_number'].tolist()),
            'call_time': datetime.now() - timedelta(days=random.randint(1, 30), hours=random.randint(0, 23)),
            'duration': random.randint(10, 600),
            'call_type': random.choice(['voice', 'sms', 'data']),
            'tower_location': f'Tower {random.randint(1,50)}',
            'latitude': random.uniform(8.4, 37.6),
            'longitude': random.uniform(68.7, 97.25)
        }
        cdr.append(call)
    
    df_cdr = pd.DataFrame(cdr)
    
    # Generate transactions
    transactions = []
    for i in range(80):
        transaction = {
            'transaction_id': f'TXN-{i+1:05d}',
            'from_account': f'ACC{random.randint(100000, 999999)}',
            'to_account': f'ACC{random.randint(100000, 999999)}',
            'amount': random.uniform(1000, 500000),
            'currency': 'INR',
            'transaction_date': datetime.now() - timedelta(days=random.randint(1, 90)),
            'transaction_type': random.choice(['transfer', 'deposit', 'withdrawal', 'payment']),
            'bank_name': random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']),
            'branch_code': f'BR{random.randint(1000, 9999)}'
        }
        transactions.append(transaction)
    
    df_transactions = pd.DataFrame(transactions)
    
    # Generate vehicles
    vehicles = []
    for i in range(20):
        vehicle = {
            'vehicle_id': f'V-{i+1:04d}',
            'registration_number': f'{random.choice(["MH","DL","KA","TN","TS"])}{random.randint(1,99)} {random.choice(["AB","CD","EF","GH","IJ"])}{random.randint(1000,9999)}',
            'owner_id': random.choice(df_persons['person_id'].tolist()),
            'owner_type': 'PERSON',
            'make': random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata']),
            'model': random.choice(['Swift', 'i20', 'Camry', 'City', 'Nexon']),
            'year': random.randint(2010, 2024),
            'color': random.choice(['White', 'Black', 'Red', 'Blue', 'Silver']),
            'chassis_number': f'CH{random.randint(100000, 999999)}',
            'engine_number': f'EN{random.randint(100000, 999999)}'
        }
        vehicles.append(vehicle)
    
    df_vehicles = pd.DataFrame(vehicles)
    
    # Generate locations
    locations = []
    for i in range(25):
        location = {
            'location_id': f'L-{i+1:04d}',
            'name': f'Location {i+1}',
            'type': random.choice(['house', 'office', 'shop', 'warehouse', 'other']),
            'address': f'{random.randint(1,100)} {random.choice(["Main Road", "Street", "Avenue", "Lane"])}',
            'latitude': random.uniform(8.4, 37.6),
            'longitude': random.uniform(68.7, 97.25),
            'district': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']),
            'state': random.choice(['Maharashtra', 'Delhi', 'Karnataka', 'Tamil Nadu', 'Telangana']),
            'pincode': f'{random.randint(100000, 999999)}'
        }
        locations.append(location)
    
    df_locations = pd.DataFrame(locations)
    
    # Generate reports
    reports = []
    for i in range(40):
        report = {
            'report_id': f'R-{i+1:04d}',
            'case_id': random.choice(df_cases['case_id'].tolist()),
            'report_type': random.choice(['intelligence', 'evidence', 'analysis', 'summary']),
            'report_text': f'Sample report {i+1} containing investigation findings and evidence',
            'source': random.choice(['Field', 'Analysis', 'Informant', 'Surveillance']),
            'date_reported': datetime.now() - timedelta(days=random.randint(1, 60)),
            'priority': random.choice(['high', 'medium', 'low']),
            'status': random.choice(['draft', 'submitted', 'reviewed'])
        }
        reports.append(report)
    
    df_reports = pd.DataFrame(reports)
    
    # Save all dataframes
    data_dir = Path('app/data/raw')
    data_dir.mkdir(parents=True, exist_ok=True)
    
    df_cases.to_csv(data_dir / 'cases.csv', index=False)
    df_persons.to_csv(data_dir / 'persons.csv', index=False)
    df_phones.to_csv(data_dir / 'phones.csv', index=False)
    df_cdr.to_csv(data_dir / 'cdr.csv', index=False)
    df_transactions.to_csv(data_dir / 'transactions.csv', index=False)
    df_vehicles.to_csv(data_dir / 'vehicles.csv', index=False)
    df_locations.to_csv(data_dir / 'locations.csv', index=False)
    df_reports.to_csv(data_dir / 'reports.csv', index=False)
    
    print("✅ Sample data generated successfully!")
    print(f"📁 Data saved to: {data_dir}")
    print(f"Cases: {len(df_cases)}")
    print(f"Persons: {len(df_persons)}")
    print(f"Phones: {len(df_phones)}")
    print(f"CDR Records: {len(df_cdr)}")
    print(f"Transactions: {len(df_transactions)}")
    print(f"Vehicles: {len(df_vehicles)}")
    print(f"Locations: {len(df_locations)}")
    print(f"Reports: {len(df_reports)}")

if __name__ == "__main__":
    generate_sample_data()