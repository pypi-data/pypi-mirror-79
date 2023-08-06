# -*- coding: utf-8 -*-
"""Function base form of dddice roller implementation."""

from typing import NamedTuple, Tuple, List

from .utilities import (
    instruction_builder,
    instruction_parser,
    cherrypick_roll,
    roll_dices,
)


class DiceRoll(NamedTuple):
    instruction: str
    picks: Tuple
    rolls: List
    modifier: int
    value: int


def dice_roll(
    instruction: str = None,
    die: int = 0,
    quantity: int = 0,
    pick: int = 0,
    best: bool = True,
    modifier: int = 0,
) -> DiceRoll:
    if not (die or instruction):
        raise AttributeError(
            "Atleast die or instruction value must be pass. Where die > 0"
        )
    if instruction is None:
        instruction = instruction_builder(
            die=die, quantity=quantity, pick=pick, best=best, modifier=modifier
        )
    roll_instruction, pick_instruction, modifier = instruction_parser(
        instruction=instruction
    )
    rolls: List[int] = roll_dices(**roll_instruction)
    picks: Tuple = cherrypick_roll(rolls=rolls, **pick_instruction)
    return DiceRoll(
        instruction=instruction,
        rolls=rolls,
        picks=picks,
        modifier=modifier,
        value=sum(picks) + modifier,
    )
