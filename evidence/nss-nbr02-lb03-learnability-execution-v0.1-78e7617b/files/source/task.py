"""Exact source task/stream functions; numerical task inputs, no hidden labels to learner."""
import numpy as np

def oracle(tokens):
    """Canonical labels: bitmask implementation, no neural predictions involved."""
    a=np.asarray(tokens); out=np.empty(a.shape,dtype=np.uint8); masks=np.empty_like(out)
    flat=a.reshape(-1,a.shape[-1]); oo=out.reshape(flat.shape); mm=masks.reshape(flat.shape)
    for b,row in enumerate(flat):
        m=0
        for t,e in enumerate(row):
            e=int(e)
            if e<8: m |= 1<<e
            elif e<16: m &= ~(1<<(e-8))
            elif e==16: m=0
            elif e!=17: raise ValueError('Not an A token')
            oo[b,t]=next((i for i in range(8) if not m & (1<<i)),8)
            mm[b,t]=m
    return out,masks

def independent_oracle(tokens):
    """Independent label implementation: Python set of completed identifiers."""
    result=[]
    for row in np.asarray(tokens):
        done=set(); labels=[]
        for token in row:
            n=int(token)
            if 0<=n<=7: done.add(n)
            elif 8<=n<=15: done.discard(n-8)
            elif n==16: done.clear()
            elif n!=17: raise ValueError(n)
            labels.append(min(set(range(8))-done) if len(done)<8 else 8)
        result.append(labels)
    return np.asarray(result,dtype=np.uint8)

def stream(rng, length, family):
    """TARGET_MASK_ROUNDS_V1. Target masks guide data generation only.
    All intermediate events are exposed; target masks/labels never enter inputs.
    """
    events=[]; mask=0; round_n=0
    def emit(e):
        nonlocal mask
        if len(events)>=length: return
        events.append(int(e))
        if e<8: mask |= 1<<e
        elif e<16: mask &= ~(1<<(e-8))
        elif e==16: mask=0
    while len(events)<length:
        if family==3 and round_n%3==0: emit(16)
        # Ordinary and repeat families sample all next-action labels uniformly.
        # Revision family alternates complete and partially reopened targets.
        k=8 if family==2 and round_n%2==0 else int(rng.integers(0,8 if family==2 else 9))
        target=(1<<k)-1
        for j in range(k+1,8):
            if rng.random()<0.5: target |= 1<<j
        edits=[j if target & (1<<j) else j+8 for j in range(8) if bool(mask&(1<<j))!=bool(target&(1<<j))]
        rng.shuffle(edits)
        for e in edits: emit(e)
        # Holds mix actual NOOP and genuinely idempotent SET/CLEAR commands.
        dwell=int(rng.integers(5,10) if family==1 else rng.integers(1,5))
        for _ in range(dwell):
            if rng.random()<0.5: emit(17)
            else:
                j=int(rng.integers(0,8)); emit(j if mask & (1<<j) else j+8)
        round_n+=1
    return np.asarray(events,dtype=np.uint8)
