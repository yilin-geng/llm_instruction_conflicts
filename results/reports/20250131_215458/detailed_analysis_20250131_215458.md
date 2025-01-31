# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250131_215458 | marked_user_detailed | 88.89% | 11.11% |
| llama3_20250131_215458 | unmarked_user_detailed | 100.00% | 0.00% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250131_215458 | marked_user_detailed | 61.11% | 27.78% | 0.00% | 11.11% | 88.89% | 11.11% |
| llama3_20250131_215458 | unmarked_user_detailed | 94.44% | 5.56% | 0.00% | 0.00% | 100.00% | 0.00% |

## Statistics by Conflict Type


### llama3_20250131_215458 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 33.33% | 66.67% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 66.67% | 33.33% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 0.00% | 33.33% | 0.00% | 66.67% | 66.67% |
| word_length_conflict: 300_50 | 66.67% | 33.33% | 0.00% | 0.00% | 0.00% |

### llama3_20250131_215458 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 66.67% | 33.33% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| word_length_conflict: 300_50 | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
