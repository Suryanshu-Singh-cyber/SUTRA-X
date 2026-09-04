import spacy
import re
from typing import List, Dict, Tuple, Optional
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from indicnlp.tokenize import indic_tokenize
from indicnlp.normalize.indic_normalize import IndicNormalizer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EntityExtractor:
    """Multi-lingual entity extraction for Indian languages"""
    
    def __init__(self, language: str = 'en'):
        self.language = language
        self.normalizer = IndicNormalizer()
        
        # Load appropriate model
        if language == 'en':
            self.nlp = spacy.load('en_core_web_sm')
        elif language == 'hi':
            try:
                self.nlp = spacy.load('hi_core_news_sm')
            except:
                # Fallback to English with transliteration
                self.nlp = spacy.load('en_core_web_sm')
                logger.warning("Hindi model not found, using English with transliteration")
        else:
            self.nlp = spacy.load('en_core_web_sm')
        
        # Custom entity patterns
        self.custom_patterns = {
            'AADHAAR': r'\b[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\b',
            'PAN': r'\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b',
            'VEHICLE': r'\b[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}\b',
            'PHONE': r'\b[6-9][0-9]{9}\b',
            'IFSC': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
            'ACCOUNT': r'\b[0-9]{9,18}\b',
            'PINCODE': r'\b[0-9]{6}\b',
            'CASE_NUMBER': r'\b[0-9]{3,4}\/[0-9]{2,4}\b',
            'DATE': r'\b([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})\b',
            'TIME': r'\b[0-9]{1,2}[:][0-9]{2}\b',
            'AMOUNT': r'[₹Rs. ]?[0-9,]+\.?[0-9]+\b',
            'LOCATION': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b'
        }
        
        # Person name patterns for Indian names
        self.name_patterns = [
            r'\b(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?|Prof\.?|Shri|Smt\.?|Kumari)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:Kumar|Singh|Sharma|Verma|Patel|Reddy|Rao|Joshi|Gupta)',
        ]
    
    def transliterate_to_english(self, text: str) -> str:
        """Transliterate Hindi/Indian text to English"""
        try:
            # Detect if text is in Devanagari
            if any('\u0900' <= c <= '\u097F' for c in text):
                return transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)
            return text
        except:
            return text
    
    def normalize_text(self, text: str) -> str:
        """Normalize Indian language text"""
        if self.language == 'hi':
            return self.normalizer.normalize(text)
        return text
    
    def extract_entities_spacy(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities using spaCy"""
        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [],
            'LOC': [],
            'GPE': [],
            'DATE': [],
            'MONEY': [],
            'PERCENT': [],
            'TIME': [],
            'CARDINAL': []
        }
        
        for ent in doc.ents:
            entities[ent.label_].append({
                'text': ent.text,
                'start': ent.start_char,
                'end': ent.end_char,
                'label': ent.label_,
                'confidence': ent._.get('confidence', 0.8) if hasattr(ent._, 'confidence') else 0.8
            })
        
        return entities
    
    def extract_custom_patterns(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities using custom regex patterns"""
        entities = {}
        
        for entity_type, pattern in self.custom_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            entities[entity_type] = []
            
            for match in matches:
                entities[entity_type].append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'type': entity_type
                })
        
        return entities
    
    def extract_names(self, text: str) -> List[Dict]:
        """Extract Indian names using patterns"""
        names = []
        
        for pattern in self.name_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                names.append({
                    'name': match.group(1),
                    'full_match': match.group(),
                    'confidence': 0.7
                })
        
        return names
    
    def extract_entities(self, text: str, include_transliteration: bool = True) -> Dict:
        """Complete entity extraction pipeline"""
        # Normalize text
        normalized_text = self.normalize_text(text)
        
        # For non-English, transliterate to English
        english_text = self.transliterate_to_english(normalized_text) if include_transliteration else normalized_text
        
        # Extract entities from both original and transliterated
        entities = {
            'original_text': text,
            'normalized_text': normalized_text,
            'transliterated': english_text if include_transliteration else None,
            'entities': {}
        }
        
        # Get spaCy entities
        spacy_entities = self.extract_entities_spacy(english_text)
        
        # Get custom pattern matches
        custom_entities = self.extract_custom_patterns(english_text)
        
        # Get names
        names = self.extract_names(english_text)
        
        # Merge all entities
        all_entities = {}
        
        # Add spaCy entities
        for entity_type, ents in spacy_entities.items():
            if ents:
                all_entities[entity_type] = ents
        
        # Add custom entities
        for entity_type, ents in custom_entities.items():
            if ents:
                all_entities[entity_type] = ents
        
        # Add names
        if names:
            all_entities['INDIAN_NAME'] = names
        
        entities['entities'] = all_entities
        
        return entities
    
    def extract_entities_from_batch(self, texts: List[str]) -> List[Dict]:
        """Extract entities from multiple texts"""
        results = []
        for text in texts:
            results.append(self.extract_entities(text))
        return results

class RelationExtractor:
    """Extract relationships between entities"""
    
    def __init__(self):
        # Relationship patterns
        self.relationship_patterns = [
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:met|called|contacted|spoke to|talked to)\s+(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'MET'),
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:paid|sent|transferred|gave)\s+[₹Rs. ]?[0-9,]+\s+(?:to|for)\s+(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'PAID'),
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:called|phoned|contacted)\s+(\d{10})', 'CALLED'),
            (r'(\d{10})\s+(?:called|phoned|contacted)\s+(\d{10})', 'CALLED'),
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:lives at|resides at|stays at)\s+([A-Za-z\s,]+)', 'LIVES_AT'),
            (r'(\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|was)\s+(?:the\s+)?(?:owner|driver)\s+(?:of\s+)?(\b[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}\b)', 'OWNS'),
        ]
    
    def extract_relations(self, text: str) -> List[Dict]:
        """Extract relationships from text"""
        relations = []
        
        for pattern, rel_type in self.relationship_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                relation = {
                    'type': rel_type,
                    'source': match.group(1) if match.lastindex >= 1 else None,
                    'target': match.group(2) if match.lastindex >= 2 else None,
                    'text': match.group(),
                    'confidence': 0.7
                }
                
                # Clean the entities
                if relation['source']:
                    relation['source'] = relation['source'].strip()
                if relation['target']:
                    relation['target'] = relation['target'].strip()
                
                relations.append(relation)
        
        return relations