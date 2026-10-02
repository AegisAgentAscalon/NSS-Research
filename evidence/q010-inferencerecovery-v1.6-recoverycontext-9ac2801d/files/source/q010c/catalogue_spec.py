"""Serialize the existing generator identity; not an alternative case generator."""
def case_spec(c):
    r=c.rng_record;gc=r['graph_pair_condition_id'];ge=r['graph_pair_episode_id']
    base=dict(protocol_version='Q010R-CM1',split=c.split,paired_seed=c.paired_seed,condition_id=gc,episode_id=ge,stage_index=None)
    close=None
    if 'close_transform_seed_u64' in r:
        role=r['close_transform_role']
        ctx=dict(protocol_version='Q010R-CM1',split='stress',purpose='close_identity',paired_seed=c.paired_seed,
                 condition_id=f'stress_close_{role}_sigma001',episode_id=f'{c.pair_id}-close-{role}',stage_index=None)
        close=dict(algorithm=r['close_transform_algorithm'],role=role,sigma=r['close_transform_sigma'],
                   target_id=r['close_transform_target_id'],decoy_id=r['close_transform_decoy_id'],seed_context=ctx,rng_seed_u64=r['close_transform_seed_u64'])
    return dict(schema_version=1,generator_id='q010r.data.make_case.v1',case_id=c.case_id,pair_id=c.pair_id,
        split=c.split,arm=c.arm,phase=c.phase,path_length=c.path_length,allowed_depth=c.allowed_depth,
        missing=c.missing,missing_at=c.missing_at,near_treatment=bool(r.get('near_draw',False)),paired_seed=c.paired_seed,
        graph_seed=r['graph_seed'],treatment_seed=r['treatment_seed'],condition_id=r['condition_id'],episode_id=r['episode_id'],
        graph_pair_condition_id=gc,graph_pair_episode_id=ge,graph_seed_context=dict(base,purpose='graph_generation'),
        treatment_seed_context=dict(base,purpose='graph_treatment'),close_identity_transform=close)
