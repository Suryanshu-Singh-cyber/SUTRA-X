"""
SUTRA-X Data Loader – Enhanced for dynamic file uploads
"""
import pandas as pd
import json
import re
import io
from pathlib import Path
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except:
    OCR_AVAILABLE = False

class RealDataLoader:
    def __init__(self):
        self.datasets = {}
        self.entities = []
        self.relationships = []
        self.project_root = Path(__file__).parent.parent.parent.parent

    def detect_file_type(self, file_content, filename):
        name = filename.lower()
        if 'ilsi' in name or 'case' in name:
            return 'ilsi'
        if 'ncrb' in name or 'cyber' in name:
            return 'ncrb'
        if 'scam' in name:
            return 'multi_scam' if 'multi' in name else 'scam_hinglish'
        if 'cdr' in name or 'call' in name:
            return 'cdr'
        if 'transaction' in name or 'bank' in name:
            return 'transaction'
        return 'generic'

    def read_csv(self, data): return pd.read_csv(io.BytesIO(data))
    def read_json(self, data): return pd.read_json(io.BytesIO(data))
    def read_excel(self, data): return pd.read_excel(io.BytesIO(data))
    def read_image(self, data):
        if not OCR_AVAILABLE: return None
        try:
            img = Image.open(io.BytesIO(data))
            return pytesseract.image_to_string(img)
        except: return None

    def process_uploaded_file(self, file_content, filename, ext):
        df = None; raw = None
        if ext in ['.csv']: df = self.read_csv(file_content)
        elif ext in ['.json']: df = self.read_json(file_content)
        elif ext in ['.xlsx','.xls']: df = self.read_excel(file_content)
        elif ext in ['.png','.jpg','.jpeg','.tiff']: raw = self.read_image(file_content)
        else: raise ValueError(f"Unsupported: {ext}")

        dtype = self.detect_file_type(file_content, filename)
        if dtype == 'ilsi' and df is not None:
            return self._process_ilsi(df)
        elif dtype == 'ncrb' and df is not None:
            return self._process_ncrb(df)
        elif dtype in ['scam_hinglish','multi_scam'] and df is not None:
            return self._process_scam(df, dtype)
        elif dtype in ['cdr','transaction'] and df is not None:
            return self._process_cdr_txn(df, dtype)
        elif raw:
            return self._process_text(raw, filename)
        elif df is not None:
            return self._process_generic(df)
        return [], []

    def _process_ilsi(self, df):
        entities, rels = [], []
        for _, r in df.iterrows():
            cid = r.get('case_id', r.get('id', f"CASE_{len(entities)}"))
            facts = str(r.get('fact', r.get('text', '')))
            ipc = str(r.get('ipc_sections', r.get('labels', '')))
            entities.append({'id': cid, 'type':'CASE','name':cid,'facts':facts[:200],'source':'upload'})
            ipc_list = re.findall(r'\d+', ipc)
            for sec in ipc_list[:5]:
                ipc_id = f"IPC-{sec}"
                entities.append({'id':ipc_id,'type':'IPC_SECTION','name':f"Section {sec}",'source':'upload'})
                rels.append({'source':cid,'target':ipc_id,'type':'CITES','source_type':'upload'})
            for ent in self.extract_entities_from_text(facts):
                eid = f"{ent['type']}_{ent['value'].replace(' ', '_')}"
                entities.append({'id':eid,'type':ent['type'],'name':ent['value'],'source':'upload'})
                rels.append({'source':cid,'target':eid,'type':'MENTIONS','source_type':'upload'})
        return entities, rels

    def _process_ncrb(self, df):
        entities, rels = [], []
        for _, r in df.head(1000).iterrows():
            state = str(r.get('State', r.get('state', 'Unknown')))
            crime = str(r.get('Crime_Type', r.get('crime_type', 'Unknown')))
            if state not in ['Unknown','nan']:
                sid = f"LOC_{state.replace(' ', '_')}"
                entities.append({'id':sid,'type':'LOCATION','name':state,'source':'upload'})
                if crime not in ['Unknown','nan']:
                    cid = f"CRIME_{crime.replace(' ', '_')}"
                    entities.append({'id':cid,'type':'CRIME_TYPE','name':crime,'source':'upload'})
                    rels.append({'source':sid,'target':cid,'type':'HAS_CRIME','source_type':'upload'})
        return entities, rels

    def _process_scam(self, df, dtype):
        entities = []
        col = 'scam_type' if dtype=='scam_hinglish' else 'category'
        for _, r in df.head(500).iterrows():
            scam = str(r.get(col, r.get('type', 'Unknown')))
            if scam not in ['Unknown','nan']:
                sid = f"SCAM_{scam.replace(' ', '_')}"
                entities.append({'id':sid,'type':'SCAM_TYPE','name':scam,'source':'upload'})
        return entities, []

    def _process_cdr_txn(self, df, dtype):
        entities, rels = [], []
        if dtype == 'cdr':
            for _, r in df.head(1000).iterrows():
                frm = str(r.get('caller', r.get('from', '')))
                to = str(r.get('receiver', r.get('to', '')))
                if frm and to:
                    fid = f"PHONE_{frm.replace(' ', '_')}"
                    tid = f"PHONE_{to.replace(' ', '_')}"
                    entities.extend([{'id':fid,'type':'PHONE','name':frm,'source':'upload'},
                                     {'id':tid,'type':'PHONE','name':to,'source':'upload'}])
                    rels.append({'source':fid,'target':tid,'type':'CALLED','duration':r.get('duration',0),'source_type':'upload'})
        else: # transaction
            for _, r in df.head(1000).iterrows():
                frm = str(r.get('from', r.get('source', '')))
                to = str(r.get('to', r.get('target', '')))
                if frm and to:
                    fid = f"ACC_{frm.replace(' ', '_')}"
                    tid = f"ACC_{to.replace(' ', '_')}"
                    entities.extend([{'id':fid,'type':'ACCOUNT','name':frm,'source':'upload'},
                                     {'id':tid,'type':'ACCOUNT','name':to,'source':'upload'}])
                    rels.append({'source':fid,'target':tid,'type':'TRANSACTION','amount':r.get('amount',0),'source_type':'upload'})
        return entities, rels

    def _process_text(self, text, filename):
        entities = self.extract_entities_from_text(text)
        doc_id = f"DOC_{filename.replace(' ', '_')}"
        entities.append({'id':doc_id,'type':'DOCUMENT','name':filename,'content':text[:200],'source':'upload'})
        rels = [{'source':doc_id,'target':e['id'],'type':'MENTIONS','source_type':'upload'} for e in entities if e['type']!='DOCUMENT']
        return entities, rels

    def _process_generic(self, df):
        entities = []
        for idx, r in df.head(500).iterrows():
            entities.append({'id':f"ROW_{idx+1}",'type':'GENERIC','name':f"Row {idx+1}",'properties':r.to_dict(),'source':'upload'})
        return entities, []

    def extract_entities_from_text(self, text):
        entities = []
        if not text or not isinstance(text, str): return entities
        # IPC
        for pat in [r'(?:IPC|Section|Sec\.?)\s*(\d{1,3})', r'(\d{1,3})\s*(?:IPC|of IPC)']:
            for m in re.findall(pat, text, re.I):
                entities.append({'type':'IPC_SECTION','value':f"IPC-{m}",'source':'extracted'})
        # Names
        for first, last in re.findall(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b', text)[:10]:
            if len(first)>1 and len(last)>1 and first not in ['The','And','For','With','From']:
                entities.append({'type':'PERSON','value':f"{first} {last}",'source':'extracted'})
        # Cities
        cities = ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Kolkata','Pune','Ahmedabad','Jaipur','Lucknow']
        for city in cities:
            if city in text:
                entities.append({'type':'LOCATION','value':city,'source':'extracted'})
        return entities
