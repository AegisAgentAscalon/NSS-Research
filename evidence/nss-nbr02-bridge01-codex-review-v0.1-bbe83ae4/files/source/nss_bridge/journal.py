"""SQLite append-only event journal; fake effects and receipts are one local event.
This does not promise exactly-once real external effects or adversarial authentication.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from .util import canonical,digest,strict_json

class Journal:
    def __init__(self,path):
        self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
        self.db=sqlite3.connect(str(path),isolation_level=None)
        self.db.execute('PRAGMA journal_mode=WAL'); self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS events(seq INTEGER PRIMARY KEY, event_id TEXT UNIQUE NOT NULL, payload TEXT NOT NULL, previous TEXT NOT NULL, hash TEXT NOT NULL)')
    def rows(self):
        result=[];prev='0'*64
        for seq,eid,p,previous,h in self.db.execute('SELECT seq,event_id,payload,previous,hash FROM events ORDER BY seq'):
            obj=strict_json(p)
            if seq!=len(result)+1 or previous!=prev or digest({'seq':seq,'event_id':eid,'payload':obj,'previous':prev})!=h:raise ValueError('JOURNAL_INTEGRITY')
            result.append({'seq':seq,'event_id':eid,'payload':obj,'previous':prev,'hash':h});prev=h
        return result
    def existing(self,event_id):
        row=self.db.execute('SELECT payload FROM events WHERE event_id=?',(event_id,)).fetchone()
        return None if row is None else strict_json(row[0])
    def append(self,event_id,payload):
        if not isinstance(event_id,str) or not event_id:raise ValueError('EVENT_ID')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            old=self.existing(event_id)
            if old is not None:
                if canonical(old)!=canonical(payload):raise ValueError('EVENT_ID_COLLISION')
                self.db.execute('COMMIT');return False
            last=self.db.execute('SELECT seq,hash FROM events ORDER BY seq DESC LIMIT 1').fetchone();seq=1 if last is None else last[0]+1;prev='0'*64 if last is None else last[1]
            h=digest({'seq':seq,'event_id':event_id,'payload':payload,'previous':prev})
            self.db.execute('INSERT INTO events VALUES(?,?,?,?,?)',(seq,event_id,canonical(payload).decode(),prev,h));self.db.execute('COMMIT');return True
        except BaseException:
            if self.db.in_transaction:self.db.execute('ROLLBACK')
            raise
    def close(self):self.db.close()
