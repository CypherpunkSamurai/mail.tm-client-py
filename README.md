# mail.tm-client-py
A simple client module for mail.tm

## Example Usage

1. Download the `.py` file from this repo
2. Import `MailTMClient` from the module

```py
import json
import time
# import
from mtm import MailTMClient

# pretty printing html emails
def print_message_nicely(message):
    """Print message in a readable format"""
    print("\n" + "="*50)
    print(f"From: {message.get('from', {}).get('address', 'Unknown')}")
    print(f"Subject: {message.get('subject', 'No subject')}")
    print(f"Date: {message.get('createdAt', 'Unknown')}")
    print("-"*50)

    # Handle HTML content by showing just text for simplicity
    content = message.get('text', message.get('html', 'No content'))
    if len(content) > 500:
        content = content[:500] + "... [truncated]"
    print(content)
    print("="*50 + "\n")


# Initialize client
client = MailTMClient()

# Get available domains
domains = client.get_domains()
print("Available domains:", domains)

# Create a random account
account, password = client.generate_random_account()
print("Created account:", account)
print("Account password:", password)

# Get authentication token
token = client.get_token(account['address'], password)
print("Authentication token:", token)

# Get account info
me = client.get_me()
print("Account info:", me)

# Get messages
message_list = client.get_message_list()
message_count = client.get_message_count()
print(f"Messages: {message_count} found")

# Example message operations
if message_count > 0:
    message_id = message_list[0]['id']
    message = client.get_message(message_id)
    print_message_nicely(message)

    # Mark message as seen
    seen_status = client.mark_as_seen(message_id)
    print("Marked as seen:", seen_status)
```

## Credits

- mail.tm
