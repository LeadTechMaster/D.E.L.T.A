"""
Enhanced Location Detection System with Fuzzy Matching
Provides intelligent location detection with typo correction and comprehensive coverage
"""

import re
import logging
from typing import Dict, List, Tuple, Optional
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz, process

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocationDetector:
    """Advanced location detection with fuzzy matching and comprehensive coverage"""
    
    def __init__(self):
        """Initialize the location detector with comprehensive location database"""
        self.locations = self._build_comprehensive_location_database()
        self.state_abbreviations = self._build_state_abbreviations()
        self.common_typos = self._build_common_typos()
        logger.info(f"📍 Location detector initialized with {len(self.locations)} locations")
    
    def _build_comprehensive_location_database(self) -> Dict[str, List[str]]:
        """Build comprehensive location database with variations and aliases"""
        return {
            # Major US Cities
            "miami": ["miami", "miami fl", "miami florida", "miami beach", "south beach"],
            "seattle": ["seattle", "seattle wa", "seattle washington", "seattle metro"],
            "new york": ["new york", "nyc", "manhattan", "brooklyn", "queens", "bronx", "staten island", "new york city"],
            "chicago": ["chicago", "chicago il", "chicago illinois", "chicago metro"],
            "atlanta": ["atlanta", "atlanta ga", "atlanta georgia", "atlanta metro"],
            "dallas": ["dallas", "dallas tx", "dallas texas", "dallas fort worth", "dfw"],
            "houston": ["houston", "houston tx", "houston texas", "houston metro"],
            "austin": ["austin", "austin tx", "austin texas", "austin metro"],
            "denver": ["denver", "denver co", "denver colorado", "denver metro"],
            "las vegas": ["las vegas", "las vegas nv", "las vegas nevada", "vegas", "clark county"],
            "phoenix": ["phoenix", "phoenix az", "phoenix arizona", "phoenix metro"],
            "san antonio": ["san antonio", "san antonio tx", "san antonio texas"],
            "san diego": ["san diego", "san diego ca", "san diego california"],
            "san jose": ["san jose", "san jose ca", "san jose california", "silicon valley"],
            "san francisco": ["san francisco", "san francisco ca", "san francisco california", "sf", "bay area"],
            "los angeles": ["los angeles", "los angeles ca", "los angeles california", "la", "l.a."],
            "boston": ["boston", "boston ma", "boston massachusetts"],
            "philadelphia": ["philadelphia", "philadelphia pa", "philadelphia pennsylvania", "philly"],
            "detroit": ["detroit", "detroit mi", "detroit michigan", "detroit metro"],
            "minneapolis": ["minneapolis", "minneapolis mn", "minneapolis minnesota", "twin cities"],
            "portland": ["portland", "portland or", "portland oregon"],
            "nashville": ["nashville", "nashville tn", "nashville tennessee"],
            "memphis": ["memphis", "memphis tn", "memphis tennessee"],
            "kansas city": ["kansas city", "kansas city mo", "kansas city missouri", "kansas city ks"],
            "oklahoma city": ["oklahoma city", "oklahoma city ok", "oklahoma city oklahoma"],
            "salt lake city": ["salt lake city", "salt lake city ut", "salt lake city utah", "slc"],
            "tucson": ["tucson", "tucson az", "tucson arizona"],
            "albuquerque": ["albuquerque", "albuquerque nm", "albuquerque new mexico"],
            "omaha": ["omaha", "omaha ne", "omaha nebraska"],
            "milwaukee": ["milwaukee", "milwaukee wi", "milwaukee wisconsin"],
            "tampa": ["tampa", "tampa fl", "tampa florida", "tampa bay"],
            "orlando": ["orlando", "orlando fl", "orlando florida"],
            "jacksonville": ["jacksonville", "jacksonville fl", "jacksonville florida"],
            "charlotte": ["charlotte", "charlotte nc", "charlotte north carolina"],
            "raleigh": ["raleigh", "raleigh nc", "raleigh north carolina", "research triangle"],
            "columbus": ["columbus", "columbus oh", "columbus ohio"],
            "cleveland": ["cleveland", "cleveland oh", "cleveland ohio"],
            "cincinnati": ["cincinnati", "cincinnati oh", "cincinnati ohio"],
            "pittsburgh": ["pittsburgh", "pittsburgh pa", "pittsburgh pennsylvania"],
            "buffalo": ["buffalo", "buffalo ny", "buffalo new york"],
            "rochester": ["rochester", "rochester ny", "rochester new york"],
            "albany": ["albany", "albany ny", "albany new york"],
            "baltimore": ["baltimore", "baltimore md", "baltimore maryland"],
            "richmond": ["richmond", "richmond va", "richmond virginia"],
            "norfolk": ["norfolk", "norfolk va", "norfolk virginia"],
            "virginia beach": ["virginia beach", "virginia beach va", "virginia beach virginia"],
            "louisville": ["louisville", "louisville ky", "louisville kentucky"],
            "lexington": ["lexington", "lexington ky", "lexington kentucky"],
            "knoxville": ["knoxville", "knoxville tn", "knoxville tennessee"],
            "chattanooga": ["chattanooga", "chattanooga tn", "chattanooga tennessee"],
            "birmingham": ["birmingham", "birmingham al", "birmingham alabama"],
            "montgomery": ["montgomery", "montgomery al", "montgomery alabama"],
            "mobile": ["mobile", "mobile al", "mobile alabama"],
            "huntsville": ["huntsville", "huntsville al", "huntsville alabama"],
            "jackson": ["jackson", "jackson ms", "jackson mississippi"],
            "little rock": ["little rock", "little rock ar", "little rock arkansas"],
            "des moines": ["des moines", "des moines ia", "des moines iowa"],
            "cedar rapids": ["cedar rapids", "cedar rapids ia", "cedar rapids iowa"],
            "wichita": ["wichita", "wichita ks", "wichita kansas"],
            "topeka": ["topeka", "topeka ks", "topeka kansas"],
            "springfield": ["springfield", "springfield mo", "springfield missouri"],
            "st. louis": ["st. louis", "st. louis mo", "st. louis missouri", "saint louis"],
            "columbia": ["columbia", "columbia sc", "columbia south carolina"],
            "charleston": ["charleston", "charleston sc", "charleston south carolina"],
            "greenville": ["greenville", "greenville sc", "greenville south carolina"],
            "spartanburg": ["spartanburg", "spartanburg sc", "spartanburg south carolina"],
            "wilmington": ["wilmington", "wilmington nc", "wilmington north carolina"],
            "asheville": ["asheville", "asheville nc", "asheville north carolina"],
            "greensboro": ["greensboro", "greensboro nc", "greensboro north carolina"],
            "winston salem": ["winston salem", "winston salem nc", "winston salem north carolina"],
            "durham": ["durham", "durham nc", "durham north carolina"],
            "fayetteville": ["fayetteville", "fayetteville nc", "fayetteville north carolina"],
            "savannah": ["savannah", "savannah ga", "savannah georgia"],
            "augusta": ["augusta", "augusta ga", "augusta georgia"],
            "columbus": ["columbus", "columbus ga", "columbus georgia"],
            "macon": ["macon", "macon ga", "macon georgia"],
            "gainesville": ["gainesville", "gainesville fl", "gainesville florida"],
            "tallahassee": ["tallahassee", "tallahassee fl", "tallahassee florida"],
            "pensacola": ["pensacola", "pensacola fl", "pensacola florida"],
            "fort lauderdale": ["fort lauderdale", "fort lauderdale fl", "fort lauderdale florida"],
            "west palm beach": ["west palm beach", "west palm beach fl", "west palm beach florida"],
            "sarasota": ["sarasota", "sarasota fl", "sarasota florida"],
            "naples": ["naples", "naples fl", "naples florida"],
            "fort myers": ["fort myers", "fort myers fl", "fort myers florida"],
            "clearwater": ["clearwater", "clearwater fl", "clearwater florida"],
            "st. petersburg": ["st. petersburg", "st. petersburg fl", "st. petersburg florida", "saint petersburg"],
            "lakeland": ["lakeland", "lakeland fl", "lakeland florida"],
            "daytona beach": ["daytona beach", "daytona beach fl", "daytona beach florida"],
            "melbourne": ["melbourne", "melbourne fl", "melbourne florida"],
            "palm bay": ["palm bay", "palm bay fl", "palm bay florida"],
            "boca raton": ["boca raton", "boca raton fl", "boca raton florida"],
            "coral springs": ["coral springs", "coral springs fl", "coral springs florida"],
            "hollywood": ["hollywood", "hollywood fl", "hollywood florida"],
            "miramar": ["miramar", "miramar fl", "miramar florida"],
            "pembroke pines": ["pembroke pines", "pembroke pines fl", "pembroke pines florida"],
            "hialeah": ["hialeah", "hialeah fl", "hialeah florida"],
            "miami gardens": ["miami gardens", "miami gardens fl", "miami gardens florida"],
            "plantation": ["plantation", "plantation fl", "plantation florida"],
            "sunrise": ["sunrise", "sunrise fl", "sunrise florida"],
            "tamarac": ["tamarac", "tamarac fl", "tamarac florida"],
            "lauderhill": ["lauderhill", "lauderhill fl", "lauderhill florida"],
            "weston": ["weston", "weston fl", "weston florida"],
            "davie": ["davie", "davie fl", "davie florida"],
            "cooper city": ["cooper city", "cooper city fl", "cooper city florida"],
            "pompano beach": ["pompano beach", "pompano beach fl", "pompano beach florida"],
            "deerfield beach": ["deerfield beach", "deerfield beach fl", "deerfield beach florida"],
            "boynton beach": ["boynton beach", "boynton beach fl", "boynton beach florida"],
            "delray beach": ["delray beach", "delray beach fl", "delray beach florida"],
            "boca raton": ["boca raton", "boca raton fl", "boca raton florida"],
            "jupiter": ["jupiter", "jupiter fl", "jupiter florida"],
            "west palm beach": ["west palm beach", "west palm beach fl", "west palm beach florida"],
            "palm beach gardens": ["palm beach gardens", "palm beach gardens fl", "palm beach gardens florida"],
            "wellington": ["wellington", "wellington fl", "wellington florida"],
            "royal palm beach": ["royal palm beach", "royal palm beach fl", "royal palm beach florida"],
            "greenacres": ["greenacres", "greenacres fl", "greenacres florida"],
            "lake worth": ["lake worth", "lake worth fl", "lake worth florida"],
            "lantana": ["lantana", "lantana fl", "lantana florida"],
            "manalapan": ["manalapan", "manalapan fl", "manalapan florida"],
            "hypoluxo": ["hypoluxo", "hypoluxo fl", "hypoluxo florida"],
            "lake clarke shores": ["lake clarke shores", "lake clarke shores fl", "lake clarke shores florida"],
            "atlantic": ["atlantic", "atlantic fl", "atlantic florida"],
            "south palm beach": ["south palm beach", "south palm beach fl", "south palm beach florida"],
            "briny breezes": ["briny breezes", "briny breezes fl", "briny breezes florida"],
            "gulf stream": ["gulf stream", "gulf stream fl", "gulf stream florida"],
            "highland beach": ["highland beach", "highland beach fl", "highland beach florida"],
            "delray beach": ["delray beach", "delray beach fl", "delray beach florida"],
            "boca raton": ["boca raton", "boca raton fl", "boca raton florida"],
            "deerfield beach": ["deerfield beach", "deerfield beach fl", "deerfield beach florida"],
            "lighthouse point": ["lighthouse point", "lighthouse point fl", "lighthouse point florida"],
            "hillsboro beach": ["hillsboro beach", "hillsboro beach fl", "hillsboro beach florida"],
            "pompano beach": ["pompano beach", "pompano beach fl", "pompano beach florida"],
            "lauderdale by the sea": ["lauderdale by the sea", "lauderdale by the sea fl", "lauderdale by the sea florida"],
            "sea ranch lakes": ["sea ranch lakes", "sea ranch lakes fl", "sea ranch lakes florida"],
            "lauderdale lakes": ["lauderdale lakes", "lauderdale lakes fl", "lauderdale lakes florida"],
            "lauderhill": ["lauderhill", "lauderhill fl", "lauderhill florida"],
            "tamarac": ["tamarac", "tamarac fl", "tamarac florida"],
            "north lauderdale": ["north lauderdale", "north lauderdale fl", "north lauderdale florida"],
            "plantation": ["plantation", "plantation fl", "plantation florida"],
            "sunrise": ["sunrise", "sunrise fl", "sunrise florida"],
            "weston": ["weston", "weston fl", "weston florida"],
            "davie": ["davie", "davie fl", "davie florida"],
            "cooper city": ["cooper city", "cooper city fl", "cooper city florida"],
            "pembroke pines": ["pembroke pines", "pembroke pines fl", "pembroke pines florida"],
            "miramar": ["miramar", "miramar fl", "miramar florida"],
            "hollywood": ["hollywood", "hollywood fl", "hollywood florida"],
            "dania beach": ["dania beach", "dania beach fl", "dania beach florida"],
            "hallandale beach": ["hallandale beach", "hallandale beach fl", "hallandale beach florida"],
            "aventura": ["aventura", "aventura fl", "aventura florida"],
            "sunny isles beach": ["sunny isles beach", "sunny isles beach fl", "sunny isles beach florida"],
            "bal harbour": ["bal harbour", "bal harbour fl", "bal harbour florida"],
            "bay harbor islands": ["bay harbor islands", "bay harbor islands fl", "bay harbor islands florida"],
            "surfside": ["surfside", "surfside fl", "surfside florida"],
            "indian creek": ["indian creek", "indian creek fl", "indian creek florida"],
            "miami beach": ["miami beach", "miami beach fl", "miami beach florida", "south beach", "sobe"],
            "miami": ["miami", "miami fl", "miami florida", "downtown miami", "brickell"],
            "miami gardens": ["miami gardens", "miami gardens fl", "miami gardens florida"],
            "hialeah": ["hialeah", "hialeah fl", "hialeah florida"],
            "homestead": ["homestead", "homestead fl", "homestead florida"],
            "florida city": ["florida city", "florida city fl", "florida city florida"],
            "key largo": ["key largo", "key largo fl", "key largo florida"],
            "islamorada": ["islamorada", "islamorada fl", "islamorada florida"],
            "marathon": ["marathon", "marathon fl", "marathon florida"],
            "key west": ["key west", "key west fl", "key west florida"],
            "big pine key": ["big pine key", "big pine key fl", "big pine key florida"],
            "summerland key": ["summerland key", "summerland key fl", "summerland key florida"],
            "cudjoe key": ["cudjoe key", "cudjoe key fl", "cudjoe key florida"],
            "sugarloaf key": ["sugarloaf key", "sugarloaf key fl", "sugarloaf key florida"],
            "stock island": ["stock island", "stock island fl", "stock island florida"],
            "key west": ["key west", "key west fl", "key west florida"],
            "santa clara": ["santa clara", "santa clara ca", "santa clara california", "san jose", "silicon valley"],
            "del toro": ["del toro", "del toro ca", "del toro california", "tustin", "irvine", "orange county"],
            "irvine": ["irvine", "irvine ca", "irvine california", "orange county", "south orange county"],
            "atlantic city": ["atlantic city", "atlantic city nj", "atlantic city new jersey"],
            "reno": ["reno", "reno nv", "reno nevada"],
            "toronto": ["toronto", "toronto on", "toronto ontario"],
            
            # States with common misspellings
            "kansas": ["kansas", "ks", "kansas state", "kanses", "eknzas", "kansasas"],
            "missouri": ["missouri", "mo", "missouri state", "misouri", "missouri"],
            "illinois": ["illinois", "il", "illinois state", "ilinios", "illinoise"],
            "tennessee": ["tennessee", "tn", "tennessee state", "tenesse", "tenesee"],
            "kentucky": ["kentucky", "ky", "kentucky state", "kentuckey", "kentuky"],
            "arkansas": ["arkansas", "ar", "arkansas state", "arkanses", "arkansas"],
            "louisiana": ["louisiana", "la", "louisiana state", "louisianna", "louisiana"],
            "mississippi": ["mississippi", "ms", "mississippi state", "missisippi", "mississippi"],
            "alabama": ["alabama", "al", "alabama state", "alabma", "alabama"],
            "georgia": ["georgia", "ga", "georgia state", "georga", "georgia"],
            "florida": ["florida", "fl", "florida state", "florida", "florida"],
            "south carolina": ["south carolina", "sc", "south carolina state", "south carolina", "south carolina"],
            "north carolina": ["north carolina", "nc", "north carolina state", "north carolina", "north carolina"],
            "virginia": ["virginia", "va", "virginia state", "virgina", "virginia"],
            "west virginia": ["west virginia", "wv", "west virginia state", "west virginia", "west virginia"],
            "maryland": ["maryland", "md", "maryland state", "maryland", "maryland"],
            "delaware": ["delaware", "de", "delaware state", "delware", "delaware"],
            "pennsylvania": ["pennsylvania", "pa", "pennsylvania state", "pensylvania", "pennsylvania"],
            "new jersey": ["new jersey", "nj", "new jersey state", "new jersey", "new jersey"],
            "new york": ["new york", "ny", "new york state", "new york", "new york"],
            "connecticut": ["connecticut", "ct", "connecticut state", "connecticut", "connecticut"],
            "rhode island": ["rhode island", "ri", "rhode island state", "rhode island", "rhode island"],
            "massachusetts": ["massachusetts", "ma", "massachusetts state", "massachusets", "massachusetts"],
            "vermont": ["vermont", "vt", "vermont state", "vermont", "vermont"],
            "new hampshire": ["new hampshire", "nh", "new hampshire state", "new hampshire", "new hampshire"],
            "maine": ["maine", "me", "maine state", "maine", "maine"],
            "ohio": ["ohio", "oh", "ohio state", "ohio", "ohio"],
            "indiana": ["indiana", "in", "indiana state", "indiana", "indiana"],
            "michigan": ["michigan", "mi", "michigan state", "michigan", "michigan"],
            "wisconsin": ["wisconsin", "wi", "wisconsin state", "wisconsin", "wisconsin"],
            "minnesota": ["minnesota", "mn", "minnesota state", "minnesota", "minnesota"],
            "iowa": ["iowa", "ia", "iowa state", "iowa", "iowa"],
            "nebraska": ["nebraska", "ne", "nebraska state", "nebraska", "nebraska"],
            "north dakota": ["north dakota", "nd", "north dakota state", "north dakota", "north dakota"],
            "south dakota": ["south dakota", "sd", "south dakota state", "south dakota", "south dakota"],
            "montana": ["montana", "mt", "montana state", "montana", "montana"],
            "wyoming": ["wyoming", "wy", "wyoming state", "wyoming", "wyoming"],
            "colorado": ["colorado", "co", "colorado state", "colorado", "colorado"],
            "utah": ["utah", "ut", "utah state", "utah", "utah"],
            "nevada": ["nevada", "nv", "nevada state", "navada", "nivada"],
            "california": ["california", "ca", "california state", "california", "california"],
            "oregon": ["oregon", "or", "oregon state", "oregon", "oregon"],
            "washington": ["washington", "wa", "washington state", "washington", "washington"],
            "alaska": ["alaska", "ak", "alaska state", "alaska", "alaska"],
            "hawaii": ["hawaii", "hi", "hawaii state", "hawaii", "hawaii"],
            "texas": ["texas", "tx", "texas state", "texas", "texas"],
            "oklahoma": ["oklahoma", "ok", "oklahoma state", "oklahoma", "oklahoma"],
            "new mexico": ["new mexico", "nm", "new mexico state", "new mexico", "new mexico"],
            "arizona": ["arizona", "az", "arizona state", "arizona", "arizona"],
            "idaho": ["idaho", "id", "idaho state", "idaho", "idaho"]
        }
    
    def _build_state_abbreviations(self) -> Dict[str, str]:
        """Build state abbreviation mapping"""
        return {
            "al": "alabama", "ak": "alaska", "az": "arizona", "ar": "arkansas", "ca": "california",
            "co": "colorado", "ct": "connecticut", "de": "delaware", "fl": "florida", "ga": "georgia",
            "hi": "hawaii", "id": "idaho", "il": "illinois", "in": "indiana", "ia": "iowa",
            "ks": "kansas", "ky": "kentucky", "la": "louisiana", "me": "maine", "md": "maryland",
            "ma": "massachusetts", "mi": "michigan", "mn": "minnesota", "ms": "mississippi", "mo": "missouri",
            "mt": "montana", "ne": "nebraska", "nv": "nevada", "nh": "new hampshire", "nj": "new jersey",
            "nm": "new mexico", "ny": "new york", "nc": "north carolina", "nd": "north dakota", "oh": "ohio",
            "ok": "oklahoma", "or": "oregon", "pa": "pennsylvania", "ri": "rhode island", "sc": "south carolina",
            "sd": "south dakota", "tn": "tennessee", "tx": "texas", "ut": "utah", "vt": "vermont",
            "va": "virginia", "wa": "washington", "wv": "west virginia", "wi": "wisconsin", "wy": "wyoming"
        }
    
    def _build_common_typos(self) -> Dict[str, str]:
        """Build common typo corrections"""
        return {
            "eknzas": "kansas",
            "kanses": "kansas",
            "kansasas": "kansas",
            "misouri": "missouri",
            "ilinios": "illinois",
            "illinoise": "illinois",
            "tenesse": "tennessee",
            "tenesee": "tennessee",
            "kentuckey": "kentucky",
            "kentuky": "kentucky",
            "arkanses": "arkansas",
            "louisianna": "louisiana",
            "missisippi": "mississippi",
            "alabma": "alabama",
            "georga": "georgia",
            "virgina": "virginia",
            "delware": "delaware",
            "pensylvania": "pennsylvania",
            "massachusets": "massachusetts",
            "navada": "nevada",
            "nivada": "nevada"
        }
    
    def detect_location(self, text: str) -> Optional[str]:
        """
        Detect location from text using fuzzy matching and typo correction
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected location name or None if not found
        """
        text_lower = text.lower().strip()
        
        # First, try exact matches
        for location, variations in self.locations.items():
            for variation in variations:
                if variation in text_lower:
                    logger.info(f"📍 Exact match found: '{variation}' -> '{location}'")
                    return location
        
        # Try typo correction
        for typo, correction in self.common_typos.items():
            if typo in text_lower:
                logger.info(f"📍 Typo correction: '{typo}' -> '{correction}'")
                return correction
        
        # Try fuzzy matching for partial matches
        words = text_lower.split()
        for word in words:
            # Skip common words
            if word in ['in', 'at', 'near', 'around', 'by', 'of', 'the', 'a', 'an']:
                continue
                
            # Try fuzzy matching against all location variations
            best_match = None
            best_score = 0
            
            for location, variations in self.locations.items():
                for variation in variations:
                    # Check if word is similar to variation
                    score = fuzz.ratio(word, variation)
                    if score > 70 and score > best_score:  # 70% similarity threshold
                        best_match = location
                        best_score = score
            
            if best_match:
                logger.info(f"📍 Fuzzy match found: '{word}' -> '{best_match}' (score: {best_score})")
                return best_match
        
        # Try state abbreviation lookup
        for abbr, full_name in self.state_abbreviations.items():
            if abbr in text_lower or full_name in text_lower:
                logger.info(f"📍 State match found: '{abbr}'/'{full_name}' -> '{full_name}'")
                return full_name
        
        logger.info(f"📍 No location detected in: '{text}'")
        return None
    
    def get_location_variations(self, location: str) -> List[str]:
        """Get all variations for a given location"""
        return self.locations.get(location.lower(), [])
    
    def is_valid_location(self, location: str) -> bool:
        """Check if a location exists in the database"""
        return location.lower() in self.locations or location.lower() in self.state_abbreviations.values()

# Global instance
location_detector = LocationDetector()
