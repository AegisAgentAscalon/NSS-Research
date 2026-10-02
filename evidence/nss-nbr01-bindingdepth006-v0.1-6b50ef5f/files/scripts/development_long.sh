#!/usr/bin/env bash
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
for kind in tied_attention fixed_attention4; do
 python -m nbr006.train --kind "$kind" --seed 741 --steps 6000 --out "evidence/development/${kind}_6000.safetensors" --development > "evidence/development/${kind}_6000.log" 2>&1
 python -m nbr006.quick_eval --kind "$kind" --checkpoint "evidence/development/${kind}_6000.safetensors" > "evidence/development/${kind}_6000.eval.log" 2>&1
done
