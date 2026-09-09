"""
SUTRA-X Data Loader - Reads all 5 real datasets
Location: app/frontend/streamlit/utils/data_loader.py
"""

import pandas as pd
import json
import os
import re
from pathlib import Path

class RealDataLoader:
    """Loads all 5 real datasets for criminal network analysis"""
    
    def __init__(self):
        self.datasets = {}
        self.entities = []
        self.relationships = []
        self.project_root = Path(__file__).parent.parent.parent.parent
    
    def get_dataset_path(self, folder_name):
        """Get correct path to datasets folder"""
        return self.project_root / "datasets" / folder_name
    
    def load_ilsi_dataset(self):
        """Load ILSI: 66,090 Indian court cases with IPC sections"""
        print("📂 Loading ILSI Dataset (66,090 cases)...")
        
        try:
            # Try to find cases.json in various locations
            possible_paths = [
                self.get_dataset_path("ilsil") / "data" / "cases.json",
                self.get_dataset_path("ilsil") / "cases.json",
                self.project_root / "LeSICiN" / "data" / "cases.json",
                self.project_root / "LeSICiN" / "cases.json",
            ]
            
            file_path = None
            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                cases = []
                # Handle different JSON structures
                if isinstance(data, list):
                    for case in data[:5000]:
                        cases.append({
                            'case_id': case.get('id', f"CASE_{len(cases)}"),
                            'facts': case.get('fact', case.get('text', '')),
                            'ipc_sections': case.get('labels', case.get('ipc_sections', [])),
                            'source': 'ILSI'
                        })
                elif isinstance(data, dict):
                    for key, case in data.items():
                        if isinstance(case, dict):
                            cases.append({
                                'case_id': case.get('id', key),
                                'facts': case.get('fact', case.get('text', '')),
                                'ipc_sections': case.get('labels', case.get('ipc_sections', [])),
                                'source': 'ILSI'
                            })
                
                print(f"✅ Loaded {len(cases)} ILSI cases")
                self.datasets['ilsi'] = cases
                return cases
            else:
                print("⚠️ ILSI files not found. Download from GitHub.")
                print("Run: git clone https://github.com/Law-AI/LeSICiN.git datasets/ilsil")
                return []
                
        except Exception as e:
            print(f"❌ Error loading ILSI: {e}")
            return []
    
    def load_ncrb_cyber_data(self):
        """Load NCRB Cyber Crime Data (15 years)"""
        print("📂 Loading NCRB Cyber Crime Dataset...")
        
        try:
            possible_paths = [
                self.get_dataset_path("ncrb") / "cyber_crime_india.csv",
                self.get_dataset_path("ncrb") / "cybercrime.csv",
                self.get_dataset_path("ncrb") / "NCRB_Cyber_Crime.csv",
            ]
            
            file_path = None
            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break
            
            if file_path:
                df = pd.read_csv(file_path)
                print(f"✅ Loaded {len(df)} NCRB records")
                self.datasets['ncrb'] = df
                return df
            else:
                print("⚠️ NCRB file not found. Download from Kaggle.")
                print("Download from: https://www.kaggle.com/datasets/rajatkumar123/indian-cyber-crime-data")
                return None
                
        except Exception as e:
            print(f"❌ Error loading NCRB: {e}")
            return None
    
    def load_scam_hinglish(self):
        """Load India Cyber Scam Hinglish Dataset"""
        print("📂 Loading Scam Hinglish Dataset...")
        
        try:
            possible_paths = [
                self.get_dataset_path("scam_hinglish") / "scam_hinglish.csv",
                self.get_dataset_path("scam_hinglish") / "scam.csv",
                self.get_dataset_path("scam_hinglish") / "data.csv",
            ]
            
            file_path = None
            for path in possible_paths:
                if path.exists():
                    file_path = path
                    break
            
            if file_path:
                df = pd.read_csv(file_path)
                print(f"✅ Loaded {len(df)} scam records")
                self.datasets['scam_hinglish'] = df
                return df
            else:
                print("⚠️ Scam Hinglish file not found.")
                print("Download from: https://www.kaggle.com/datasets/ashishkumar123/india-cyber-scam-hinglish")
                return None
                
        except Exception as e:
            print(f"❌ Error loading scam data: {e}")
            return None
    
    def load_multi_scam(self):
        """Load Multi-Class Scam Classification Dataset from Hugging Face"""
        print("📂 Loading Multi-Class Scam Dataset...")
        
        try:
            from datasets import load_dataset
            dataset = load_dataset("Shade63/scam-classification-multiclass")
            print(f"✅ Loaded {len(dataset['train'])} scam messages")
            self.datasets['multi_scam'] = dataset
            return dataset
        except Exception as e:
            print(f"❌ Error loading multi-scam: {e}")
            print("Make sure: pip install datasets huggingface-hub")
            return None
    
    def extract_entities_from_text(self, text):
        """Extract entities like names, places, IPC sections from text"""
        entities = []
        
        if not text or not isinstance(text, str):
            return entities
        
        # IPC sections (e.g., IPC 420, Section 420, 420 IPC)
        ipc_patterns = [
            r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})',
            r'(\d{1,3})\s*(?:IPC|of IPC)',
        ]
        for pattern in ipc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'IPC_SECTION',
                    'value': f"IPC-{match}",
                    'source': 'ILSI'
                })
        
        # Indian names (capitalized words)
        name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        matches = re.findall(name_pattern, text)
        for first, last in matches[:10]:
            if len(first) > 1 and len(last) > 1 and first not in ['The', 'And', 'For', 'With', 'From']:
                entities.append({
                    'type': 'PERSON',
                    'value': f"{first} {last}",
                    'source': 'ILSI'
                })
        
        # Indian cities
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 
                  'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
                  'Nagpur', 'Indore', 'Bhopal', 'Visakhapatnam', 'Patna']
        for city in cities:
            if city in text:
                entities.append({
                    'type': 'LOCATION',
                    'value': city,
                    'source': 'ILSI'
                })
        
        return entities
    
    def process_all_data(self):
        """Process all loaded datasets into entities and relationships"""
        print("🔄 Processing all datasets...")
        
        all_entities = []
        all_relationships = []
        
        # Process ILSI cases
        if 'ilsi' in self.datasets:
            cases = self.datasets['ilsi']
            
            for case in cases[:5000]:
                case_id = case.get('case_id', f"CASE_{len(all_entities)}")
                
                # Add case as entity
                all_entities.append({
                    'id': case_id,
                    'type': 'CASE',
                    'name': case_id,
                    'facts': case.get('facts', '')[:200],
                    'source': 'ILSI'
                })
                
                # IPC sections
                ipc_sections = case.get('ipc_sections', [])
                if isinstance(ipc_sections, str):
                    ipc_sections = re.findall(r'\d+', ipc_sections)
                
                for ipc in ipc_sections[:5]:
                    if ipc:
                        ipc_id = f"IPC-{ipc}"
                        all_entities.append({
                            'id': ipc_id,
                            'type': 'IPC_SECTION',
                            'name': f"Section {ipc}",
                            'source': 'ILSI'
                        })
                        all_relationships.append({
                            'source': case_id,
                            'target': ipc_id,
                            'type': 'CITES',
                            'source_type': 'ILSI'
                        })
                
                # Extract entities from facts
                facts = case.get('facts', '')
                extracted = self.extract_entities_from_text(facts)
                for ent in extracted:
                    entity_id = f"{ent['type']}_{ent['value'].replace(' ', '_')}"
                    all_entities.append({
                        'id': entity_id,
                        'type': ent['type'],
                        'name': ent['value'],
                        'source': ent['source']
                    })
                    all_relationships.append({
                        'source': case_id,
                        'target': entity_id,
                        'type': 'MENTIONS',
                        'source_type': ent['source']
                    })
        
        # Process NCRB data
        if 'ncrb' in self.datasets:
            df = self.datasets['ncrb']
            for _, row in df.head(1000).iterrows():
                state = str(row.get('State', row.get('state', 'Unknown')))
                if state != 'Unknown' and state != 'nan':
                    state_id = f"LOC_{state.replace(' ', '_')}"
                    all_entities.append({
                        'id': state_id,
                        'type': 'LOCATION',
                        'name': state,
                        'source': 'NCRB'
                    })
                    
                    crime_type = str(row.get('Crime_Type', row.get('crime_type', 'Unknown')))
                    if crime_type != 'Unknown' and crime_type != 'nan':
                        crime_id = f"CRIME_{crime_type.replace(' ', '_')}"
                        all_entities.append({
                            'id': crime_id,
                            'type': 'CRIME_TYPE',
                            'name': crime_type,
                            'source': 'NCRB'
                        })
                        all_relationships.append({
                            'source': state_id,
                            'target': crime_id,
                            'type': 'HAS_CRIME',
                            'source_type': 'NCRB'
                        })
        
        # Process Scam data
        if 'scam_hinglish' in self.datasets:
            df = self.datasets['scam_hinglish']
            for _, row in df.head(500).iterrows():
                scam_type = str(row.get('scam_type', row.get('type', 'Unknown')))
                if scam_type != 'Unknown' and scam_type != 'nan':
                    scam_id = f"SCAM_{scam_type.replace(' ', '_')}"
                    all_entities.append({
                        'id': scam_id,
                        'type': 'SCAM_TYPE',
                        'name': scam_type,
                        'source': 'ScamHinglish'
                    })
        
        print(f"✅ Processed {len(all_entities)} entities and {len(all_relationships)} relationships")
        
        self.entities = all_entities
        self.relationships = all_relationships
        return all_entities, all_relationships
    
    def get_summary(self):
        """Get summary of loaded datasets"""
        summary = {}
        for name, data in self.datasets.items():
            if name == 'ilsi':
                summary[name] = f"{len(data)} cases"
            elif name == 'ncrb':
                summary[name] = f"{len(data)} records"
            elif name == 'scam_hinglish':
                summary[name] = f"{len(data)} records"
            elif name == 'multi_scam':
                summary[name] = f"{len(data['train'])} messages"
            elif name == 'hifire':
                summary[name] = "Loaded"
            else:
                summary[name] = "Unknown"
        return summary