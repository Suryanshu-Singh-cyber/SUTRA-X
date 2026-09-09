"""
SUTRA-X Data Loader – Supports local datasets + dynamic file uploads
"""
import pandas as pd
import json
import os
import re
from pathlib import Path
import io
from datetime import datetime

# OCR support (optional)
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class RealDataLoader:
    def __init__(self):
        self.datasets = {}
        self.entities = []
        self.relationships = []
        self.project_root = Path(__file__).parent.parent.parent.parent  # up to Nexus_intel

    # ---------- Local dataset loading (for real data) ----------
    def load_ilsi_dataset(self):
        """Load ILSI: 66,090 Indian court cases"""
        print("📂 Loading ILSI Dataset...")
        try:
            # Try multiple possible paths
            paths = [
                self.project_root / "datasets" / "ilsil" / "data" / "cases.json",
                self.project_root / "datasets" / "ilsil" / "cases.json",
                self.project_root / "LeSICiN" / "data" / "cases.json",
            ]
            for p in paths:
                if p.exists():
                    with open(p, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    cases = []
                    if isinstance(data, list):
                        for case in data[:5000]:
                            cases.append({
                                'case_id': case.get('id', f"CASE_{len(cases)}"),
                                'facts': case.get('fact', case.get('text', '')),
                                'ipc_sections': case.get('labels', case.get('ipc_sections', []))
                            })
                    elif isinstance(data, dict):
                        for key, case in data.items():
                            if isinstance(case, dict):
                                cases.append({
                                    'case_id': case.get('id', key),
                                    'facts': case.get('fact', case.get('text', '')),
                                    'ipc_sections': case.get('labels', case.get('ipc_sections', []))
                                })
                    self.datasets['ilsi'] = cases
                    print(f"✅ Loaded {len(cases)} ILSI cases")
                    return cases
            print("⚠️ ILSI files not found.")
            return []
        except Exception as e:
            print(f"❌ Error loading ILSI: {e}")
            return []

    def load_ncrb_cyber_data(self):
        """Load NCRB Cyber Crime Data"""
        print("📂 Loading NCRB Cyber Crime Dataset...")
        try:
            paths = [
                self.project_root / "datasets" / "ncrb" / "cyber_crime_india.csv",
                self.project_root / "datasets" / "ncrb" / "cybercrime.csv",
            ]
            for p in paths:
                if p.exists():
                    df = pd.read_csv(p)
                    self.datasets['ncrb'] = df
                    print(f"✅ Loaded {len(df)} NCRB records")
                    return df
            print("⚠️ NCRB file not found.")
            return None
        except Exception as e:
            print(f"❌ Error loading NCRB: {e}")
            return None

    def load_scam_hinglish(self):
        """Load India Cyber Scam Hinglish Dataset"""
        print("📂 Loading Scam Hinglish Dataset...")
        try:
            paths = [
                self.project_root / "datasets" / "scam_hinglish" / "scam_hinglish.csv",
                self.project_root / "datasets" / "scam_hinglish" / "scam.csv",
            ]
            for p in paths:
                if p.exists():
                    df = pd.read_csv(p)
                    self.datasets['scam_hinglish'] = df
                    print(f"✅ Loaded {len(df)} scam records")
                    return df
            print("⚠️ Scam Hinglish file not found.")
            return None
        except Exception as e:
            print(f"❌ Error loading scam: {e}")
            return None

    def load_multi_scam(self):
        """Load Multi-Class Scam Classification (Hugging Face)"""
        print("📂 Loading Multi-Class Scam Dataset...")
        try:
            from datasets import load_dataset
            dataset = load_dataset("Shade63/scam-classification-multiclass")
            self.datasets['multi_scam'] = dataset
            print(f"✅ Loaded {len(dataset['train'])} scam messages")
            return dataset
        except Exception as e:
            print(f"⚠️ Multi-scam not available: {e}")
            return None

    # ---------- Process all local datasets ----------
    def process_all_data(self):
        """Convert loaded datasets to entities + relationships"""
        print("🔄 Processing all datasets...")
        all_entities = []
        all_relationships = []

        # ILSI
        if 'ilsi' in self.datasets:
            for case in self.datasets['ilsi'][:5000]:
                case_id = case.get('case_id', f"CASE_{len(all_entities)}")
                all_entities.append({
                    'id': case_id,
                    'type': 'CASE',
                    'name': case_id,
                    'facts': case.get('facts', '')[:200],
                    'source': 'ILSI'
                })
                ipc = case.get('ipc_sections', [])
                if isinstance(ipc, str):
                    ipc = re.findall(r'\d+', ipc)
                for sec in ipc[:5]:
                    if sec:
                        ipc_id = f"IPC-{sec}"
                        all_entities.append({'id': ipc_id, 'type': 'IPC_SECTION', 'name': f"Section {sec}", 'source': 'ILSI'})
                        all_relationships.append({'source': case_id, 'target': ipc_id, 'type': 'CITES', 'source_type': 'ILSI'})
                # Extract entities from facts
                extracted = self.extract_entities_from_text(case.get('facts', ''))
                for ent in extracted:
                    entity_id = f"{ent['type']}_{ent['value'].replace(' ', '_')}"
                    all_entities.append({'id': entity_id, 'type': ent['type'], 'name': ent['value'], 'source': 'ILSI'})
                    all_relationships.append({'source': case_id, 'target': entity_id, 'type': 'MENTIONS', 'source_type': 'ILSI'})

        # NCRB
        if 'ncrb' in self.datasets:
            df = self.datasets['ncrb']
            for _, row in df.head(1000).iterrows():
                state = str(row.get('State', row.get('state', 'Unknown')))
                if state not in ['Unknown', 'nan']:
                    state_id = f"LOC_{state.replace(' ', '_')}"
                    all_entities.append({'id': state_id, 'type': 'LOCATION', 'name': state, 'source': 'NCRB'})
                    crime = str(row.get('Crime_Type', row.get('crime_type', 'Unknown')))
                    if crime not in ['Unknown', 'nan']:
                        crime_id = f"CRIME_{crime.replace(' ', '_')}"
                        all_entities.append({'id': crime_id, 'type': 'CRIME_TYPE', 'name': crime, 'source': 'NCRB'})
                        all_relationships.append({'source': state_id, 'target': crime_id, 'type': 'HAS_CRIME', 'source_type': 'NCRB'})

        # Scam Hinglish
        if 'scam_hinglish' in self.datasets:
            df = self.datasets['scam_hinglish']
            for _, row in df.head(500).iterrows():
                scam = str(row.get('scam_type', row.get('type', 'Unknown')))
                if scam not in ['Unknown', 'nan']:
                    scam_id = f"SCAM_{scam.replace(' ', '_')}"
                    all_entities.append({'id': scam_id, 'type': 'SCAM_TYPE', 'name': scam, 'source': 'ScamHinglish'})

        print(f"✅ Processed {len(all_entities)} entities and {len(all_relationships)} relationships")
        self.entities = all_entities
        self.relationships = all_relationships
        return all_entities, all_relationships

    # ---------- Dynamic file upload processing ----------
    def detect_file_type(self, file_content, filename):
        filename_lower = filename.lower()
        if 'ilsi' in filename_lower or 'case' in filename_lower:
            return 'ilsi'
        if 'ncrb' in filename_lower or 'cyber' in filename_lower:
            return 'ncrb'
        if 'scam' in filename_lower:
            return 'multi_scam' if 'multi' in filename_lower else 'scam_hinglish'
        if 'cdr' in filename_lower or 'call' in filename_lower:
            return 'cdr'
        if 'transaction' in filename_lower or 'bank' in filename_lower:
            return 'transaction'
        return 'generic'

    def process_uploaded_file(self, file_content, filename, file_extension):
        df = None
        raw_text = None
        if file_extension in ['.csv']:
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_extension in ['.json']:
            df = pd.read_json(io.BytesIO(file_content))
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(io.BytesIO(file_content))
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff']:
            if OCR_AVAILABLE:
                image = Image.open(io.BytesIO(file_content))
                raw_text = pytesseract.image_to_string(image)
            else:
                raise ValueError("OCR not installed. Install pytesseract and PIL.")
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        dataset_type = self.detect_file_type(file_content, filename)
        if dataset_type == 'ilsi' and df is not None:
            return self._process_ilsi_df(df)
        elif dataset_type == 'ncrb' and df is not None:
            return self._process_ncrb_df(df)
        elif dataset_type in ['scam_hinglish', 'multi_scam'] and df is not None:
            return self._process_scam_df(df, dataset_type)
        elif dataset_type in ['cdr', 'transaction'] and df is not None:
            return self._process_cdr_transaction_df(df, dataset_type)
        elif raw_text:
            return self._process_text(raw_text, filename)
        else:
            return self._process_generic_df(df) if df is not None else ([], [])

    def _process_ilsi_df(self, df):
        entities, relationships = [], []
        for _, row in df.iterrows():
            case_id = row.get('case_id', row.get('id', f"CASE_{len(entities)}"))
            facts = row.get('fact', row.get('text', ''))
            ipc = row.get('ipc_sections', row.get('labels', ''))
            entities.append({'id': case_id, 'type': 'CASE', 'name': case_id, 'facts': str(facts)[:200], 'source': 'upload'})
            if isinstance(ipc, str):
                ipc_list = re.findall(r'\d+', ipc)
            else:
                ipc_list = str(ipc).split(',')
            for sec in ipc_list[:5]:
                if sec:
                    ipc_id = f"IPC-{sec}"
                    entities.append({'id': ipc_id, 'type': 'IPC_SECTION', 'name': f"Section {sec}", 'source': 'upload'})
                    relationships.append({'source': case_id, 'target': ipc_id, 'type': 'CITES', 'source_type': 'upload'})
            extracted = self.extract_entities_from_text(str(facts))
            for ent in extracted:
                entity_id = f"{ent['type']}_{ent['value'].replace(' ', '_')}"
                entities.append({'id': entity_id, 'type': ent['type'], 'name': ent['value'], 'source': 'upload'})
                relationships.append({'source': case_id, 'target': entity_id, 'type': 'MENTIONS', 'source_type': 'upload'})
        return entities, relationships

    def _process_ncrb_df(self, df):
        entities, relationships = [], []
        for _, row in df.head(1000).iterrows():
            state = str(row.get('State', row.get('state', 'Unknown')))
            if state not in ['Unknown', 'nan']:
                state_id = f"LOC_{state.replace(' ', '_')}"
                entities.append({'id': state_id, 'type': 'LOCATION', 'name': state, 'source': 'upload'})
                crime = str(row.get('Crime_Type', row.get('crime_type', 'Unknown')))
                if crime not in ['Unknown', 'nan']:
                    crime_id = f"CRIME_{crime.replace(' ', '_')}"
                    entities.append({'id': crime_id, 'type': 'CRIME_TYPE', 'name': crime, 'source': 'upload'})
                    relationships.append({'source': state_id, 'target': crime_id, 'type': 'HAS_CRIME', 'source_type': 'upload'})
        return entities, relationships

    def _process_scam_df(self, df, dataset_type):
        entities, relationships = [], []
        col = 'scam_type' if dataset_type == 'scam_hinglish' else 'category'
        for _, row in df.head(500).iterrows():
            scam = str(row.get(col, row.get('type', 'Unknown')))
            if scam not in ['Unknown', 'nan']:
                scam_id = f"SCAM_{scam.replace(' ', '_')}"
                entities.append({'id': scam_id, 'type': 'SCAM_TYPE', 'name': scam, 'source': 'upload'})
        return entities, relationships

    def _process_cdr_transaction_df(self, df, dataset_type):
        entities, relationships = [], []
        if dataset_type == 'cdr':
            for _, row in df.head(1000).iterrows():
                caller = str(row.get('caller', row.get('from', '')))
                receiver = str(row.get('receiver', row.get('to', '')))
                if caller and receiver:
                    cid = f"PHONE_{caller.replace(' ', '_')}"
                    rid = f"PHONE_{receiver.replace(' ', '_')}"
                    entities.append({'id': cid, 'type': 'PHONE', 'name': caller, 'source': 'upload'})
                    entities.append({'id': rid, 'type': 'PHONE', 'name': receiver, 'source': 'upload'})
                    relationships.append({'source': cid, 'target': rid, 'type': 'CALLED',
                                          'duration': row.get('duration', 0), 'source_type': 'upload'})
        elif dataset_type == 'transaction':
            for _, row in df.head(1000).iterrows():
                from_acc = str(row.get('from', row.get('source', '')))
                to_acc = str(row.get('to', row.get('target', '')))
                if from_acc and to_acc:
                    fid = f"ACC_{from_acc.replace(' ', '_')}"
                    tid = f"ACC_{to_acc.replace(' ', '_')}"
                    entities.append({'id': fid, 'type': 'ACCOUNT', 'name': from_acc, 'source': 'upload'})
                    entities.append({'id': tid, 'type': 'ACCOUNT', 'name': to_acc, 'source': 'upload'})
                    relationships.append({'source': fid, 'target': tid, 'type': 'TRANSACTION',
                                          'amount': row.get('amount', 0), 'source_type': 'upload'})
        return entities, relationships

    def _process_text(self, text, filename):
        entities = self.extract_entities_from_text(text)
        doc_id = f"DOC_{filename.replace(' ', '_')}"
        entities.append({'id': doc_id, 'type': 'DOCUMENT', 'name': filename, 'content': text[:200], 'source': 'upload'})
        relationships = []
        for ent in entities:
            if ent['type'] != 'DOCUMENT':
                relationships.append({'source': doc_id, 'target': ent['id'], 'type': 'MENTIONS', 'source_type': 'upload'})
        return entities, relationships

    def _process_generic_df(self, df):
        entities, relationships = [], []
        for idx, row in df.head(500).iterrows():
            row_dict = row.to_dict()
            entity_id = f"ROW_{idx+1}"
            entities.append({'id': entity_id, 'type': 'GENERIC', 'name': f"Row {idx+1}", 'properties': row_dict, 'source': 'upload'})
        return entities, relationships

    def extract_entities_from_text(self, text):
        entities = []
        if not text or not isinstance(text, str):
            return entities
        # IPC sections
        ipc_patterns = [r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})', r'(\d{1,3})\s*(?:IPC|of IPC)']
        for pattern in ipc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({'type': 'IPC_SECTION', 'value': f"IPC-{match}", 'source': 'extracted'})
        # Names
        name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        matches = re.findall(name_pattern, text)
        for first, last in matches[:10]:
            if len(first)>1 and len(last)>1 and first not in ['The','And','For','With','From']:
                entities.append({'type': 'PERSON', 'value': f"{first} {last}", 'source': 'extracted'})
        # Cities
        cities = ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
        for city in cities:
            if city in text:
                entities.append({'type': 'LOCATION', 'value': city, 'source': 'extracted'})
        return entities

    def get_summary(self):
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
            else:
                summary[name] = "Loaded"
        return summary
