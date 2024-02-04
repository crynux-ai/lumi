"""
TODO: test cases:

1. Normal new user join:
    /user join
expect: receive welcome message both in original channel and new channel.

2. Join a channel without bot:
    remove bot from channel
    /user join
expect: HappyAIGen bot is not in guild:channel, ask admin to fix

3. Join twice
    /user join
    /user join
expect: you've already joined, show credit

4. No private channel
expect: We cannot join any channel, ask admin to fix

5. Join, remove, join
    /user join
    remove user
    /user join
expect: Add user to a channel. We've added you back, show credit, welcome in the new channel.

6. Join from DM
    /user join
expect: Ask to join from a guild channel

"""
