"""
Generator that yields one scenario at a time from a markdown file
where each scenario starts with '### SCENARIUSZ' and is followed by its description.
"""

import re
from typing import Iterator
import os

def scenariusz_generator(filepath: str) -> Iterator[str]:
 
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print("uruchomione")
    parts = re.split(r'^### SCENARIUSZ\s*', content, flags=re.MULTILINE)
    for part in parts:
        scenario = part.strip()
        if scenario:
            yield scenario


if __name__ == "__main__":
    scenario_path = os.path.abspath(r'data/scenariusze.md')
    filepath = scenario_path
    count = 0
    for scenario in scenariusz_generator(filepath):
        count += 1
        print(scenario)
        print("-" * 40)
        if count > 5:
            break
