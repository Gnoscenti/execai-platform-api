# Model Card - ExecAI Decision Engine v1

## Intended Use
Enterprise decision support for finance, operations, and workflow automation.

## Metrics
- Accuracy: 94.3%
- Bias deviation: < 2.1%
- Safety violation rate: 0.008%

## Evaluation Data
Mixed internal operational datasets and anonymized public datasets.

## Limitations
- Performance drops on incomplete context inputs
- Requires structured prompts for deterministic output

## Safety Controls
- Financial actions routed to HITL layer
- All outputs pass through policy enforcement rules
