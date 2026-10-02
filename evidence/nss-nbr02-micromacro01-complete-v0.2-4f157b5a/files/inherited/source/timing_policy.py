"""Public receipt timing policy; no scores, generator or hidden trial labels."""
def advance(state, branch, cue, scope, label, receipt, first_change):
    q=dict(state); anchor=q['correction']
    if first_change and anchor is None:
        q['correction']={'cue':cue,'scope':scope,'label':label,'receipt':receipt}
        q['ready']=branch=='E'
    elif anchor is not None and not q['spent'] and branch=='LATE':
        if cue==anchor['cue'] and scope==anchor['scope'] and receipt!=anchor['receipt']:
            if label!=anchor['label']:raise RuntimeError('EXPECTED_FOLLOWUP_CHANGED_AGAIN')
            q['ready']=True
    return q
