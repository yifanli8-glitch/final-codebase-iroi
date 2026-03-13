#!/usr/bin/env python3

import re
import json
from typing import Optional, Dict, Any


WAYPOINT_MAP = {
    "one": "W1", "1": "W1", "point one": "W1", "point 1": "W1",
    "two": "W2", "2": "W2", "point two": "W2", "point 2": "W2",
    "three": "W3", "3": "W3", "point three": "W3", "point 3": "W3",
    "four": "W4", "4": "W4", "point four": "W4", "point 4": "W4",
    "five": "W5", "5": "W5", "point five": "W5", "point 5": "W5",
    "w1": "W1", "w2": "W2", "w3": "W3", "w4": "W4", "w5": "W5",
}

COMMAND_PATTERNS = [
    (r"go to (?:point )?(.+)", "navigate"),
    (r"move to (?:point )?(.+)", "navigate"),
    (r"navigate to (?:point )?(.+)", "navigate"),
    (r"take me to (?:point )?(.+)", "navigate"),
    (r"come to me", "move_to_user"),
    (r"come here", "move_to_user"),
    (r"find me", "move_to_user"),
    (r"stop", "stop"),
    (r"halt", "stop"),
]


def parse_command(text: str) -> Optional[Dict[str, Any]]:
    if not text:
        return None
    
    text = text.lower().strip()
    
    for pattern, cmd_type in COMMAND_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if cmd_type == "navigate":
                target_text = match.group(1).strip().lower()
                target = _resolve_waypoint(target_text)
                if target:
                    return {"type": "navigate", "target": target}
            elif cmd_type in ("move_to_user", "stop"):
                return {"type": cmd_type}
    
    return None


def _resolve_waypoint(text: str) -> Optional[str]:
    text = text.lower().strip()
    
    if text in WAYPOINT_MAP:
        return WAYPOINT_MAP[text]
    
    for key, value in WAYPOINT_MAP.items():
        if key in text:
            return value
    
    return None


def command_to_json(command: Dict[str, Any]) -> str:
    return json.dumps(command)


if __name__ == "__main__":
    test_cases = [
        "go to point three",
        "go to W3",
        "move to point 2",
        "navigate to point one",
        "come to me",
        "stop",
        "take me to point four",
        "hello",
    ]
    
    print("Command Parser Test")
    print("=" * 40)
    for text in test_cases:
        result = parse_command(text)
        print(f"'{text}' -> {result}")
