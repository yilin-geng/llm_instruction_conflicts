# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| llama3_20250201_235232 | baseline_all_user | 81.33% | 18.67% |
| llama3_20250201_235232 | basic_separation | 45.33% | 54.67% |
| llama3_20250201_235232 | emphasized_separation | 78.67% | 21.33% |
| llama3_20250201_235232 | marked_system_basic | 95.17% | 4.83% |
| llama3_20250201_235232 | marked_system_detailed | 89.00% | 11.00% |
| llama3_20250201_235232 | marked_user_basic | 94.83% | 5.17% |
| llama3_20250201_235232 | marked_user_detailed | 90.83% | 9.17% |
| llama3_20250201_235232 | task_specified_separation | 29.83% | 70.17% |
| llama3_20250201_235232 | unmarked_system_basic | 87.33% | 12.67% |
| llama3_20250201_235232 | unmarked_system_detailed | 86.00% | 14.00% |
| llama3_20250201_235232 | unmarked_user_basic | 87.67% | 12.33% |
| llama3_20250201_235232 | unmarked_user_detailed | 90.17% | 9.83% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| llama3_20250201_235232 | baseline_all_user | 70.17% | 11.17% | 18.50% | 0.17% | 81.33% | 18.67% |
| llama3_20250201_235232 | basic_separation | 33.00% | 12.33% | 54.33% | 0.33% | 45.33% | 54.67% |
| llama3_20250201_235232 | emphasized_separation | 59.00% | 19.67% | 19.17% | 2.17% | 78.67% | 21.33% |
| llama3_20250201_235232 | marked_system_basic | 29.00% | 66.17% | 0.00% | 4.83% | 95.17% | 4.83% |
| llama3_20250201_235232 | marked_system_detailed | 63.83% | 25.17% | 5.00% | 6.00% | 89.00% | 11.00% |
| llama3_20250201_235232 | marked_user_basic | 14.83% | 80.00% | 0.00% | 5.17% | 94.83% | 5.17% |
| llama3_20250201_235232 | marked_user_detailed | 65.67% | 25.17% | 4.67% | 4.50% | 90.83% | 9.17% |
| llama3_20250201_235232 | task_specified_separation | 13.33% | 16.50% | 69.17% | 1.00% | 29.83% | 70.17% |
| llama3_20250201_235232 | unmarked_system_basic | 62.83% | 24.50% | 11.50% | 1.17% | 87.33% | 12.67% |
| llama3_20250201_235232 | unmarked_system_detailed | 75.50% | 10.50% | 13.67% | 0.33% | 86.00% | 14.00% |
| llama3_20250201_235232 | unmarked_user_basic | 57.17% | 30.50% | 7.33% | 5.00% | 87.67% | 12.33% |
| llama3_20250201_235232 | unmarked_user_detailed | 86.83% | 3.33% | 9.67% | 0.17% | 90.17% | 9.83% |

## Statistics by Conflict Type


### llama3_20250201_235232 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 98.00% | 2.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 41.00% | 59.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 41.00% | 5.00% | 53.00% | 1.00% | 54.00% |
| language_conflict: en_fr | 93.00% | 0.00% | 7.00% | 0.00% | 7.00% |
| num_sentence_conflict: 10_5 | 72.00% | 1.00% | 27.00% | 0.00% | 27.00% |
| word_length_conflict: 300_50 | 76.00% | 0.00% | 24.00% | 0.00% | 24.00% |

### llama3_20250201_235232 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 85.00% | 0.00% | 15.00% | 0.00% | 15.00% |
| keyword_forbidden_conflict: awesome_need | 26.00% | 74.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 0.00% | 93.00% | 0.00% | 93.00% |
| language_conflict: en_fr | 61.00% | 0.00% | 39.00% | 0.00% | 39.00% |
| num_sentence_conflict: 10_5 | 8.00% | 0.00% | 90.00% | 2.00% | 92.00% |
| word_length_conflict: 300_50 | 11.00% | 0.00% | 89.00% | 0.00% | 89.00% |

### llama3_20250201_235232 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 96.00% | 3.00% | 1.00% | 0.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 49.00% | 51.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 10.00% | 0.00% | 90.00% | 0.00% | 90.00% |
| language_conflict: en_fr | 85.00% | 0.00% | 15.00% | 0.00% | 15.00% |
| num_sentence_conflict: 10_5 | 77.00% | 3.00% | 7.00% | 13.00% | 20.00% |
| word_length_conflict: 300_50 | 37.00% | 61.00% | 2.00% | 0.00% | 2.00% |

### llama3_20250201_235232 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 60.00% | 40.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 25.00% | 75.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 17.00% | 82.00% | 0.00% | 1.00% | 1.00% |
| language_conflict: en_fr | 50.00% | 49.00% | 0.00% | 1.00% | 1.00% |
| num_sentence_conflict: 10_5 | 21.00% | 52.00% | 0.00% | 27.00% | 27.00% |
| word_length_conflict: 300_50 | 1.00% | 99.00% | 0.00% | 0.00% | 0.00% |

### llama3_20250201_235232 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 82.00% | 18.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 73.00% | 27.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 51.00% | 45.00% | 0.00% | 4.00% | 4.00% |
| language_conflict: en_fr | 99.00% | 1.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 50.00% | 25.00% | 0.00% | 25.00% | 25.00% |
| word_length_conflict: 300_50 | 28.00% | 35.00% | 30.00% | 7.00% | 37.00% |

### llama3_20250201_235232 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 13.00% | 87.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 12.00% | 88.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 12.00% | 88.00% | 0.00% | 0.00% | 0.00% |
| language_conflict: en_fr | 38.00% | 62.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 11.00% | 58.00% | 0.00% | 31.00% | 31.00% |
| word_length_conflict: 300_50 | 3.00% | 97.00% | 0.00% | 0.00% | 0.00% |

### llama3_20250201_235232 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 90.00% | 10.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 69.00% | 31.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 66.00% | 29.00% | 0.00% | 5.00% | 5.00% |
| language_conflict: en_fr | 96.00% | 4.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 51.00% | 36.00% | 0.00% | 13.00% | 13.00% |
| word_length_conflict: 300_50 | 22.00% | 41.00% | 28.00% | 9.00% | 37.00% |

### llama3_20250201_235232 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 42.00% | 1.00% | 54.00% | 3.00% | 57.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 92.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 3.00% | 91.00% | 0.00% | 91.00% |
| language_conflict: en_fr | 9.00% | 2.00% | 89.00% | 0.00% | 89.00% |
| num_sentence_conflict: 10_5 | 6.00% | 1.00% | 90.00% | 3.00% | 93.00% |
| word_length_conflict: 300_50 | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |

### llama3_20250201_235232 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 98.00% | 2.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 55.00% | 45.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 9.00% | 63.00% | 26.00% | 2.00% | 28.00% |
| language_conflict: en_fr | 69.00% | 22.00% | 9.00% | 0.00% | 9.00% |
| num_sentence_conflict: 10_5 | 70.00% | 1.00% | 25.00% | 4.00% | 29.00% |
| word_length_conflict: 300_50 | 76.00% | 14.00% | 9.00% | 1.00% | 10.00% |

### llama3_20250201_235232 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 98.00% | 2.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 45.00% | 55.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 55.00% | 6.00% | 37.00% | 2.00% | 39.00% |
| language_conflict: en_fr | 92.00% | 0.00% | 8.00% | 0.00% | 8.00% |
| num_sentence_conflict: 10_5 | 80.00% | 0.00% | 20.00% | 0.00% | 20.00% |
| word_length_conflict: 300_50 | 83.00% | 0.00% | 17.00% | 0.00% | 17.00% |

### llama3_20250201_235232 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 81.00% | 19.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 62.00% | 38.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 83.00% | 6.00% | 4.00% | 10.00% |
| language_conflict: en_fr | 63.00% | 28.00% | 8.00% | 1.00% | 9.00% |
| num_sentence_conflict: 10_5 | 48.00% | 3.00% | 24.00% | 25.00% | 49.00% |
| word_length_conflict: 300_50 | 82.00% | 12.00% | 6.00% | 0.00% | 6.00% |

### llama3_20250201_235232 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 99.00% | 1.00% | 0.00% | 0.00% | 0.00% |
| keyword_forbidden_conflict: awesome_need | 85.00% | 15.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 77.00% | 4.00% | 18.00% | 1.00% | 19.00% |
| language_conflict: en_fr | 95.00% | 0.00% | 5.00% | 0.00% | 5.00% |
| num_sentence_conflict: 10_5 | 83.00% | 0.00% | 17.00% | 0.00% | 17.00% |
| word_length_conflict: 300_50 | 82.00% | 0.00% | 18.00% | 0.00% | 18.00% |
