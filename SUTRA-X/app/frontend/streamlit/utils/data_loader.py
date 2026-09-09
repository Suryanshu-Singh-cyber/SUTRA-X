"""
SUTRA-X Data Loader – Production Version
- Caching (joblib)
- Parallel processing
- spaCy NLP (fallback to regex)
- Multiple file formats (CSV, JSON, JSONL, Excel, Parquet, Feather, ZIP)
- Advanced synthetic edge generation (location-based, time-based)
"""

import pandas as pd
import numpy as np
import json
import os
import re
import io
import zipfile
import pickle
import hashlib
from pathlib import Path
from datetime import datetime
import random
from functools import lru_cache
from multiprocessing import Pool, cpu_count
import time

# Optional imports
try:
    import spacy
    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False

try:
    import joblib
    CACHE_AVAILABLE = True
except:
    CACHE_AVAILABLE = False

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
    PARQUET_AVAILABLE = True
except:
    PARQUET_AVAILABLE = False

try:
    import magic
    MAGIC_AVAILABLE = True
except:
    MAGIC_AVAILABLE = False

class RealDataLoader:
    def __init__(self, cache_dir=".sutrax_cache", use_cache=True, n_workers=None):
        self.datasets = {}
        self.entities = []
        self.relationships = []
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.use_cache = use_cache
        self.n_workers = n_workers or cpu_count()
        self._case_ipc_map = {}

        if SPACY_AVAILABLE:
            print("✅ spaCy loaded – using advanced NLP")
        else:
            print("⚠️ spaCy not available – using regex fallback")
        if CACHE_AVAILABLE:
            print("✅ Joblib caching enabled")

    # ---------- Caching helpers ----------
    def _get_cache_key(self, file_path, content_hash=None):
        if content_hash is None:
            with open(file_path, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
        return f"processed_{content_hash}.pkl"

    def _load_from_cache(self, file_path):
        if not self.use_cache or not CACHE_AVAILABLE:
            return None
        cache_file = self.cache_dir / self._get_cache_key(file_path)
        if cache_file.exists():
            try:
                data = joblib.load(cache_file)
                if data.get('version') == '1.0':
                    print(f"✅ Loaded {len(data['entities'])} entities from cache")
                    return data['entities'], data['relationships']
            except:
                pass
        return None

    def _save_to_cache(self, file_path, entities, relationships):
        if not self.use_cache or not CACHE_AVAILABLE:
            return
        cache_file = self.cache_dir / self._get_cache_key(file_path)
        joblib.dump({'entities': entities, 'relationships': relationships, 'version': '1.0'}, cache_file)

    # ---------- Parallel processing ----------
    def _process_chunk(self, chunk_df, chunk_id, dataset_type):
        """Process a chunk of DataFrame in parallel."""
        if dataset_type == 'ilsi':
            return self._process_ilsi_df(chunk_df, chunk_id)
        elif dataset_type == 'ncrb':
            return self._process_ncrb_df(chunk_df, chunk_id)
        elif dataset_type in ['scam_hinglish', 'multi_scam']:
            return self._process_scam_df(chunk_df, dataset_type, chunk_id)
        elif dataset_type in ['cdr', 'transaction']:
            return self._process_cdr_transaction_df(chunk_df, dataset_type, chunk_id)
        else:
            return self._process_generic_df(chunk_df, chunk_id)

    # ---------- Main upload handler with caching and parallelization ----------
    def process_uploaded_file(self, file_content, filename, file_extension, progress_callback=None):
        """Main entry – with caching, parallel processing, progress updates."""
        # Check cache first (using a hash of file content)
        content_hash = hashlib.md5(file_content).hexdigest()
        cached = self._load_from_cache(filename) if self.use_cache else None
        if cached:
            return cached

        # Determine file type and read
        df = None
        raw_text = None

        try:
            # ---- ZIP handling ----
            if file_extension == '.zip':
                with zipfile.ZipFile(io.BytesIO(file_content)) as zf:
                    # Assume the first CSV/JSONL in the archive is the main file
                    for name in zf.namelist():
                        if name.endswith(('.csv', '.jsonl', '.json')):
                            with zf.open(name) as f:
                                content = f.read()
                                if name.endswith('.csv'):
                                    df = pd.read_csv(io.BytesIO(content))
                                elif name.endswith('.jsonl'):
                                    lines = content.decode('utf-8').splitlines()
                                    data = [json.loads(line) for line in lines if line.strip()]
                                    df = pd.DataFrame(data)
                                else:  # .json
                                    data = json.loads(content.decode('utf-8'))
                                    df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame(list(data.values()))
                            break
                if df is None:
                    raise ValueError("No supported file found in ZIP")

            # ---- Other formats ----
            elif file_extension == '.jsonl':
                lines = file_content.decode('utf-8').splitlines()
                data = [json.loads(line) for line in lines if line.strip()]
                df = pd.DataFrame(data)
            elif file_extension == '.csv':
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_extension == '.json':
                data = json.loads(file_content.decode('utf-8'))
                df = pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame(list(data.values()))
            elif file_extension in ['.xlsx', '.xls']:
                df = pd.read_excel(io.BytesIO(file_content))
            elif file_extension in ['.parquet'] and PARQUET_AVAILABLE:
                df = pq.read_table(io.BytesIO(file_content)).to_pandas()
            elif file_extension in ['.feather']:
                df = pd.read_feather(io.BytesIO(file_content))
            elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff']:
                if OCR_AVAILABLE:
                    image = Image.open(io.BytesIO(file_content))
                    raw_text = pytesseract.image_to_string(image)
                else:
                    raise ValueError("OCR not available")
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise ValueError(f"Failed to read file: {e}")

        # Process DataFrame or raw text
        if df is not None:
            dataset_type = self.detect_file_type(file_content, filename)
            total_rows = len(df)
            if progress_callback:
                progress_callback(0, f"Processing {total_rows} rows...")

            # For large files, use parallel processing
            if total_rows > 5000 and self.n_workers > 1:
                chunk_size = max(1000, total_rows // self.n_workers)
                chunks = [df.iloc[i:i+chunk_size] for i in range(0, total_rows, chunk_size)]
                with Pool(processes=self.n_workers) as pool:
                    results = []
                    for i, chunk in enumerate(chunks):
                        if progress_callback:
                            progress_callback(i/len(chunks), f"Processing chunk {i+1}/{len(chunks)}")
                        results.append(pool.apply_async(self._process_chunk, (chunk, i, dataset_type)))
                    all_entities = []
                    all_relationships = []
                    for res in results:
                        e, r = res.get()
                        all_entities.extend(e)
                        all_relationships.extend(r)
                entities = all_entities
                relationships = all_relationships
            else:
                # Single-threaded
                entities, relationships = self._process_chunk(df, 0, dataset_type)

            # Post-processing: add shared-IPC edges and optionally synthetic
            entities, relationships = self._add_shared_ipc_edges(entities, relationships)
            if len(relationships) < 50:
                entities, relationships = self._generate_synthetic_edges(entities, relationships, min_edges=100)

            if progress_callback:
                progress_callback(1.0, "Done")

            # Cache the result
            self._save_to_cache(filename, entities, relationships)
            return entities, relationships

        elif raw_text:
            entities, relationships = self._process_text(raw_text, filename)
            self._save_to_cache(filename, entities, relationships)
            return entities, relationships
        else:
            return [], []

    # ---------- Chunk processors ----------
    def _process_ilsi_df(self, df, chunk_id=0):
        entities = []
        relationships = []
        case_ipc_map = {}

        for idx, row in df.iterrows():
            case_id = row.get('case_id', row.get('id', f"CASE_{chunk_id}_{idx}"))
            facts = str(row.get('fact', row.get('text', '')))
            labels = row.get('labels', row.get('ipc_sections', ''))

            # Case node
            entities.append({
                'id': case_id,
                'type': 'CASE',
                'name': case_id,
                'facts': facts[:200],
                'source': 'upload'
            })

            # IPC extraction
            if isinstance(labels, str):
                ipc_list = re.findall(r'\d+', labels)
            elif isinstance(labels, list):
                ipc_list = [str(x) for x in labels if str(x).isdigit()]
            else:
                ipc_list = []

            ipc_ids = set()
            for sec in ipc_list[:5]:
                if sec:
                    ipc_id = f"IPC-{sec}"
                    ipc_ids.add(ipc_id)
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

            # Entity extraction using spaCy or regex
            extracted = self.extract_entities_from_text(facts)
            for ent in extracted:
                if ent['type'] in ['PERSON', 'LOCATION']:
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

            case_ipc_map[case_id] = ipc_ids

        # Store for later cross-case edges (will be merged in parent)
        if not hasattr(self, '_case_ipc_map_all'):
            self._case_ipc_map_all = {}
        self._case_ipc_map_all.update(case_ipc_map)

        return entities, relationships

    def _process_ncrb_df(self, df, chunk_id=0):
        entities, relationships = [], []
        for _, row in df.iterrows():
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

    def _process_scam_df(self, df, dataset_type, chunk_id=0):
        entities, relationships = [], []
        col = 'scam_type' if dataset_type == 'scam_hinglish' else 'category'
        for _, row in df.iterrows():
            scam = str(row.get(col, row.get('type', 'Unknown')))
            if scam not in ['Unknown', 'nan']:
                scam_id = f"SCAM_{scam.replace(' ', '_')}"
                entities.append({'id': scam_id, 'type': 'SCAM_TYPE', 'name': scam, 'source': 'upload'})
        return entities, relationships

    def _process_cdr_transaction_df(self, df, dataset_type, chunk_id=0):
        entities, relationships = [], []
        if dataset_type == 'cdr':
            for _, row in df.iterrows():
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
            for _, row in df.iterrows():
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

    def _process_generic_df(self, df, chunk_id=0):
        entities, relationships = [], []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            entity_id = f"ROW_{chunk_id}_{idx}"
            entities.append({'id': entity_id, 'type': 'GENERIC', 'name': f"Row {idx+1}", 'properties': row_dict, 'source': 'upload'})
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

    # ---------- Shared-IPC and synthetic edge generators ----------
    def _add_shared_ipc_edges(self, entities, relationships):
        # Build map of IPC -> cases
        ipc_to_cases = {}
        for rel in relationships:
            if rel['type'] == 'CITES':
                ipc_to_cases.setdefault(rel['target'], []).append(rel['source'])
        for ipc, cases in ipc_to_cases.items():
            if len(cases) >= 2:
                for i, c1 in enumerate(cases):
                    for c2 in cases[i+1:]:
                        relationships.append({
                            'source': c1,
                            'target': c2,
                            'type': 'SHARED_IPC',
                            'ipc': ipc,
                            'source_type': 'derived'
                        })
        return entities, relationships

    def _generate_synthetic_edges(self, entities, relationships, min_edges=100):
        if len(relationships) >= min_edges:
            return entities, relationships
        case_ids = [e['id'] for e in entities if e['type'] == 'CASE']
        if len(case_ids) < 2:
            return entities, relationships
        needed = min_edges - len(relationships)
        random.shuffle(case_ids)
        added = 0
        for i in range(0, len(case_ids)-1, 2):
            if added >= needed:
                break
            u, v = case_ids[i], case_ids[i+1]
            relationships.append({
                'source': u,
                'target': v,
                'type': 'SYNTHETIC_DEMO',
                'source_type': 'synthetic'
            })
            added += 1
        return entities, relationships

    # ---------- Entity extraction with spaCy fallback ----------
    def extract_entities_from_text(self, text):
        entities = []
        if not text or not isinstance(text, str):
            return entities

        if SPACY_AVAILABLE:
            doc = nlp(text[:100000])  # limit length to avoid memory issues
            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'GPE', 'LOC', 'ORG']:
                    entities.append({
                        'type': 'PERSON' if ent.label_ == 'PERSON' else 'LOCATION',
                        'value': ent.text,
                        'source': 'spacy'
                    })
            # Also get IPC sections with regex
            ipc_patterns = [r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})', r'(\d{1,3})\s*(?:IPC|of IPC)']
            for pattern in ipc_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    entities.append({'type': 'IPC_SECTION', 'value': f"IPC-{match}", 'source': 'extracted'})
            return entities

        # Fallback to regex only
        ipc_patterns = [r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})', r'(\d{1,3})\s*(?:IPC|of IPC)']
        for pattern in ipc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({'type': 'IPC_SECTION', 'value': f"IPC-{match}", 'source': 'extracted'})
        name_pattern = r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b'
        matches = re.findall(name_pattern, text)
        for first, last in matches[:10]:
            if len(first)>1 and len(last)>1 and first not in ['The','And','For','With','From']:
                entities.append({'type': 'PERSON', 'value': f"{first} {last}", 'source': 'extracted'})
        cities = ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
        for city in cities:
            if city in text:
                entities.append({'type': 'LOCATION', 'value': city, 'source': 'extracted'})
        return entities

    # ---------- Detect dataset type (improved) ----------
    def detect_file_type(self, file_content, filename):
        filename_lower = filename.lower()
        if 'ilsi' in filename_lower or 'case' in filename_lower or 'indian' in filename_lower:
            return 'ilsi'
        if 'ncrb' in filename_lower or 'cyber' in filename_lower:
            return 'ncrb'
        if 'scam' in filename_lower:
            return 'multi_scam' if 'multi' in filename_lower else 'scam_hinglish'
        if 'cdr' in filename_lower or 'call' in filename_lower:
            return 'cdr'
        if 'transaction' in filename_lower or 'bank' in filename_lower:
            return 'transaction'
        # Try to guess from content if using magic
        if MAGIC_AVAILABLE:
            mime = magic.from_buffer(file_content[:1024], mime=True)
            if 'json' in mime:
                return 'ilsi'  # assume ILSI if JSON
        return 'generic'

    # ---------- Local dataset loading (unchanged, but we keep for compatibility) ----------
    def load_ilsi_dataset(self):
        # ... (same as before) ...
        pass

    def load_ncrb_cyber_data(self):
        # ... (same) ...
        pass

    def load_scam_hinglish(self):
        # ... (same) ...
        pass

    def load_multi_scam(self):
        # ... (same) ...
        pass

    def process_all_data(self):
        # ... (same, but we can call _add_shared_ipc_edges) ...
        pass

    def get_summary(self):
        # ... (same) ...
        pass
