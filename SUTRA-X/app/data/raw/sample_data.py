
"""
Sample Data Generator
"""

import random
import networkx as nx
from datetime import datetime, timedelta

def generate_sample_network():
    """Generate sample criminal network"""
    
    G = nx.Graph()
    
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali', 
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das']
    
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune']
    
    # Generate persons
    persons = []
    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations),
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        persons.append(person_id)
    
    # Generate phones
    phones = []
    for i in range(20):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number)
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8)
    
    # Generate accounts
    accounts = []
    for i in range(15):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', bank=random.choice(['SBI', 'HDFC', 'ICICI']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    # Generate vehicles
    vehicles = []
    prefixes = ['MH', 'DL', 'KA', 'TN', 'TS']
    for i in range(10):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg)
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    # Generate locations
    locs = []
    loc_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 'Hitech City']
    for i in range(8):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', name=loc_names[i % len(loc_names)],
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        locs.append(loc_id)
    
    # Generate cases
    cases = []
    case_titles = ['Drug Trafficking', 'Financial Fraud', 'Arms Dealing', 'Cyber Crime', 'Money Laundering']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', title=case_titles[i % len(case_titles)],
                   status=random.choice(['Active', 'Pending', 'Under Review']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    # Generate calls
    for _ in range(30):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', duration=random.randint(30, 600))
    
    # Generate transactions
    for _ in range(25):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            G.add_edge(from_acc, to_acc, type='TRANSACTION', amount=random.randint(5000, 500000))
    
    # Generate visits
    for _ in range(20):
        person = random.choice(persons)
        loc = random.choice(locs)
        G.add_edge(person, loc, type='VISITED')
    
    # Cross-case connections
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
    return G
