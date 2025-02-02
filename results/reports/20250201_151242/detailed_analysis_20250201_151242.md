# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250201_151242 | baseline_all_user | 36.33% | 63.67% |
| llama3_20250201_151242 | basic_separation | 20.33% | 79.67% |
| llama3_20250201_151242 | emphasized_separation | 24.00% | 76.00% |
| llama3_20250201_151242 | marked_system_basic | 80.83% | 19.17% |
| llama3_20250201_151242 | marked_system_detailed | 84.33% | 15.67% |
| llama3_20250201_151242 | marked_user_basic | 82.50% | 17.50% |
| llama3_20250201_151242 | marked_user_detailed | 90.00% | 10.00% |
| llama3_20250201_151242 | task_specified_separation | 20.50% | 79.50% |
| llama3_20250201_151242 | unmarked_system_basic | 40.00% | 60.00% |
| llama3_20250201_151242 | unmarked_system_detailed | 40.00% | 60.00% |
| llama3_20250201_151242 | unmarked_user_basic | 36.67% | 63.33% |
| llama3_20250201_151242 | unmarked_user_detailed | 48.50% | 51.50% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250201_151242 | baseline_all_user | 36.00% | 0.33% | 56.50% | 7.17% | 36.33% | 63.67% |
| llama3_20250201_151242 | basic_separation | 20.33% | 0.00% | 76.83% | 2.83% | 20.33% | 79.67% |
| llama3_20250201_151242 | emphasized_separation | 23.83% | 0.17% | 72.50% | 3.50% | 24.00% | 76.00% |
| llama3_20250201_151242 | marked_system_basic | 24.50% | 56.33% | 17.67% | 1.50% | 80.83% | 19.17% |
| llama3_20250201_151242 | marked_system_detailed | 65.33% | 19.00% | 15.00% | 0.67% | 84.33% | 15.67% |
| llama3_20250201_151242 | marked_user_basic | 11.83% | 70.67% | 16.17% | 1.33% | 82.50% | 17.50% |
| llama3_20250201_151242 | marked_user_detailed | 75.33% | 14.67% | 9.33% | 0.67% | 90.00% | 10.00% |
| llama3_20250201_151242 | task_specified_separation | 20.50% | 0.00% | 74.83% | 4.67% | 20.50% | 79.50% |
| llama3_20250201_151242 | unmarked_system_basic | 24.00% | 16.00% | 55.17% | 4.83% | 40.00% | 60.00% |
| llama3_20250201_151242 | unmarked_system_detailed | 39.83% | 0.17% | 57.00% | 3.00% | 40.00% | 60.00% |
| llama3_20250201_151242 | unmarked_user_basic | 25.50% | 11.17% | 54.17% | 9.17% | 36.67% | 63.33% |
| llama3_20250201_151242 | unmarked_user_detailed | 46.00% | 2.50% | 49.33% | 2.17% | 48.50% | 51.50% |

## Statistics by Conflict Type


### llama3_20250201_151242 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 7.00% | 0.00% | 92.00% | 1.00% | 93.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 55.00% | 2.00% | 34.00% | 9.00% | 43.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 47.00% | 0.00% | 20.00% | 33.00% | 53.00% |
| word_length_conflict: 300_50 | 1.00% | 0.00% | 99.00% | 0.00% | 99.00% |

### llama3_20250201_151242 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| language_conflict: en_fr | 97.00% | 0.00% | 3.00% | 0.00% | 3.00% |
| num_sentence_conflict: 10_5 | 3.00% | 0.00% | 80.00% | 17.00% | 97.00% |
| word_length_conflict: 300_50 | 2.00% | 0.00% | 98.00% | 0.00% | 98.00% |

### llama3_20250201_151242 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 20.00% | 0.00% | 80.00% | 0.00% | 80.00% |
| keyword_forbidden_conflict: awesome_need | 3.00% | 0.00% | 97.00% | 0.00% | 97.00% |
| keyword_frequency_conflict: like_5_2 | 3.00% | 0.00% | 97.00% | 0.00% | 97.00% |
| language_conflict: en_fr | 99.00% | 0.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 7.00% | 0.00% | 72.00% | 21.00% | 93.00% |
| word_length_conflict: 300_50 | 11.00% | 1.00% | 88.00% | 0.00% | 88.00% |

### llama3_20250201_151242 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 32.00% | 47.00% | 16.00% | 5.00% | 21.00% |
| keyword_forbidden_conflict: awesome_need | 10.00% | 0.00% | 90.00% | 0.00% | 90.00% |
| keyword_frequency_conflict: like_5_2 | 18.00% | 82.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 28.00% | 72.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 15.00% | 85.00% | 0.00% | 0.00% | 0.00% |
| word_length_conflict: 300_50 | 44.00% | 52.00% | 0.00% | 4.00% | 4.00% |

### llama3_20250201_151242 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 79.00% | 2.00% | 16.00% | 3.00% | 19.00% |
| keyword_forbidden_conflict: awesome_need | 28.00% | 0.00% | 72.00% | 0.00% | 72.00% |
| keyword_frequency_conflict: like_5_2 | 72.00% | 28.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 77.00% | 23.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 60.00% | 38.00% | 2.00% | 0.00% | 2.00% |
| word_length_conflict: 300_50 | 76.00% | 23.00% | 0.00% | 1.00% | 1.00% |

### llama3_20250201_151242 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 5.00% | 89.00% | 2.00% | 4.00% | 6.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 11.00% | 89.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 15.00% | 85.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 10.00% | 89.00% | 0.00% | 1.00% | 1.00% |
| word_length_conflict: 300_50 | 25.00% | 72.00% | 0.00% | 3.00% | 3.00% |

### llama3_20250201_151242 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 74.00% | 15.00% | 9.00% | 2.00% | 11.00% |
| keyword_forbidden_conflict: awesome_need | 53.00% | 0.00% | 47.00% | 0.00% | 47.00% |
| keyword_frequency_conflict: like_5_2 | 81.00% | 19.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 79.00% | 21.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 78.00% | 22.00% | 0.00% | 0.00% | 0.00% |
| word_length_conflict: 300_50 | 87.00% | 11.00% | 0.00% | 2.00% | 2.00% |

### llama3_20250201_151242 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| language_conflict: en_fr | 99.00% | 0.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 4.00% | 0.00% | 68.00% | 28.00% | 96.00% |
| word_length_conflict: 300_50 | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |

### llama3_20250201_151242 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 16.00% | 0.00% | 84.00% | 0.00% | 84.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 58.00% | 31.00% | 4.00% | 35.00% |
| language_conflict: en_fr | 62.00% | 38.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 50.00% | 0.00% | 25.00% | 25.00% | 50.00% |
| word_length_conflict: 300_50 | 3.00% | 0.00% | 97.00% | 0.00% | 97.00% |

### llama3_20250201_151242 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_frequency_conflict: like_5_2 | 63.00% | 1.00% | 33.00% | 3.00% | 36.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 56.00% | 0.00% | 29.00% | 15.00% | 44.00% |
| word_length_conflict: 300_50 | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |

### llama3_20250201_151242 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 44.00% | 0.00% | 56.00% | 0.00% | 56.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 14.00% | 34.00% | 46.00% | 6.00% | 52.00% |
| language_conflict: en_fr | 68.00% | 32.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 21.00% | 1.00% | 29.00% | 49.00% | 78.00% |
| word_length_conflict: 300_50 | 2.00% | 0.00% | 98.00% | 0.00% | 98.00% |

### llama3_20250201_151242 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 21.00% | 0.00% | 79.00% | 0.00% | 79.00% |
| keyword_forbidden_conflict: awesome_need | 17.00% | 0.00% | 83.00% | 0.00% | 83.00% |
| keyword_frequency_conflict: like_5_2 | 70.00% | 15.00% | 14.00% | 1.00% | 15.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 67.00% | 0.00% | 21.00% | 12.00% | 33.00% |
| word_length_conflict: 300_50 | 1.00% | 0.00% | 99.00% | 0.00% | 99.00% |
