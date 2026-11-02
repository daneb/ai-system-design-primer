"""Write an Anki package (.apkg) with the standard library only.

Used by `python3 scripts/primer.py anki`. The collection schema and the default `col` row are adapted
from genanki (https://github.com/kerrickstaley/genanki, MIT License, Copyright (c) 2017 Kerrick
Staley). The legacy collection format (schema 11) is what Anki's package importer reads.

Design choices:
- One note type with Front, Back and Section fields.
- One sub-deck per part ("AI System Design Primer::Part 3: Components, in request order").
- A note's GUID comes from its section ID and question, so re-importing an updated deck changes the
  answer in place and keeps the learner's review history. Rewording a question makes a new card.
- Deck and note-type IDs are fixed hashes, so every build targets the same decks.
"""
import hashlib
import html
import json
import os
import sqlite3
import tempfile
import time
import zipfile

SCHEMA = """
CREATE TABLE col (
    id              integer primary key,
    crt             integer not null,
    mod             integer not null,
    scm             integer not null,
    ver             integer not null,
    dty             integer not null,
    usn             integer not null,
    ls              integer not null,
    conf            text not null,
    models          text not null,
    decks           text not null,
    dconf           text not null,
    tags            text not null
);
CREATE TABLE notes (
    id              integer primary key,   /* 0 */
    guid            text not null,         /* 1 */
    mid             integer not null,      /* 2 */
    mod             integer not null,      /* 3 */
    usn             integer not null,      /* 4 */
    tags            text not null,         /* 5 */
    flds            text not null,         /* 6 */
    sfld            integer not null,      /* 7 */
    csum            integer not null,      /* 8 */
    flags           integer not null,      /* 9 */
    data            text not null          /* 10 */
);
CREATE TABLE cards (
    id              integer primary key,   /* 0 */
    nid             integer not null,      /* 1 */
    did             integer not null,      /* 2 */
    ord             integer not null,      /* 3 */
    mod             integer not null,      /* 4 */
    usn             integer not null,      /* 5 */
    type            integer not null,      /* 6 */
    queue           integer not null,      /* 7 */
    due             integer not null,      /* 8 */
    ivl             integer not null,      /* 9 */
    factor          integer not null,      /* 10 */
    reps            integer not null,      /* 11 */
    lapses          integer not null,      /* 12 */
    left            integer not null,      /* 13 */
    odue            integer not null,      /* 14 */
    odid            integer not null,      /* 15 */
    flags           integer not null,      /* 16 */
    data            text not null          /* 17 */
);
CREATE TABLE revlog (
    id              integer primary key,
    cid             integer not null,
    usn             integer not null,
    ease            integer not null,
    ivl             integer not null,
    lastIvl         integer not null,
    factor          integer not null,
    time            integer not null,
    type            integer not null
);
CREATE TABLE graves (
    usn             integer not null,
    oid             integer not null,
    type            integer not null
);
CREATE INDEX ix_notes_usn on notes (usn);
CREATE INDEX ix_cards_usn on cards (usn);
CREATE INDEX ix_revlog_usn on revlog (usn);
CREATE INDEX ix_cards_nid on cards (nid);
CREATE INDEX ix_cards_sched on cards (did, queue, due);
CREATE INDEX ix_revlog_cid on revlog (cid);
CREATE INDEX ix_notes_csum on notes (csum);
"""

COL = r"""
INSERT INTO col VALUES(
    null,
    1411124400,
    1425279151694,
    1425279151690,
    11,
    0,
    0,
    0,
    '{
        "activeDecks": [
            1
        ],
        "addToCur": true,
        "collapseTime": 1200,
        "curDeck": 1,
        "curModel": "1425279151691",
        "dueCounts": true,
        "estTimes": true,
        "newBury": true,
        "newSpread": 0,
        "nextPos": 1,
        "sortBackwards": false,
        "sortType": "noteFld",
        "timeLim": 0
    }',
    '{}',
    '{
        "1": {
            "collapsed": false,
            "conf": 1,
            "desc": "",
            "dyn": 0,
            "extendNew": 10,
            "extendRev": 50,
            "id": 1,
            "lrnToday": [
                0,
                0
            ],
            "mod": 1425279151,
            "name": "Default",
            "newToday": [
                0,
                0
            ],
            "revToday": [
                0,
                0
            ],
            "timeToday": [
                0,
                0
            ],
            "usn": 0
        }
    }',
    '{
        "1": {
            "autoplay": true,
            "id": 1,
            "lapse": {
                "delays": [
                    10
                ],
                "leechAction": 0,
                "leechFails": 8,
                "minInt": 1,
                "mult": 0
            },
            "maxTaken": 60,
            "mod": 0,
            "name": "Default",
            "new": {
                "bury": true,
                "delays": [
                    1,
                    10
                ],
                "initialFactor": 2500,
                "ints": [
                    1,
                    4,
                    7
                ],
                "order": 1,
                "perDay": 20,
                "separate": true
            },
            "replayq": true,
            "rev": {
                "bury": true,
                "ease4": 1.3,
                "fuzz": 0.05,
                "ivlFct": 1,
                "maxIvl": 36500,
                "minSpace": 1,
                "perDay": 100
            },
            "timer": 0,
            "usn": 0
        }
    }',
    '{}'
);
"""

ROOT_DECK = "AI System Design Primer"
MODEL_NAME = "AI System Design Primer (Q and A)"
CSS = """.card { font-family: Inter, "Helvetica Neue", Arial, sans-serif; font-size: 20px;
  text-align: left; color: #0b0b0b; background: #fcfcfb; line-height: 1.45; max-width: 40em; margin: 0 auto; }
.section { margin-top: 1.5em; font-size: 14px; color: #52514e; }
hr#answer { border: 0; border-top: 1px solid #e7e6e2; margin: 1em 0; }
.nightMode.card, .night_mode .card { color: #f0efec; background: #1a1a19; }
.nightMode .section, .night_mode .section { color: #c3c2b7; }"""
BASE91 = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
          "!#$%&()*+,-./:;<=>?@[]^_`{|}~")


COL_DEFAULT_DECK = '{"collapsed": false, "conf": 1, "desc": "", "dyn": 0, "extendNew": 10, "extendRev": 50, "id": 1, "lrnToday": [0, 0], "mod": 1425279151, "name": "Default", "newToday": [0, 0], "revToday": [0, 0], "timeToday": [0, 0], "usn": 0}'


def stable_id(*parts):
    """An ID in [2**30, 2**31) from a hash (the range genanki recommends), stable across builds."""
    h = int(hashlib.sha256("::".join(parts).encode()).hexdigest()[:8], 16)
    return (1 << 30) + h % (1 << 30)


def guid_for(*values):
    """Anki-style base91 GUID from the first 8 bytes of a SHA-256 (same scheme as genanki)."""
    n = int.from_bytes(hashlib.sha256("__".join(values).encode()).digest()[:8], "big")
    out = ""
    while n:
        n, r = divmod(n, len(BASE91))
        out = BASE91[r] + out
    return out


def checksum(text):
    """Anki's first-field checksum: first 8 hex digits of SHA-1, as an integer."""
    return int(hashlib.sha1(text.encode()).hexdigest()[:8], 16)


def _model(model_id, deck_id, now):
    field = lambda name, ord_: {"name": name, "ord": ord_, "font": "Arial", "media": [], "rtl": False,
                                 "size": 20, "sticky": False}
    return {
        "css": CSS, "did": deck_id, "id": str(model_id), "name": MODEL_NAME, "mod": now, "usn": -1,
        "flds": [field("Front", 0), field("Back", 1), field("Section", 2)],
        "tmpls": [{"name": "Card 1", "ord": 0, "did": None, "bafmt": "", "bqfmt": "", "bfont": "",
                   "bsize": 0, "qfmt": "{{Front}}",
                   "afmt": '{{FrontSide}}<hr id="answer">{{Back}}<div class="section">{{Section}}</div>'}],
        "req": [[0, "all", [0]]], "sortf": 0, "tags": [], "type": 0, "vers": [],
        "latexPre": "\\documentclass[12pt]{article}\n\\begin{document}\n", "latexPost": "\\end{document}",
        "latexsvg": False,
    }


def _deck(deck_id, name, now, desc=""):
    return {"id": deck_id, "name": name, "desc": desc, "mod": now, "usn": -1, "collapsed": False,
            "conf": 1, "dyn": 0, "extendNew": 0, "extendRev": 50,
            "lrnToday": [0, 0], "newToday": [0, 0], "revToday": [0, 0], "timeToday": [0, 0]}


def write_apkg(path, cards, description=""):
    """cards: dicts with part_name, section_id, section_title, question, answer, tags (list)."""
    now = int(time.time())
    model_id = stable_id(MODEL_NAME)
    decks = {"1": json.loads(COL_DEFAULT_DECK)}
    root_id = stable_id(ROOT_DECK)
    decks[str(root_id)] = _deck(root_id, ROOT_DECK, now, description)
    fd, db = tempfile.mkstemp(suffix=".anki2")
    os.close(fd)
    try:
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.executescript(SCHEMA)
        cur.executescript(COL)
        next_id = now * 1000
        for position, c in enumerate(cards, 1):
            name = f"{ROOT_DECK}::{c['part_name']}"
            deck_id = stable_id(name)
            decks.setdefault(str(deck_id), _deck(deck_id, name, now))
            front = html.escape(c["question"])
            fields = [front, html.escape(c["answer"]),
                      html.escape(f"{c['section_id']} {c['section_title']}")]
            next_id += 1
            note_id = next_id
            cur.execute("INSERT INTO notes VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        (note_id, guid_for(c["section_id"], c["question"]), model_id, now, -1,
                         " " + " ".join(c["tags"]) + " ", "\x1f".join(fields), front,
                         checksum(c["question"]), 0, ""))
            next_id += 1
            cur.execute("INSERT INTO cards VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (next_id, note_id, deck_id, 0, now, -1, 0, 0, position,
                         0, 0, 0, 0, 0, 0, 0, 0, ""))
        cur.execute("UPDATE col SET decks = ?, models = ?, mod = ?",
                    (json.dumps(decks), json.dumps({str(model_id): _model(model_id, root_id, now)}),
                     now * 1000))
        con.commit()
        con.close()
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.write(db, "collection.anki2")
            z.writestr("media", "{}")
    finally:
        os.remove(db)
    return len(cards)


def check_apkg(path):
    """Structural checks on a written package; returns a list of problems (empty if fine)."""
    problems = []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        if names != {"collection.anki2", "media"}:
            problems.append(f"unexpected files: {sorted(names)}")
        fd, db = tempfile.mkstemp(suffix=".anki2")
        os.close(fd)
        with open(db, "wb") as f:
            f.write(z.read("collection.anki2"))
    try:
        con = sqlite3.connect(db)
        if con.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            problems.append("sqlite integrity check failed")
        models_s, decks_s = con.execute("SELECT models, decks FROM col").fetchone()
        models, decks = json.loads(models_s), json.loads(decks_s)
        for (mid, flds) in con.execute("SELECT mid, flds FROM notes"):
            m = models.get(str(mid))
            if not m:
                problems.append(f"note uses unknown model {mid}")
            elif len(flds.split("\x1f")) != len(m["flds"]):
                problems.append("note field count doesn't match its model")
        for (did,) in con.execute("SELECT DISTINCT did FROM cards"):
            if str(did) not in decks:
                problems.append(f"card in unknown deck {did}")
        orphans = con.execute("SELECT COUNT(*) FROM cards WHERE nid NOT IN (SELECT id FROM notes)").fetchone()[0]
        if orphans:
            problems.append(f"{orphans} cards without notes")
        dup = con.execute("SELECT COUNT(*) - COUNT(DISTINCT guid) FROM notes").fetchone()[0]
        if dup:
            problems.append(f"{dup} duplicate note GUIDs (two cards with the same question in one section)")
        con.close()
    finally:
        os.remove(db)
    return problems
