# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250131_183740 | marked_user_detailed | 85.71% | 14.29% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250131_183740 | marked_user_detailed | 28.57% | 57.14% | 14.29% | 0.00% | 85.71% | 14.29% |

## Statistics by Conflict Type


### llama3_20250131_183740 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Both | Failure Rate |
|---------------|------------|---------|-----------|------|------|-------------|
| keyword_forbidden_conflict | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 0.00% | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| word_length_conflict: 300_50 | 25.00% | 50.00% | 25.00% | 0.00% | 0.00% | 25.00% |
