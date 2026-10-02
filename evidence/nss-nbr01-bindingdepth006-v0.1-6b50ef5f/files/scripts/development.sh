#!/usr/bin/env bash
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for kind in gated_hop tied_attention fixed_attention4 flat_gru binder; do
 python -m nbr006.train --kind "$kind" --seed 741 --steps 1200 --out "evidence/development/$kind.safetensors" --development > "evidence/development/$kind.log" 2>&1
 if [ "$kind" != binder ]; then python -m nbr006.quick_eval --kind "$kind" --checkpoint "evidence/development/$kind.safetensors" > "evidence/development/$kind.eval.log" 2>&1; fi
done
