from hope.core import takecmd, speak
from hope.features import wishme, execute_query, check_internet
from hope import config

if __name__ == "__main__":
    check_internet()
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