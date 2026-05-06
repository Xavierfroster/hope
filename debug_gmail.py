import sys

# CRITICAL: Monkeypatch 're' with 'regex' to fix the broken system 're' module
import regex
import re

# Swap the core functions
re.compile = regex.compile
re.sub = regex.sub
re.subn = regex.subn
re.split = regex.split
re.findall = regex.findall
re.finditer = regex.finditer
re.match = regex.match
re.fullmatch = regex.fullmatch
re.search = regex.search

# Provide a dummy _compile_template if something still looks for it
def _patched_compile_template(pattern, repl):
    return regex.compile(pattern)
re._compile_template = _patched_compile_template

import os
# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from hope.communication import gmail_api
    from hope.configuration import settings as config
    
    print("Attempting to initialize Gmail Service...")
    service = gmail_api.get_gmail_service()
    print("Service initialized successfully!")
    
except Exception as e:
    print(f"\nAN ERROR OCCURRED: {e}")
    import traceback
    traceback.print_exc()
