"""
Sample Data Generator
"""

import random
import sys
from pathlib import Path

# Try to import networkx
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

def generate_sample_network():
    """Generate sample criminal network with Indian data"""
    
    if NETWORKX_AVAILABLE:
        G = nx.Graph()
    else:
        # Simple fallback graph
        G = SimpleGraph()
    
    first_names = ['Raj', 'Amit', 'Priya', 'Suresh', 'Anita', 'Vikram', 'Neha', 'Rahul', 
                   'Sunita', 'Mohan', 'Geeta', 'Arjun', 'Kavita', 'Deepak', 'Anjali', 
                   'Sanjay', 'Meera', 'Ravi', 'Pooja', 'Kumar', 'Ashok', 'Preeti',
                   'Vijay', 'Nisha', 'Ramesh', 'Sneha', 'Mahesh', 'Jyoti']
    
    last_names = ['Sharma', 'Singh', 'Patel', 'Reddy', 'Rao', 'Joshi', 'Gupta', 'Verma', 
                  'Kumar', 'Nair', 'Mehta', 'Choudhary', 'Yadav', 'Khan', 'Das']
    
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
    
    # Generate persons with coordinates
    persons = []
    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        person_id = f"P-{i+1:04d}"
        G.add_node(person_id, type='PERSON', name=name, 
                   age=random.randint(22, 60),
                   city=random.choice(locations),
                   occupation=random.choice(['Business', 'Student', 'Government', 'Private', 'Professional']),
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        persons.append(person_id)
    
    # Phones
    phones = []
    for i in range(20):
        phone_id = f"PH-{i+1:04d}"
        number = f"98{random.randint(10000000, 99999999)}"
        G.add_node(phone_id, type='PHONE', number=number)
        phones.append(phone_id)
        owner = random.choice(persons)
        G.add_edge(owner, phone_id, type='OWNS', confidence=0.8)
    
    # Accounts
    accounts = []
    for i in range(15):
        account_id = f"ACC-{i+1:04d}"
        G.add_node(account_id, type='ACCOUNT', bank=random.choice(['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB']))
        accounts.append(account_id)
        owner = random.choice(persons)
        G.add_edge(owner, account_id, type='OWNS', confidence=0.7)
    
    # Vehicles
    vehicles = []
    prefixes = ['MH', 'DL', 'KA', 'TN', 'TS', 'GJ', 'UP']
    for i in range(10):
        vehicle_id = f"V-{i+1:04d}"
        reg = f"{random.choice(prefixes)}{random.randint(1,99)} {random.choice(['AB','CD','EF','GH'])}{random.randint(1000,9999)}"
        G.add_node(vehicle_id, type='VEHICLE', registration=reg,
                   make=random.choice(['Maruti', 'Hyundai', 'Toyota', 'Honda', 'Tata']))
        vehicles.append(vehicle_id)
        owner = random.choice(persons)
        G.add_edge(owner, vehicle_id, type='OWNS', confidence=0.6)
    
    # Locations with coordinates
    locs = []
    loc_names = ['Connaught Place', 'Bandra West', 'Indiranagar', 'T. Nagar', 'Hitech City', 
                 'Juhu', 'Koramangala', 'Marine Drive']
    for i in range(8):
        loc_id = f"L-{i+1:04d}"
        G.add_node(loc_id, type='LOCATION', 
                   name=loc_names[i % len(loc_names)],
                   city=random.choice(locations),
                   latitude=8.4 + random.random() * 29.2,
                   longitude=68.7 + random.random() * 28.6)
        locs.append(loc_id)
    
    # Cases
    cases = []
    case_titles = ['Drug Trafficking Ring', 'Financial Fraud Network', 'Arms Dealing', 
                   'Cyber Crime Syndicate', 'Money Laundering', 'Human Trafficking']
    for i in range(6):
        case_id = f"CASE-{i+1:03d}"
        G.add_node(case_id, type='CASE', 
                   title=case_titles[i % len(case_titles)],
                   status=random.choice(['Active', 'Pending', 'Under Review']))
        cases.append(case_id)
        for _ in range(random.randint(2, 5)):
            person = random.choice(persons)
            G.add_edge(case_id, person, type='INVOLVED', confidence=0.6 + random.random()*0.3)
    
    # CDR Calls
    for _ in range(30):
        caller = random.choice(phones)
        receiver = random.choice(phones)
        if caller != receiver:
            G.add_edge(caller, receiver, type='CALLED', duration=random.randint(30, 600))
    
    # Transactions
    for _ in range(25):
        from_acc = random.choice(accounts)
        to_acc = random.choice(accounts)
        if from_acc != to_acc:
            G.add_edge(from_acc, to_acc, type='TRANSACTION', amount=random.randint(5000, 500000))
    
    # Visits
    for _ in range(20):
        person = random.choice(persons)
        loc = random.choice(locs)
        G.add_edge(person, loc, type='VISITED')
    
    # Cross-case connections
    for _ in range(8):
        person = random.choice(persons)
        case = random.choice(cases)
        G.add_edge(person, case, type='INVOLVED', confidence=0.5 + random.random()*0.4)
    
    # Hidden connections
    hidden_pairs = [('P-0001', 'P-0015'), ('PH-0003', 'PH-0018'), ('ACC-0002', 'ACC-0012')]
    for src, tgt in hidden_pairs:
        if src in G.nodes and tgt in G.nodes and not G.has_edge(src, tgt):
            G.add_edge(src, tgt, type='HIDDEN_CONNECTION', confidence=0.7, hidden=True)
    
    return G

# Simple fallback graph if networkx is not available
class SimpleGraph:
    def __init__(self):
        self._nodes = {}
        self._adj = {}
        self._edges = {}
    
    def add_node(self, node, **attrs):
        self._nodes[node] = attrs
        if node not in self._adj:
            self._adj[node] = {}
    
    def add_edge(self, u, v, **attrs):
        if u not in self._adj:
            self._adj[u] = {}
        if v not in self._adj:
            self._adj[v] = {}
        self._adj[u][v] = attrs
        self._adj[v][u] = attrs
        self._edges[(u, v)] = attrs
    
    def neighbors(self, node):
        return list(self._adj.get(node, {}).keys())
    
    def degree(self, node):
        return len(self._adj.get(node, {}))
    
    @property
    def nodes(self):
        return self._nodes
    
    @property
    def edges(self):
        return self._edges
    
    def number_of_nodes(self):
        return len(self._nodes)
    
    def number_of_edges(self):
        return len(self._edges)
    
    def has_edge(self, u, v):
        return (u, v) in self._edges or (v, u) in self._edges
    
    def get_edge_data(self, u, v):
        if (u, v) in self._edges:
            return self._edges[(u, v)]
        if (v, u) in self._edges:
            return self._edges[(v, u)]
        return {}
