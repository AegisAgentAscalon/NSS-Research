# NSS BRIDGE01 v0.1

Dummy prototype, not a conversational model or deployment.

Run offline: `python run_demo.py --out demo_output` from this directory (NumPy required). Use a new directory. The bundled four checkpoint exports are tiny learned checklist models. No model download, training, real upload or shell tool is performed.

Read `docs/ARCHITECTURE_AND_REPORT.md` first. All records and responses are under `results/main/cases`; independent checks under `audit`. `tests/preflight.py` exercises local software and one loopback fake server, not a real LLM. Run reproduction on a COPY to preserve this evidence package.

Primary result:216/216 scripted sessions satisfy the exact action contract;4144/4144 retained neural event suggestions match the rule. The exact coordinator also succeeds. Rejected proposals are retained; dummy replies are never counted as generated natural language.

Next research: low-bit inference and training ONLY. Other lines remain on hold by owner direction.

## Execution platform

The supplied runner and audit were tested on Linux and use Python’s Unix `resource` module for process measurements. On Windows, use WSL/Linux for this version; native Windows execution has not been validated. The NumPy exports avoid Torch for the demo. Running a real local language server is a separate, untested integration; do not treat the loopback stub as a model-quality test.
