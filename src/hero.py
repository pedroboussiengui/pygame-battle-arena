from dataclasses import dataclass

@dataclass
class Hero:
    max_health: int
    current_health: int
    max_mana: int
    current_mana: int

    