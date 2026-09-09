"""
SUTRA-X Data Loader – Enhanced for dynamic file uploads
Supports CSV, JSON, Excel, and images (OCR)
"""

import pandas as pd
import json
import os
import re
from pathlib import Path
import io
from datetime import datetime

# Try to import optional OCR library (Tesseract)
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCR not available – install pytesseract & PIL for image support")

class RealDataLoader:
    """Loads and processes all types of uploaded files for criminal network analysis"""

    def __init__(self):
        self.datasets = {}
        self.entities = []
        self.relationships = []
        self.project_root = Path(__file__).parent.parent.parent.parent  # up to Nexus_intel

    # ---------- File detection ----------
    def detect_file_type(self, file_content, filename):
        """Detect dataset type based on filename or content"""
        filename_lower = filename.lower()
        if 'ilsi' in filename_lower or 'case' in filename_lower:
            return 'ilsi'
        if 'ncrb' in filename_lower or 'cyber' in filename_lower:
            return 'ncrb'
        if 'scam' in filename_lower:
            if 'multi' in filename_lower or 'multiclass' in filename_lower:
                return 'multi_scam'
            return 'scam_hinglish'
        if 'cdr' in filename_lower or 'call' in filename_lower:
            return 'cdr'
        if 'transaction' in filename_lower or 'bank' in filename_lower:
            return 'transaction'
        return 'generic'

    # ---------- Generic file readers ----------
    def read_csv(self, file_content):
        return pd.read_csv(io.BytesIO(file_content))

    def read_json(self, file_content):
        return pd.read_json(io.BytesIO(file_content))

    def read_excel(self, file_content):
        return pd.read_excel(io.BytesIO(file_content))

    def read_image(self, file_content):
        """Extract text from image using OCR (if available)"""
        if not OCR_AVAILABLE:
            return None
        try:
            image = Image.open(io.BytesIO(file_content))
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"❌ OCR failed: {e}")
            return None

    # ---------- Process uploaded file ----------
    def process_uploaded_file(self, file_content, filename, file_extension):
        """Main entry point – reads file, detects type, extracts entities"""
        df = None
        raw_text = None

        # 1. Read based on extension
        if file_extension in ['.csv']:
            df = self.read_csv(file_content)
        elif file_extension in ['.json']:
            df = self.read_json(file_content)
        elif file_extension in ['.xlsx', '.xls']:
            df = self.read_excel(file_content)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff']:
            raw_text = self.read_image(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        # 2. Detect dataset type
        dataset_type = self.detect_file_type(file_content, filename)

        # 3. Process accordingly
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
            # Generic: treat as generic tabular data
            if df is not None:
                return self._process_generic_df(df)
            else:
                return [], []

    # ---------- Specific processors ----------
    def _process_ilsi_df(self, df):
        entities, relationships = [], []
        # Expect columns: case_id, fact, ipc_sections (or similar)
        for _, row in df.iterrows():
            case_id = row.get('case_id', row.get('id', f"CASE_{len(entities)}"))
            facts = row.get('fact', row.get('text', ''))
            ipc = row.get('ipc_sections', row.get('labels', ''))

            # Entity: case
            entities.append({
                'id': case_id,
                'type': 'CASE',
                'name': case_id,
                'facts': str(facts)[:200],
                'source': 'upload'
            })
            # Extract IPC sections
            if isinstance(ipc, str):
                ipc_list = re.findall(r'\d+', ipc)
            else:
                ipc_list = str(ipc).split(',')
            for sec in ipc_list[:5]:
                if sec:
                    ipc_id = f"IPC-{sec}"
                    entities.append({
                        'id': ipc_id,
                        'type': 'IPC_SECTION',
                        'name': f"Section {sec}",
                        'source': 'upload'
                    })
                    relationships.append({
                        'source': case_id,
                        'target': ipc_id,
                        'type': 'CITES',
                        'source_type': 'upload'
                    })
            # Extract other entities from facts
            extracted = self.extract_entities_from_text(str(facts))
            for ent in extracted:
                entity_id = f"{ent['type']}_{ent['value'].replace(' ', '_')}"
                entities.append({
                    'id': entity_id,
                    'type': ent['type'],
                    'name': ent['value'],
                    'source': 'upload'
                })
                relationships.append({
                    'source': case_id,
                    'target': entity_id,
                    'type': 'MENTIONS',
                    'source_type': 'upload'
                })
        return entities, relationships

    def _process_ncrb_df(self, df):
        entities, relationships = [], []
        for _, row in df.head(1000).iterrows():
            state = str(row.get('State', row.get('state', 'Unknown')))
            crime = str(row.get('Crime_Type', row.get('crime_type', 'Unknown')))
            if state != 'Unknown' and state != 'nan':
                state_id = f"LOC_{state.replace(' ', '_')}"
                entities.append({
                    'id': state_id,
                    'type': 'LOCATION',
                    'name': state,
                    'source': 'upload'
                })
                if crime != 'Unknown' and crime != 'nan':
                    crime_id = f"CRIME_{crime.replace(' ', '_')}"
                    entities.append({
                        'id': crime_id,
                        'type': 'CRIME_TYPE',
                        'name': crime,
                        'source': 'upload'
                    })
                    relationships.append({
                        'source': state_id,
                        'target': crime_id,
                        'type': 'HAS_CRIME',
                        'source_type': 'upload'
                    })
        return entities, relationships

    def _process_scam_df(self, df, dataset_type):
        entities, relationships = [], []
        col = 'scam_type' if dataset_type == 'scam_hinglish' else 'category'
        for _, row in df.head(500).iterrows():
            scam = str(row.get(col, row.get('type', 'Unknown')))
            if scam != 'Unknown' and scam != 'nan':
                scam_id = f"SCAM_{scam.replace(' ', '_')}"
                entities.append({
                    'id': scam_id,
                    'type': 'SCAM_TYPE',
                    'name': scam,
                    'source': 'upload'
                })
        return entities, relationships

    def _process_cdr_transaction_df(self, df, dataset_type):
        entities, relationships = [], []
        # For CDR: caller, receiver, duration, etc.
        if dataset_type == 'cdr':
            for _, row in df.head(1000).iterrows():
                caller = row.get('caller', row.get('from', ''))
                receiver = row.get('receiver', row.get('to', ''))
                if caller and receiver:
                    caller_id = f"PHONE_{caller.replace(' ', '_')}"
                    receiver_id = f"PHONE_{receiver.replace(' ', '_')}"
                    entities.append({'id': caller_id, 'type': 'PHONE', 'name': caller, 'source': 'upload'})
                    entities.append({'id': receiver_id, 'type': 'PHONE', 'name': receiver, 'source': 'upload'})
                    relationships.append({
                        'source': caller_id,
                        'target': receiver_id,
                        'type': 'CALLED',
                        'duration': row.get('duration', 0),
                        'source_type': 'upload'
                    })
        elif dataset_type == 'transaction':
            for _, row in df.head(1000).iterrows():
                from_acc = row.get('from', row.get('source', ''))
                to_acc = row.get('to', row.get('target', ''))
                if from_acc and to_acc:
                    from_id = f"ACC_{from_acc.replace(' ', '_')}"
                    to_id = f"ACC_{to_acc.replace(' ', '_')}"
                    entities.append({'id': from_id, 'type': 'ACCOUNT', 'name': from_acc, 'source': 'upload'})
                    entities.append({'id': to_id, 'type': 'ACCOUNT', 'name': to_acc, 'source': 'upload'})
                    relationships.append({
                        'source': from_id,
                        'target': to_id,
                        'type': 'TRANSACTION',
                        'amount': row.get('amount', 0),
                        'source_type': 'upload'
                    })
        return entities, relationships

    def _process_text(self, text, filename):
        # Use existing extract_entities_from_text
        entities = self.extract_entities_from_text(text)
        # Also create a document node
        doc_id = f"DOC_{filename.replace(' ', '_')}"
        entities.append({
            'id': doc_id,
            'type': 'DOCUMENT',
            'name': filename,
            'content': text[:200],
            'source': 'upload'
        })
        # Relationship: document mentions entities
        relationships = []
        for ent in entities:
            if ent['type'] != 'DOCUMENT':
                relationships.append({
                    'source': doc_id,
                    'target': ent['id'],
                    'type': 'MENTIONS',
                    'source_type': 'upload'
                })
        return entities, relationships

    def _process_generic_df(self, df):
        # Treat each row as an entity with columns as properties
        entities, relationships = [], []
        for idx, row in df.head(500).iterrows():
            row_dict = row.to_dict()
            entity_id = f"ROW_{idx+1}"
            entities.append({
                'id': entity_id,
                'type': 'GENERIC',
                'name': f"Row {idx+1}",
                'properties': row_dict,
                'source': 'upload'
            })
            # Create connections between rows if they share values
            # (Simplified: not implemented for speed)
        return entities, relationships

    # ---------- Entity extraction from free text (reused from original) ----------
    def extract_entities_from_text(self, text):
        """Extract PERSON, LOCATION, IPC sections from text"""
        entities = []
        if not text or not isinstance(text, str):
            return entities

        # IPC sections
        ipc_patterns = [r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})', r'(\d{1,3})\s*(?:IPC|of IPC)']
        for pattern in ipc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'type': 'IPC_SECTION',
                    'value': f"IPC-{match}",
                    'source': 'extracted'
                })

        # Indian names (capitalized words)
        name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        matches = re.findall(name_pattern, text)
        for first, last in matches[:10]:
            if len(first) > 1 and len(last) > 1 and first not in ['The', 'And', 'For', 'With', 'From']:
                entities.append({
                    'type': 'PERSON',
                    'value': f"{first} {last}",
                    'source': 'extracted'
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
                    'source': 'extracted'
                })
        return entities

    # ---------- Existing methods (simplified for upload) ----------
    def load_local_datasets(self):
        """Legacy method to load from local folders – kept for compatibility"""
        # ... (same as before)
        pass
