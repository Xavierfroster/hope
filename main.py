from core import takecmd, speak
from features import wishme, execute_query, check_internet

if __name__ == "__main__":
    check_internet()
    wishme()
    while True:
        query = takecmd().lower()
        if "none" in query:
            continue
            
        # Phase 2: Wake Word Detection ("hey hope" or "hope")
        if query.startswith("hey hope") or query.startswith("hope"):
            speak("Yes sir?")
            # Process the rest of the string if there are other commands in the same sentence
            clean_query = query.replace("hey hope", "").replace("hope", "").strip()
            
            if not clean_query:
                # If they only said "hey hope", listen for the actual command
                clean_query = takecmd().lower()
            
            if "none" not in clean_query:
                execute_query(clean_query)
        else:
            # We strictly enforce wake word based on PRD Phase 2
            print("Wake word 'Hope' not detected. Ignoring command.")