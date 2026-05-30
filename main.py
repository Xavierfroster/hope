import sys
import re
import regex
import time

# --- Python 3.13 / System 're' Module Fix ---
# Bypasses "Template compilation is not supported" error by using 'regex' library
re.compile = regex.compile
re.sub = regex.sub
re.subn = regex.subn
re.split = regex.split
re.findall = regex.findall
re.finditer = regex.finditer
re.match = regex.match
re.fullmatch = regex.fullmatch
re.search = regex.search
def _patched_compile_template(pattern, repl): return regex.compile(pattern)
re._compile_template = _patched_compile_template
# --------------------------------------------

from hope.core.engine import takecmd, speak
from hope.features import wishme, execute_query, check_internet
from hope.configuration import settings as config

if __name__ == "__main__":
    check_internet()
    time.sleep(2) # Delay after starting before greeting
    wishme()
    while True:
        query = takecmd().lower()
        if "none" in query:
            continue
            
        # Phase 2: Wake Word Detection
        if query.startswith(f"hey {config.WAKE_WORD}") or query.startswith(config.WAKE_WORD):
            speak("Yes sir?")
            # Process the rest of the string
            clean_query = query.replace(f"hey {config.WAKE_WORD}", "").replace(config.WAKE_WORD, "").strip()
            
            if not clean_query:
                # If they only said "hey hope", listen for the actual command
                clean_query = takecmd().lower()
            
            if "none" not in clean_query:
                execute_query(clean_query)
        else:
            # We strictly enforce wake word based on PRD Phase 2
            print("Wake word 'Hope' not detected. Ignoring command.")