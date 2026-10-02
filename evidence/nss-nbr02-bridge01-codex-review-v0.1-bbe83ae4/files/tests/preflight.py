from __future__ import annotations
import sys,tempfile,copy,json,threading
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from nss_bridge.bridge import Bridge,key
from nss_bridge.adapters import ScriptedDummy,LocalChatClient
from nss_bridge.util import canonical,digest,atomic_json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
R=Path(__file__).resolve().parents[1]
RESULT=[]
def check(name,fn):
    fn(); RESULT.append({'name':name,'pass':True})
def raises(fn,phrase):
    try:fn()
    except Exception as e:
        assert phrase in str(e),(phrase,str(e));return
    raise AssertionError('DID_NOT_REJECT:'+phrase)
def run():
    with tempfile.TemporaryDirectory() as td:
        b=Bridge(td,'owner',R/'models/parent_4101.npz','shadow');b.create('T');b.create('U')
        def proposal(step=0,**kw):
            p={'owner':'owner','task_id':'T','revision':b.tasks['T']['revision'],'request_id':'r0','action':'perform','step':step};p.update(kw);return canonical(p).decode()
        check('initial_checklist_and_isolated_banks',lambda: (assert_(b.next_step('T')==0),assert_(b.advisor.banks[key('owner','T')]['h'].tolist()==b.advisor.banks[key('owner','U')]['h'].tolist())))
        for name,raw,reason in [
          ('malformed','{','INVALID_JSON'),('duplicate_json_key','{"owner":0,"owner":1}','INVALID_JSON'),
          ('wrong_owner',proposal(owner='else'),'WRONG_OWNER'),('wrong_task',proposal(task_id='U'),'WRONG_TASK'),
          ('extra_permission_field',proposal(approved=True),'PROPOSAL_SCHEMA'),('wrong_next',proposal(step=2),'WRONG_NEXT_STEP'),
          ('premature_finish',proposal(action='finish',step=None),'FALSE_COMPLETION'),
          ('bool_not_integer',proposal(step=True),'STEP'),('out_of_range',proposal(step=9),'STEP'),
          ('wrong_revision_type',proposal(revision=True),'REVISION_TYPE'),('code_action',proposal(action='shell'),'ACTION')]:
            check(name,lambda raw=raw,reason=reason:assert_(b.submit('T',raw)['reason']==reason))
        check('tool_failure_no_effect',lambda:assert_(not b.submit('T',proposal(),tool_fail=True)['effect'] and b.next_step('T')==0))
        before=b.advisor.banks[key('owner','U')]['h'].copy();raw=proposal()
        check('successful_receipt',lambda:assert_(b.submit('T',raw)['effect'] and b.next_step('T')==1))
        check('other_task_state_unchanged',lambda:assert_((before==b.advisor.banks[key('owner','U')]['h']).all()))
        check('duplicate_request_returns_receipt',lambda:assert_(b.submit('T',raw)['reason']=='RECEIPT_REPLAY'))
        check('id_collision_rejected',lambda:assert_(b.submit('T',proposal(step=1))['reason']=='REQUEST_ID_COLLISION'))
        check('already_done_rejected',lambda:assert_(b.submit('T',proposal(request_id='new'))['reason']=='ALREADY_DONE'))
        check('stale_proposal',lambda:assert_(b.submit('T',proposal(step=1,revision=0,request_id='stale'))['reason']=='STALE_REVISION'))
        env=b.snapshot();check('snapshot_same_binding',lambda:b.load_snapshot(copy.deepcopy(env)))
        bad=copy.deepcopy(env);bad['payload']['owner']='else'
        check('snapshot_checksum',lambda:raises(lambda:b.load_snapshot(bad),'SNAPSHOT_CHECKSUM'))
        bad['sha256']=digest(bad['payload'])
        check('snapshot_owner',lambda:raises(lambda:b.load_snapshot(bad),'SNAPSHOT_BINDING'))
        bad=copy.deepcopy(env);bad['payload']['advisor']['model_id']='bad';bad['sha256']=digest(bad['payload'])
        check('snapshot_model',lambda:raises(lambda:b.load_snapshot(bad),'WRONG_MODEL'))
        bad=copy.deepcopy(env);bad['payload']['advisor']['banks']['owner::T']['cursor']+=1;bad['sha256']=digest(bad['payload'])
        check('snapshot_cursor',lambda:raises(lambda:b.load_snapshot(bad),'STATE_CURSOR_GAP'))
        b.event('T','heartbeat',event_id='heart')
        check('stale_snapshot',lambda:raises(lambda:b.load_snapshot(env),'STALE_SNAPSHOT'))
        n=len(b.tasks['T']['events']);b.event('T','heartbeat',event_id='heart')
        check('duplicate_source_event',lambda:assert_(len(b.tasks['T']['events'])==n))
        for step in range(1,7):assert b.submit('T',proposal(step=step,request_id=f'a{step}'))['effect']
        check('publish_requires_approval',lambda:assert_(b.submit('T',proposal(step=7,request_id='p'))['reason']=='APPROVAL_REQUIRED'))
        b.event('T','approve');raw=proposal(step=7,request_id='p')
        check('approval_allows_publish',lambda:assert_(b.submit('T',raw)['effect']))
        check('legitimate_finish',lambda:assert_(b.submit('T',proposal(action='finish',step=None,request_id='fin'))['reason']=='FINISHED'))
        b.event('T','reopen',step=0)
        check('reopening_changes_epoch',lambda:assert_(b.next_step('T')==0 and b.tasks['T']['epochs'][0]==1))
        raw=proposal(request_id='redo');check('crash_after_durable_receipt',lambda:raises(lambda:b.submit('T',raw,crash_after_commit=True),'INJECTED_AFTER'))
        # Closing leaves the durable receipt; fresh instance must not repeat it.
        b.close();b=Bridge(td,'owner',R/'models/parent_4101.npz','shadow')
        check('lost_reply_recovery',lambda:assert_(b.submit('T',raw)['reason']=='RECEIPT_REPLAY' and b.next_step('T')==8))
        check('journal_chain_corruption',lambda:assert_(len(b.journal.rows())>0))
        b.journal.db.execute("UPDATE events SET hash='bad' WHERE seq=1")
        check('corrupt_journal_rejected',lambda:raises(b.journal.rows,'JOURNAL_INTEGRITY'));b.close()
    for url in ['https://example.com','http://192.168.1.2:8000','http://localhost:8000','http://127.0.0.1:8000/other','http://u:p@127.0.0.1:8000']:
        check('reject_endpoint_'+url,lambda u=url:raises(lambda:LocalChatClient(u,'dummy'),'LOOPBACK_ONLY' if '/other' not in u else 'BASE_PATH'))
    seen=[]
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*a):pass
        def do_POST(self):
            seen.append({'path':self.path,'payload':json.loads(self.rfile.read(int(self.headers['Content-Length'])))})
            packet=json.loads(seen[-1]['payload']['messages'][-1]['content'])
            answer=ScriptedDummy().complete(packet)
            out=canonical({'choices':[{'message':{'role':'assistant','content':answer}}]})
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(out)));self.end_headers();self.wfile.write(out)
    with tempfile.TemporaryDirectory() as td:
        b=Bridge(td,'owner');b.create('T');pkt=b.packet('T','http1')
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler);th=threading.Thread(target=server.serve_forever,daemon=True);th.start()
        try:
            client=LocalChatClient(f'http://127.0.0.1:{server.server_port}','dummy');raw=client.complete(pkt)
            check('real_loopback_http_transport',lambda:assert_(raw==ScriptedDummy().complete(pkt) and seen[0]['path']=='/v1/chat/completions'))
            check('HTTP_response_passes_normal_gate',lambda:assert_(b.submit('T',raw)['effect']))
        finally:server.shutdown();server.server_close();th.join();b.close()
    return {'test_groups':len(RESULT),'passed':len(RESULT),'cases':RESULT,'HTTP_test':'real loopback server, scripted reply, NO language inference','optimizer_applications':0}
def assert_(x):
    if not x:raise AssertionError('CHECK_FAILED')
if __name__=='__main__':
    try:
        out=run();atomic_json(R/'results/PREFLIGHT.json',out);print(json.dumps(out,indent=2))
    except BaseException as e:
        import traceback,time
        out={'completed_checks':RESULT,'error':repr(e),'traceback':traceback.format_exc()};atomic_json(R/'failures'/f'preflight_{time.time_ns()}.json',out);raise
