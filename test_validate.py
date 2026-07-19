#!/usr/bin/env python3
"""
Quick validation script to test the fetcher locally.
"""
import sys
sys.path.insert(0, '.')
from fetch_and_combine import normalize_name, is_wanted, WANTED_CHANNELS

# Test normalization
print("Testing normalization:")
tests = [
    "  Jaya TV  ",
    "Jaya TV (720p)",
    "[HD] Jaya TV",
    "jaya tv",
    "JAYA TV",
]
for t in tests:
    print(f"  '{t}' -> '{normalize_name(t)}'")

# Test wanted matching
print("\nTesting wanted matching:")
test_channels = [
    {"name": "Jaya TV", "norm": normalize_name("Jaya TV")},
    {"name": "Jaya TV (720p)", "norm": normalize_name("Jaya TV (720p)")},
    {"name": "Unknown Channel", "norm": normalize_name("Unknown Channel")},
    {"name": "Apple TV KLM", "norm": normalize_name("Apple TV KLM")},
    {"name": "Zee Tamil HD", "norm": normalize_name("Zee Tamil HD")},
]
for ch in test_channels:
    result = is_wanted(ch)
    print(f"  {'✓' if result else '✗'} {ch['name']}")

print(f"\nTotal wanted channels in config: {len(WANTED_CHANNELS)}")
