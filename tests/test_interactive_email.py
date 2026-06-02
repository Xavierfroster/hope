import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hope import features
from hope import core
from hope import memory
import time

# Mocking
def mock_speak(audio, query=None):
    print(f"\n[HOPE]: {audio}")

# Dynamic mock for takecmd to simulate conversation
inputs = []
def mock_takecmd():
    if inputs:
        val = inputs.pop(0)
        print(f"[INPUT SIM]: {val}")
        return val
    return "None"

def mock_send_email(to, content):
    print(f"[SYSTEM]: Mock sending email to {to} with content: {content}")

features.sendEmail = mock_send_email
core.speak = mock_speak
features.speak = mock_speak
features.takecmd = mock_takecmd

def run_test(query, user_inputs):
    global inputs
    inputs = user_inputs
    print(f"\n--- STARTING EMAIL TEST: \"{query}\" ---")
    features.execute_query(query)

# 1. Test: New contact and saving it
# User says: email -> Hope asks who -> User gives email -> Hope asks save -> User says yes -> Hope asks name -> User says Kumar
run_test("send an email", ["test@example.com", "yes", "Kumar", "This is a test message"])

# 2. Test: Recalling the contact
# User says: email to Kumar -> Hope finds it -> Hope asks content -> User gives content
run_test("email to Kumar", ["This is the second test message using saved contact"])

print("\n--- TEST COMPLETE ---")
