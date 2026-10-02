# Development record — before main registration

Three 1,800-step development fits, representation 141 and learning seed 641,
were run once each: split1, split4, coupled17. All outputs and logs are retained.
No main seed was examined for tuning. No architecture, optimizer or training
recipe was changed after those development fits. The inherited development
content model itself lost roughly half its known records under nominal repeated
noise; the protected presence and fixed controls showed the same limitation.
The nearest-prototype control did not. The coupled fit also developed false
presence under noisy continuation. These are preserved failures, not hidden
competent-control claims.

Development revealed an evaluation distinction worth making explicit before
main runs: a false presence signal can be masked by an UNKNOWN content-reader
answer. The final evaluator saves explicit existence estimates and requires both
correct status and correct answers for its every-read metric. A new `read_status`
API distinguishes empty from present-but-unreadable. This is a stricter gate than
a last-answer-only test. Development scores in the retained earlier files use
the initial answer-only scoring; they are not main confirmatory evidence.

Four-coordinate existence is a deliberately redundant code with extra raw
state. Independent-versus-common presence-noise challenges and fixed sign/mean
controls are locked before main results. The learned scalar remains included
regardless of success. No further tuning is planned within the main pass.
