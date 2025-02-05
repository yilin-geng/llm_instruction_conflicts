# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250202_042122 | baseline_all_user | 61.83% | 38.17% |
| llama3_20250202_042122 | basic_separation | 37.00% | 63.00% |
| llama3_20250202_042122 | emphasized_separation | 47.00% | 53.00% |
| llama3_20250202_042122 | marked_system_basic | 90.83% | 9.17% |
| llama3_20250202_042122 | marked_system_detailed | 82.33% | 17.67% |
| llama3_20250202_042122 | marked_user_basic | 90.17% | 9.83% |
| llama3_20250202_042122 | marked_user_detailed | 82.00% | 18.00% |
| llama3_20250202_042122 | task_specified_separation | 30.67% | 69.33% |
| llama3_20250202_042122 | unmarked_system_basic | 61.33% | 38.67% |
| llama3_20250202_042122 | unmarked_system_detailed | 62.00% | 38.00% |
| llama3_20250202_042122 | unmarked_user_basic | 64.33% | 35.67% |
| llama3_20250202_042122 | unmarked_user_detailed | 65.83% | 34.17% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250202_042122 | baseline_all_user | 43.67% | 18.17% | 37.17% | 1.00% | 61.83% | 38.17% |
| llama3_20250202_042122 | basic_separation | 22.17% | 14.83% | 62.00% | 1.00% | 37.00% | 63.00% |
| llama3_20250202_042122 | emphasized_separation | 31.33% | 15.67% | 52.00% | 1.00% | 47.00% | 53.00% |
| llama3_20250202_042122 | marked_system_basic | 32.50% | 58.33% | 4.00% | 5.17% | 90.83% | 9.17% |
| llama3_20250202_042122 | marked_system_detailed | 65.83% | 16.50% | 15.17% | 2.50% | 82.33% | 17.67% |
| llama3_20250202_042122 | marked_user_basic | 16.33% | 73.83% | 3.00% | 6.83% | 90.17% | 9.83% |
| llama3_20250202_042122 | marked_user_detailed | 62.00% | 20.00% | 12.50% | 5.50% | 82.00% | 18.00% |
| llama3_20250202_042122 | task_specified_separation | 14.67% | 16.00% | 69.33% | 0.00% | 30.67% | 69.33% |
| llama3_20250202_042122 | unmarked_system_basic | 44.33% | 17.00% | 37.17% | 1.50% | 61.33% | 38.67% |
| llama3_20250202_042122 | unmarked_system_detailed | 44.67% | 17.33% | 37.00% | 1.00% | 62.00% | 38.00% |
| llama3_20250202_042122 | unmarked_user_basic | 42.83% | 21.50% | 34.00% | 1.67% | 64.33% | 35.67% |
| llama3_20250202_042122 | unmarked_user_detailed | 51.00% | 14.83% | 33.17% | 1.00% | 65.83% | 34.17% |

## Statistics by Conflict Type


### llama3_20250202_042122 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 96.00% | 3.00% | 1.00% | 0.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 19.00% | 81.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 26.00% | 3.00% | 69.00% | 2.00% | 71.00% |
| language_conflict: en_fr | 81.00% | 17.00% | 2.00% | 0.00% | 2.00% |
| num_sentence_conflict: 10_5 | 12.00% | 5.00% | 79.00% | 4.00% | 83.00% |
| word_length_conflict: 300_50 | 28.00% | 0.00% | 72.00% | 0.00% | 72.00% |

### llama3_20250202_042122 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 54.00% | 0.00% | 40.00% | 6.00% | 46.00% |
| keyword_forbidden_conflict: awesome_need | 14.00% | 86.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 9.00% | 1.00% | 90.00% | 0.00% | 90.00% |
| language_conflict: en_fr | 36.00% | 2.00% | 62.00% | 0.00% | 62.00% |
| num_sentence_conflict: 10_5 | 14.00% | 0.00% | 86.00% | 0.00% | 86.00% |
| word_length_conflict: 300_50 | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |

### llama3_20250202_042122 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 77.00% | 0.00% | 21.00% | 2.00% | 23.00% |
| keyword_forbidden_conflict: awesome_need | 13.00% | 87.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 12.00% | 0.00% | 85.00% | 3.00% | 88.00% |
| language_conflict: en_fr | 61.00% | 7.00% | 32.00% | 0.00% | 32.00% |
| num_sentence_conflict: 10_5 | 10.00% | 0.00% | 89.00% | 1.00% | 90.00% |
| word_length_conflict: 300_50 | 15.00% | 0.00% | 85.00% | 0.00% | 85.00% |

### llama3_20250202_042122 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 45.00% | 55.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 28.00% | 72.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 33.00% | 62.00% | 0.00% | 5.00% | 5.00% |
| language_conflict: en_fr | 32.00% | 68.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 37.00% | 26.00% | 12.00% | 25.00% | 37.00% |
| word_length_conflict: 300_50 | 20.00% | 67.00% | 12.00% | 1.00% | 13.00% |

### llama3_20250202_042122 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 78.00% | 22.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 56.00% | 44.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 71.00% | 19.00% | 2.00% | 8.00% | 10.00% |
| language_conflict: en_fr | 100.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 67.00% | 9.00% | 19.00% | 5.00% | 24.00% |
| word_length_conflict: 300_50 | 23.00% | 5.00% | 70.00% | 2.00% | 72.00% |

### llama3_20250202_042122 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 26.00% | 74.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 13.00% | 87.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 13.00% | 82.00% | 0.00% | 5.00% | 5.00% |
| language_conflict: en_fr | 17.00% | 83.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 18.00% | 39.00% | 8.00% | 35.00% | 43.00% |
| word_length_conflict: 300_50 | 11.00% | 78.00% | 10.00% | 1.00% | 11.00% |

### llama3_20250202_042122 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 67.00% | 33.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 63.00% | 37.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 64.00% | 22.00% | 1.00% | 13.00% | 14.00% |
| language_conflict: en_fr | 98.00% | 2.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 54.00% | 17.00% | 10.00% | 19.00% | 29.00% |
| word_length_conflict: 300_50 | 26.00% | 9.00% | 64.00% | 1.00% | 65.00% |

### llama3_20250202_042122 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 34.00% | 0.00% | 66.00% | 0.00% | 66.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 95.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 13.00% | 0.00% | 87.00% | 0.00% | 87.00% |
| language_conflict: en_fr | 17.00% | 1.00% | 82.00% | 0.00% | 82.00% |
| num_sentence_conflict: 10_5 | 10.00% | 0.00% | 90.00% | 0.00% | 90.00% |
| word_length_conflict: 300_50 | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |

### llama3_20250202_042122 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 95.00% | 4.00% | 1.00% | 0.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 23.00% | 77.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 20.00% | 0.00% | 75.00% | 5.00% | 80.00% |
| language_conflict: en_fr | 84.00% | 11.00% | 5.00% | 0.00% | 5.00% |
| num_sentence_conflict: 10_5 | 14.00% | 6.00% | 78.00% | 2.00% | 80.00% |
| word_length_conflict: 300_50 | 30.00% | 4.00% | 64.00% | 2.00% | 66.00% |

### llama3_20250202_042122 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 95.00% | 5.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 23.00% | 77.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 26.00% | 3.00% | 69.00% | 2.00% | 71.00% |
| language_conflict: en_fr | 85.00% | 13.00% | 2.00% | 0.00% | 2.00% |
| num_sentence_conflict: 10_5 | 13.00% | 4.00% | 81.00% | 2.00% | 83.00% |
| word_length_conflict: 300_50 | 26.00% | 2.00% | 70.00% | 2.00% | 72.00% |

### llama3_20250202_042122 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 90.00% | 10.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 21.00% | 79.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 23.00% | 9.00% | 63.00% | 5.00% | 68.00% |
| language_conflict: en_fr | 78.00% | 19.00% | 3.00% | 0.00% | 3.00% |
| num_sentence_conflict: 10_5 | 12.00% | 6.00% | 78.00% | 4.00% | 82.00% |
| word_length_conflict: 300_50 | 33.00% | 6.00% | 60.00% | 1.00% | 61.00% |

### llama3_20250202_042122 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 95.00% | 3.00% | 2.00% | 0.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 29.00% | 71.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 40.00% | 1.00% | 57.00% | 2.00% | 59.00% |
| language_conflict: en_fr | 88.00% | 9.00% | 3.00% | 0.00% | 3.00% |
| num_sentence_conflict: 10_5 | 16.00% | 5.00% | 77.00% | 2.00% | 79.00% |
| word_length_conflict: 300_50 | 38.00% | 0.00% | 60.00% | 2.00% | 62.00% |
