"""Approved synthetic corpus through public archive/snapshot consumption boundaries."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from .dataset_store import DatasetSnapshots
from .experience_store import ExperienceArchive
from .neural_contracts import CODEC, encoded, fingerprint, pairs, read_document, validate_pairs
from .runtime import fail
from .serialization import decode

AT='2026-09-10T18:00:00Z'
ACTOR={'id':'neural-probe-scripted-operator','kind':'HUMAN','version':'fixture-v1'}


def unwrap(result):
    if result['status']!='SUCCESS':fail(result['status'],result['detail'])
    return result['data']


class ProbeData:
    """Not a second archive. Reopens the existing owners using a fixed manifest."""
    def __init__(self,directory):
        self.root=Path(directory);self.binding=read_document(self.root/'binding.json')
        self.archive=ExperienceArchive(self.root/'experience')
        self.snapshots=DatasetSnapshots(self.root/'snapshots')
        self.tokenizer=self.root/'codec.json'
        self._identity=fingerprint(self.binding)

    @classmethod
    def create(cls,directory):
        root=Path(directory)
        if root.exists() and any(root.iterdir()):fail('CONSTRAINT_CONFLICT','Dataset setup needs an empty directory')
        root.mkdir(parents=True,exist_ok=True)
        archive=ExperienceArchive.create(root/'experience')
        snapshots=DatasetSnapshots.create(root/'snapshots',archive=archive)
        token=root/'codec.json';token.write_bytes(encoded(CODEC));members=[];sources={}
        for split in ('train','validation'):
            id='neural-'+split;content=encoded({'codec':CODEC['id'],'pairs':pairs(split)}).decode()
            h=sha256(content.encode()).hexdigest();sources[split]=h
            capture={'schema_version':1,'operation_id':'capture:'+id,'experience_id':id,
                'actor':ACTOR,'at':AT,
                'observation':{'kind':'EXTERNAL_RECORD','execution':None,
                    'summary':'Deterministically enumerated synthetic symbol pairs; not private conversation.',
                    'outcome':'UNKNOWN','check_refs':[]},
                'family_id':'neural-split-'+split,'sensitivity':'ORDINARY',
                'evidence':[{'id':'pairs','kind':'REFERENCE','author':ACTOR,'recorded_at':AT,
                    'media_type':'application/json','sha256':h,'content':content,'generator':None,
                    'parent_source_ids':[],'rights_note':'Scripted development fixture, no authenticated rights determination.'}],
                'statement':{'text':content,'uncertainty':'LOW','support_ids':['pairs']}}
            unwrap(archive.capture(capture))
            for action,payload in [('REVIEW',{'decision':'APPROVED'}),
                ('PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fixture:neural-development'})]:
                ref=unwrap(archive.inspect(id))['reference']
                unwrap(archive.change({'schema_version':1,'experience_id':id,'operation_id':id+':'+action,
                    'expected_revision_hash':ref['sha256'],'actor':ACTOR,'at':AT,
                    'reason':'Scripted HUMAN attestation on synthetic development records only.',
                    'action':action,'payload':payload}))
            members.append({**unwrap(archive.inspect(id))['reference'],'split':split})
        receipt=unwrap(snapshots.build({'schema_version':1,'operation_id':'neural:build','snapshot_id':'neural-pairs-v1',
            'actor':ACTOR,'at':AT,'reason':'Exact synthetic pairs; train and validation remain separate.',
            'purpose':'training','transform':'curated_text_v1',
            'tokenizer':{'id':CODEC['id'],'version':'1','sha256':sha256(token.read_bytes()).hexdigest()},
            'members':members},archive=archive,tokenizer_path=token))
        test={'codec':CODEC['id'],'pairs':pairs('test'),'purpose':'DEVELOPER_VISIBLE_SYNTHETIC_HELDOUT_PAIRS'}
        (root/'test.json').write_bytes(encoded(test))
        binding={'snapshot_id':receipt['snapshot_id'],'snapshot_sha256':receipt['sha256'],
                 'codec_sha256':fingerprint(CODEC),'test_sha256':fingerprint(test),'source_hashes':sources}
        (root/'binding.json').write_bytes(encoded(binding))
        return cls(root)

    def read(self,split):
        if fingerprint(read_document(self.root/'binding.json'))!=self._identity:
            fail('CONSTRAINT_CONFLICT','Dataset binding changed after opening')
        if split=='test':
            obj=read_document(self.root/'test.json')
            if fingerprint(obj)!=self.binding['test_sha256'] or obj['codec']!=CODEC['id']:
                fail('VALIDATION_FAILED','Heldout fixture changed')
            return validate_pairs(obj['pairs'],'test')
        result=unwrap(self.snapshots.read_for_use(self.binding['snapshot_id'],
            expected_manifest_hash=self.binding['snapshot_sha256'],purpose='training',split=split,
            archive=self.archive,tokenizer_path=self.tokenizer))
        if len(result['examples'])!=1:fail('VALIDATION_FAILED','Expected one fixed corpus record per split')
        obj=decode(result['examples'][0]['text'])
        if set(obj)!= {'codec','pairs'} or obj['codec']!=CODEC['id']:
            fail('VALIDATION_FAILED','Wrong symbol codec')
        return validate_pairs(obj['pairs'],split)

    def gate(self):
        """Point-in-time checks, not a lease or retraction of already used bytes."""
        self.read('train');self.read('validation');self.read('test')
        return deepcopy(self.binding)

    def revoke_for_test(self):
        return unwrap(self.archive.revoke_source({'schema_version':1,'operation_id':'neural:withdraw',
            'actor':ACTOR,'at':AT,'reason':'Scripted test of use restrictions after training.',
            'permission_ref':'fixture:neural-withdrawal','source_sha256':self.binding['source_hashes']['train'],
            'purpose':'training'}))
