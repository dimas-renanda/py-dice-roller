#!/usr/bin/env python3
"""Roll NdM dice from the CLI."""
import sys, secrets, re, argparse

def roll(notation, drop_lowest=False, verbose=False):
    m = re.match(r'^(\d+)d(\d+)([+-]\d+)?$', notation.lower())
    if not m: raise ValueError(f"Invalid notation: {notation}. Use NdM or NdM+bonus")
    n, sides = int(m.group(1)), int(m.group(2))
    bonus = int(m.group(3) or 0)
    if n < 1 or sides < 1: raise ValueError("N and M must be positive")
    rolls = [secrets.randbelow(sides)+1 for _ in range(n)]
    used = rolls[:]
    if drop_lowest and len(rolls) > 1: used = sorted(rolls)[1:]
    total = sum(used) + bonus
    if verbose or n > 1:
        print(f"  🎲 {notation}: {rolls}", end="")
        if drop_lowest and len(rolls) > 1: print(f" (drop {min(rolls)})", end="")
        if bonus: print(f" + bonus({bonus:+d})", end="")
        print(f" = {total}")
    else:
        print(f"  🎲 {notation}: {total}")
    return total

p = argparse.ArgumentParser()
p.add_argument("dice", nargs="*", default=["1d6"])
p.add_argument("--drop-lowest","-dl",action="store_true")
p.add_argument("--verbose","-v",action="store_true")
args = p.parse_args()

for d in args.dice:
    try: roll(d, args.drop_lowest, args.verbose or len(args.dice)>1)
    except Exception as e: print(f"  Error: {e}")
