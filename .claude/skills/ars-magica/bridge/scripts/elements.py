#!/usr/bin/env python3
"""
elements.py — the atomic setting-element library (hooks: generate:element, seeds).

Setting facts (Houses, Tribunals, Realms, Code clauses, NPC archetypes, hooks, …) live as
addressable JSON records in ../data/elements/*.json. They can be searched, shown, INSERTED as
live Threads/Characters (engine-schema entries that the dice roll, carrying their element
payload), SURFACED by relevance to the current scene, or rolled fresh.

Commands:
  search [--type T] [--tag X] [--text Q]          list matching element ids
  show <id>                                        full record
  insert <id> --into thread|character --campaign DIR [--weight N] [--name "…"]
  surface --campaign DIR [--here "tags,words"] [--n 8]
  new --type T --campaign DIR [--insert thread|character]
"""
import random, sys
import armcore as C

def _match(rec, typ, tag, text):
    if typ and rec.get("type") != typ: return False
    if tag and tag.lower() not in [t.lower() for t in rec.get("tags", [])]: return False
    if text:
        blob = " ".join(str(rec.get(k, "")) for k in
                        ("name", "summary", "wants", "as_thread", "as_character")).lower()
        blob += " " + " ".join(rec.get("tags", [])).lower()
        if text.lower() not in blob: return False
    return True

def cmd_search(argv):
    typ = C.opt(argv, "--type"); tag = C.opt(argv, "--tag"); text = C.opt(argv, "--text")
    hits = [r for r in C.load_all_elements().values() if _match(r, typ, tag, text)]
    print(f"🔎 {len(hits)} element(s):")
    for r in sorted(hits, key=lambda x: x["id"]):
        print(f"   {r['id']:28} [{r.get('type','?')}] {r['name']}  — tags: {','.join(r.get('tags', []))}")

def cmd_show(argv):
    if len(argv) < 2: sys.exit("show <id>")
    rec = C.load_all_elements().get(argv[1])
    if not rec: sys.exit(f"no element '{argv[1]}'")
    print(f"📜 {rec['id']}  [{rec.get('type')}]  {rec['name']}")
    for k in ("realm", "summary", "wants", "as_character", "as_thread", "tags", "relations", "source"):
        if rec.get(k): print(f"   {k}: {rec[k]}")

def _live_entries(campaign):
    L = C.lists(); out = []
    for kind in ("thread", "character"):
        for e in L.load_list(campaign, kind).get("entries", []):
            out.append((kind, e))
    return out

def cmd_insert(argv):
    if len(argv) < 2: sys.exit("insert <id> --into thread|character --campaign DIR")
    rec = C.load_all_elements().get(argv[1])
    if not rec: sys.exit(f"no element '{argv[1]}'")
    into = C.opt(argv, "--into"); campaign = C.opt(argv, "--campaign")
    if into not in ("thread", "character") or not campaign:
        sys.exit("need --into thread|character and --campaign DIR")
    weight = C.opt(argv, "--weight", 1, int)
    name = C.opt(argv, "--name") or (rec["name"] if into == "character"
                                     else rec.get("as_thread") or rec["name"])
    L = C.lists(); obj = L.load_list(campaign, into)
    if any(e["name"].strip().lower() == name.strip().lower() for e in obj["entries"]):
        sys.exit(f"'{name}' already on the {into} list")
    obj["entries"].append({"name": name, "weight": max(1, min(3, weight)),
                           "element_id": rec["id"], "tags": rec.get("tags", []),
                           "realm": rec.get("realm"), "status": "active"})
    L.save_list(campaign, obj)
    print(f"➕ inserted {rec['id']} as a {into}: \"{name}\" (weight {weight})  → {into}s.json")
    print(f"   payload: tags {rec.get('tags', [])}" + (f", realm {rec['realm']}" if rec.get('realm') else ""))
    print("   (the engine's dice now roll it like any List entry; surface its detail when invoked.)")

def cmd_surface(argv):
    campaign = C.opt(argv, "--campaign")
    if not campaign: sys.exit("surface needs --campaign DIR")
    here = [w.strip().lower() for w in (C.opt(argv, "--here", "") or "").replace(",", " ").split() if w.strip()]
    n = C.opt(argv, "--n", 8, int)
    live = _live_entries(campaign)
    context = set(here)
    for _, e in live:                       # open Threads/Characters contribute their tags + realm
        context.update(t.lower() for t in e.get("tags", []))
        if e.get("realm"): context.add(str(e["realm"]).lower())
    inserted_ids = {e.get("element_id") for _, e in live if e.get("element_id")}
    scored = []
    for r in C.load_all_elements().values():
        if r["id"] in inserted_ids: continue
        tags = set(t.lower() for t in r.get("tags", []))
        if r.get("realm"): tags.add(str(r["realm"]).lower())
        overlap = len(tags & context)
        if overlap: scored.append((overlap, r))
    scored.sort(key=lambda x: (-x[0], x[1]["id"]))
    print(f"🃏 surfacing {min(n, len(scored))} relevant element(s) for context {sorted(context) or '(none)'}:")
    if not scored:
        print("   (no tag overlap — roll a fresh one: `element new --type hook` / `realm_encounter`)")
    for ov, r in scored[:n]:
        hint = r.get("as_thread") or r.get("summary") or ""
        print(f"   ·{ov}  {r['id']:26} {r['name']} — {hint}")

def cmd_new(argv):
    typ = C.opt(argv, "--type")
    if not typ: sys.exit("new --type T [--campaign DIR --insert thread|character]")
    pool = [r for r in C.load_all_elements().values() if r.get("type") == typ]
    if not pool: sys.exit(f"no elements of type '{typ}'")
    r = random.choice(pool)
    print(f"🎲 new {typ}: {r['id']} — {r['name']}")
    print(f"   {r.get('summary', '')}")
    into = C.opt(argv, "--insert"); campaign = C.opt(argv, "--campaign")
    if into and campaign:
        cmd_insert([None, r["id"], "--into", into, "--campaign", campaign])

def run(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    {"search": cmd_search, "show": cmd_show, "insert": cmd_insert,
     "surface": cmd_surface, "new": cmd_new}.get(
        argv[0], lambda a: sys.exit(f"unknown element command '{argv[0]}'"))(argv)

if __name__ == "__main__":
    run(sys.argv[1:])
