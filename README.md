## Playing Manually

```
from solver import Game
game = Game()
game.add_turn([
    ("n", "position"),
    ("o", "wrong"),
    ("t", "position"),
    ("e", "wrong"),
    ("s", "wrong"),
])
game.add_turn([
    ("a", "position"),
    ("c", "wrong"),
    ("r", "wrong"),
    ("i", "wrong"),
    ("d", "wrong"),
])
game.possible_words
game.add_turn([
    ("p", "right"),
    ("a", "position"),
    ("n", "position"),
    ("t", "position"),
    ("y", "wrong"),
])
```

## Evaluate Current Strategy

`python evaluate_strategy.py`
