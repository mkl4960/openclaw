import os
from agentmail import AgentMail

api_key = os.getenv('AGENTMAIL_API_KEY')
if not api_key:
    print("AGENTMAIL_API_KEY not set")
    exit(1)

client = AgentMail(api_key=api_key)
print("Client created")

try:
    inboxes = client.inboxes.list()
    print(f"Inboxes response: {inboxes}")
    print(f"Number of inboxes: {len(inboxes.inboxes)}")
    for inbox in inboxes.inboxes:
        print(f"Inbox: {inbox.id} - {inbox.email}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")