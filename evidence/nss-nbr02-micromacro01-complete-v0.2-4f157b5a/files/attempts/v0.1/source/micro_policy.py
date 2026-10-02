"""Public receipt-count schedule; no scores or hidden trial labels."""
def advance(state,branch,cue,scope,label,receipt,changed):
    s={**state};anchor=s['correction']
    if anchor is None:
        if not changed:return s
        s['correction']={'cue':cue,'scope':scope,'label':label,'receipt':receipt};s['since']=0
    else:
        if receipt==anchor['receipt']:raise RuntimeError('DUPLICATE_CHANGED_RECEIPT')
        if cue==anchor['cue'] and scope==anchor['scope'] and label!=anchor['label']:raise RuntimeError('SECOND_REVERSAL_OUT_OF_SCOPE')
        if s['ready']>0:raise RuntimeError('DUE_MAINTENANCE_NOT_SPENT')
        s['since']+=1
    if branch in ('D','F4') and s['since'] in (0,1,2,3):s['ready']=1
    elif branch=='B4' and s['since']==3:s['ready']=4
    else:s['ready']=0
    return s
