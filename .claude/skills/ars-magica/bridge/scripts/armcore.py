#!/usr/bin/env python3
"""
armcore.py — shared plumbing for the Ars Magica companion scripts.

Locates the bridge's data/, imports the mythic-gm engine's lists.py so the campaign
Lists (threads.json / characters.json / adventure.json) are read & written in the EXACT
engine schema, and load/saves the per-year theme state (year-state.json). No randomness
lives here (see armdice.py); nothing here invents results.
"""
import json, os, sys

HERE   = os.path.dirname(os.path.abspath(__file__))          # …/ars-magica/bridge/scripts
BRIDGE = os.path.dirname(HERE)                               # …/ars-magica/bridge
DATA   = os.path.join(BRIDGE, "data")
ENGINE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "mythic-gm", "scripts"))

# ---- engine lists.py (schema-compatible state) -------------------------------
sys.path.insert(0, ENGINE)
try:
    import lists as engine_lists          # load_list/save_list/load_adventure/save_adventure/add_entry…
except Exception as e:                    # pragma: no cover - surfaces a clear error if the engine moved
    engine_lists = None
    _ENGINE_ERR = e

def lists():
    if engine_lists is None:
        sys.exit(f"Could not import the engine's lists.py from {ENGINE}: {_ENGINE_ERR}")
    return engine_lists

# ---- bridge data -------------------------------------------------------------
def load_rule(name):
    """Load data/rules/<name>.json."""
    return json.load(open(os.path.join(DATA, "rules", name + ".json"), encoding="utf-8"))

def iter_element_files():
    d = os.path.join(DATA, "elements")
    if not os.path.isdir(d): return []
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".json")]

def load_all_elements():
    """Flatten every data/elements/*.json into one id->record dict (records carry their own type)."""
    out = {}
    for f in iter_element_files():
        obj = json.load(open(f, encoding="utf-8"))
        for rec in obj.get("elements", []):
            rec.setdefault("type", obj.get("type"))
            out[rec["id"]] = rec
    return out

# ---- per-year theme/coverage state ------------------------------------------
THEMES = ["Action", "Tension", "Mystery", "Social", "Personal"]

def year_path(campaign): return os.path.join(campaign, "year-state.json")

def load_year(campaign):
    p = year_path(campaign)
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8"))
    return None

def save_year(campaign, obj):
    json.dump(obj, open(year_path(campaign), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- tiny shared CLI arg helpers --------------------------------------------
def opt(argv, flag, default=None, cast=str):
    if flag in argv:
        try: return cast(argv[argv.index(flag) + 1])
        except (IndexError, ValueError): sys.exit(f"Bad/missing value for {flag}")
    return default

def has(argv, flag): return flag in argv
