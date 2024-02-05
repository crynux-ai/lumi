"""
TODO: test cases

1. Usual start
    A: /pixel start
    B: /pixel start
expect: Respond "Matching...", then a game starts, share message to both users.

2. Not start from assigned channel
    A: /pixel start in publi chcannel
expect: can you type start from [channel](link)

3. Start before join
    A: no join but start
expect: can you /join from [punlic channel](link)

4. Not enough user
    A: /pixel start
expect: Respond "Matching...". After 10 min, "No player found"

5. No enough credit to start
    A: /pixel start
expect: Respond "Not enough credit, you can invite your friends or start Crynux Nodes to earn"

6. Timeout while waiting
expect: Respond "Timeout"

"""