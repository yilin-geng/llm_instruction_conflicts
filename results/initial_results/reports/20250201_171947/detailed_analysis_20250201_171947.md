# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250201_171947 | baseline_all_user | 36.33% | 63.67% |
| llama3_20250201_171947 | basic_separation | 20.33% | 79.67% |
| llama3_20250201_171947 | emphasized_separation | 23.33% | 76.67% |
| llama3_20250201_171947 | marked_system_basic | 73.83% | 26.17% |
| llama3_20250201_171947 | marked_system_detailed | 75.50% | 24.50% |
| llama3_20250201_171947 | marked_user_basic | 79.33% | 20.67% |
| llama3_20250201_171947 | marked_user_detailed | 79.00% | 21.00% |
| llama3_20250201_171947 | task_specified_separation | 20.50% | 79.50% |
| llama3_20250201_171947 | unmarked_system_basic | 39.00% | 61.00% |
| llama3_20250201_171947 | unmarked_system_detailed | 42.83% | 57.17% |
| llama3_20250201_171947 | unmarked_user_basic | 40.17% | 59.83% |
| llama3_20250201_171947 | unmarked_user_detailed | 41.83% | 58.17% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250201_171947 | baseline_all_user | 36.00% | 0.33% | 56.50% | 7.17% | 36.33% | 63.67% |
| llama3_20250201_171947 | basic_separation | 20.33% | 0.00% | 76.83% | 2.83% | 20.33% | 79.67% |
| llama3_20250201_171947 | emphasized_separation | 23.00% | 0.33% | 65.17% | 11.50% | 23.33% | 76.67% |
| llama3_20250201_171947 | marked_system_basic | 29.50% | 44.33% | 21.83% | 4.33% | 73.83% | 26.17% |
| llama3_20250201_171947 | marked_system_detailed | 44.00% | 31.50% | 19.00% | 5.50% | 75.50% | 24.50% |
| llama3_20250201_171947 | marked_user_basic | 20.00% | 59.33% | 17.33% | 3.33% | 79.33% | 20.67% |
| llama3_20250201_171947 | marked_user_detailed | 48.50% | 30.50% | 18.00% | 3.00% | 79.00% | 21.00% |
| llama3_20250201_171947 | task_specified_separation | 20.50% | 0.00% | 74.83% | 4.67% | 20.50% | 79.50% |
| llama3_20250201_171947 | unmarked_system_basic | 27.33% | 11.67% | 47.17% | 13.83% | 39.00% | 61.00% |
| llama3_20250201_171947 | unmarked_system_detailed | 30.00% | 12.83% | 43.00% | 14.17% | 42.83% | 57.17% |
| llama3_20250201_171947 | unmarked_user_basic | 25.67% | 14.50% | 46.67% | 13.17% | 40.17% | 59.83% |
| llama3_20250201_171947 | unmarked_user_detailed | 33.33% | 8.50% | 45.17% | 13.00% | 41.83% | 58.17% |

## Statistics by Conflict Type


### llama3_20250201_171947 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 7.00% | 0.00% | 92.00% | 1.00% | 93.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 55.00% | 2.00% | 34.00% | 9.00% | 43.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 47.00% | 0.00% | 20.00% | 33.00% | 53.00% |
| word_length_conflict: 300_50 | 1.00% | 0.00% | 99.00% | 0.00% | 99.00% |

### llama3_20250201_171947 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| language_conflict: en_fr | 97.00% | 0.00% | 3.00% | 0.00% | 3.00% |
| num_sentence_conflict: 10_5 | 3.00% | 0.00% | 80.00% | 17.00% | 97.00% |
| word_length_conflict: 300_50 | 2.00% | 0.00% | 98.00% | 0.00% | 98.00% |

### llama3_20250201_171947 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 21.00% | 0.00% | 77.00% | 2.00% | 79.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 0.00% | 85.00% | 8.00% | 93.00% |
| language_conflict: en_fr | 97.00% | 2.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 3.00% | 0.00% | 38.00% | 59.00% | 97.00% |
| word_length_conflict: 300_50 | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |

### llama3_20250201_171947 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 66.00% | 24.00% | 6.00% | 4.00% | 10.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 22.00% | 38.00% | 22.00% | 18.00% | 40.00% |
| language_conflict: en_fr | 10.00% | 90.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 23.00% | 67.00% | 7.00% | 3.00% | 10.00% |
| word_length_conflict: 300_50 | 51.00% | 47.00% | 1.00% | 1.00% | 2.00% |

### llama3_20250201_171947 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 92.00% | 0.00% | 5.00% | 3.00% | 8.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 38.00% | 28.00% | 12.00% | 22.00% | 34.00% |
| language_conflict: en_fr | 43.00% | 57.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 40.00% | 47.00% | 5.00% | 8.00% | 13.00% |
| word_length_conflict: 300_50 | 42.00% | 57.00% | 1.00% | 0.00% | 1.00% |

### llama3_20250201_171947 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 32.00% | 63.00% | 1.00% | 4.00% | 5.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 11.00% | 66.00% | 7.00% | 16.00% | 23.00% |
| language_conflict: en_fr | 7.00% | 93.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 19.00% | 79.00% | 2.00% | 0.00% | 2.00% |
| word_length_conflict: 300_50 | 45.00% | 55.00% | 0.00% | 0.00% | 0.00% |

### llama3_20250201_171947 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 93.00% | 2.00% | 4.00% | 1.00% | 5.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_frequency_conflict: like_5_2 | 31.00% | 45.00% | 9.00% | 15.00% | 24.00% |
| language_conflict: en_fr | 51.00% | 49.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 50.00% | 45.00% | 3.00% | 2.00% | 5.00% |
| word_length_conflict: 300_50 | 58.00% | 42.00% | 0.00% | 0.00% | 0.00% |

### llama3_20250201_171947 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| language_conflict: en_fr | 99.00% | 0.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 4.00% | 0.00% | 68.00% | 28.00% | 96.00% |
| word_length_conflict: 300_50 | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |

### llama3_20250201_171947 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 79.00% | 1.00% | 19.00% | 1.00% | 20.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 8.00% | 3.00% | 64.00% | 25.00% | 89.00% |
| language_conflict: en_fr | 63.00% | 37.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 14.00% | 26.00% | 52.00% | 78.00% |
| word_length_conflict: 300_50 | 2.00% | 15.00% | 78.00% | 5.00% | 83.00% |

### llama3_20250201_171947 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 85.00% | 1.00% | 14.00% | 0.00% | 14.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 7.00% | 59.00% | 27.00% | 86.00% |
| language_conflict: en_fr | 69.00% | 31.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 13.00% | 28.00% | 51.00% | 79.00% |
| word_length_conflict: 300_50 | 6.00% | 25.00% | 62.00% | 7.00% | 69.00% |

### llama3_20250201_171947 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 88.00% | 0.00% | 12.00% | 0.00% | 12.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 4.00% | 64.00% | 26.00% | 90.00% |
| language_conflict: en_fr | 41.00% | 59.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 11.00% | 29.00% | 52.00% | 81.00% |
| word_length_conflict: 300_50 | 2.00% | 13.00% | 84.00% | 1.00% | 85.00% |

### llama3_20250201_171947 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 88.00% | 0.00% | 12.00% | 0.00% | 12.00% |
| keyword_forbidden_conflict: awesome_need | 7.00% | 0.00% | 93.00% | 0.00% | 93.00% |
| keyword_frequency_conflict: like_5_2 | 9.00% | 3.00% | 63.00% | 25.00% | 88.00% |
| language_conflict: en_fr | 77.00% | 23.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 16.00% | 9.00% | 30.00% | 45.00% | 75.00% |
| word_length_conflict: 300_50 | 3.00% | 16.00% | 73.00% | 8.00% | 81.00% |
