# RuleChecker Test Harness

Takes input from STDIN and outputs "legal" or "illegal" to STDOUT.

### Example run
In command line: .\xrules < 1-in.json

### Test Cases
Test 1: Legal because move is not suicidal.

Test 2: Illegal because player move would be on edge, and player has other options.

Test 3: Legal because player would be on edge but has no other option.

Test 4: Illegal because player would collide with another player, and player has other options.

Test 5: Legal because player would collide with another player but has no other option.
