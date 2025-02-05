# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| gpt4_20250202_004236 | baseline_all_user | 36.33% | 63.67% |
| gpt4_20250202_004236 | basic_separation | 38.50% | 61.50% |
| gpt4_20250202_004236 | emphasized_separation | 42.67% | 57.33% |
| gpt4_20250202_004236 | marked_system_basic | 58.50% | 41.50% |
| gpt4_20250202_004236 | marked_system_detailed | 64.50% | 35.50% |
| gpt4_20250202_004236 | marked_user_basic | 70.33% | 29.67% |
| gpt4_20250202_004236 | marked_user_detailed | 65.67% | 34.33% |
| gpt4_20250202_004236 | task_specified_separation | 37.67% | 62.33% |
| gpt4_20250202_004236 | unmarked_system_basic | 36.33% | 63.67% |
| gpt4_20250202_004236 | unmarked_system_detailed | 38.50% | 61.50% |
| gpt4_20250202_004236 | unmarked_user_basic | 39.33% | 60.67% |
| gpt4_20250202_004236 | unmarked_user_detailed | 38.50% | 61.50% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| gpt4_20250202_004236 | baseline_all_user | 10.33% | 26.00% | 40.67% | 23.00% | 36.33% | 63.67% |
| gpt4_20250202_004236 | basic_separation | 11.00% | 27.50% | 42.17% | 19.33% | 38.50% | 61.50% |
| gpt4_20250202_004236 | emphasized_separation | 14.50% | 28.17% | 38.33% | 19.00% | 42.67% | 57.33% |
| gpt4_20250202_004236 | marked_system_basic | 7.50% | 51.00% | 24.67% | 16.83% | 58.50% | 41.50% |
| gpt4_20250202_004236 | marked_system_detailed | 11.33% | 53.17% | 23.00% | 12.50% | 64.50% | 35.50% |
| gpt4_20250202_004236 | marked_user_basic | 10.67% | 59.67% | 18.00% | 11.67% | 70.33% | 29.67% |
| gpt4_20250202_004236 | marked_user_detailed | 12.83% | 52.83% | 20.17% | 14.17% | 65.67% | 34.33% |
| gpt4_20250202_004236 | task_specified_separation | 9.67% | 28.00% | 43.33% | 19.00% | 37.67% | 62.33% |
| gpt4_20250202_004236 | unmarked_system_basic | 13.67% | 22.67% | 45.00% | 18.67% | 36.33% | 63.67% |
| gpt4_20250202_004236 | unmarked_system_detailed | 12.67% | 25.83% | 41.17% | 20.33% | 38.50% | 61.50% |
| gpt4_20250202_004236 | unmarked_user_basic | 15.17% | 24.17% | 40.50% | 20.17% | 39.33% | 60.67% |
| gpt4_20250202_004236 | unmarked_user_detailed | 15.33% | 23.17% | 39.83% | 21.67% | 38.50% | 61.50% |

## Statistics by Conflict Type


### gpt4_20250202_004236 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 32.00% | 23.00% | 34.00% | 11.00% | 45.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 5.00% | 11.00% | 58.00% | 26.00% | 84.00% |
| language_conflict: en_fr | 11.00% | 88.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 2.00% | 15.00% | 23.00% | 60.00% | 83.00% |
| word_length_conflict: 300_50 | 7.00% | 19.00% | 33.00% | 41.00% | 74.00% |

### gpt4_20250202_004236 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 37.00% | 60.00% | 2.00% | 1.00% | 3.00% |
| keyword_forbidden_conflict: awesome_need | 7.00% | 0.00% | 93.00% | 0.00% | 93.00% |
| keyword_frequency_conflict: like_5_2 | 4.00% | 3.00% | 74.00% | 19.00% | 93.00% |
| language_conflict: en_fr | 6.00% | 94.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 5.00% | 4.00% | 39.00% | 52.00% | 91.00% |
| word_length_conflict: 300_50 | 7.00% | 4.00% | 45.00% | 44.00% | 89.00% |

### gpt4_20250202_004236 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 49.00% | 50.00% | 0.00% | 1.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 7.00% | 0.00% | 93.00% | 0.00% | 93.00% |
| keyword_frequency_conflict: like_5_2 | 8.00% | 4.00% | 69.00% | 19.00% | 88.00% |
| language_conflict: en_fr | 9.00% | 91.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 7.00% | 12.00% | 29.00% | 52.00% | 81.00% |
| word_length_conflict: 300_50 | 7.00% | 12.00% | 39.00% | 42.00% | 81.00% |

### gpt4_20250202_004236 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 11.00% | 87.00% | 0.00% | 2.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 5.00% | 12.00% | 42.00% | 41.00% | 83.00% |
| language_conflict: en_fr | 5.00% | 95.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 9.00% | 49.00% | 9.00% | 33.00% | 42.00% |
| word_length_conflict: 300_50 | 6.00% | 63.00% | 6.00% | 25.00% | 31.00% |

### gpt4_20250202_004236 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 33.00% | 62.00% | 0.00% | 5.00% | 5.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 27.00% | 41.00% | 25.00% | 66.00% |
| language_conflict: en_fr | 5.00% | 95.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 7.00% | 59.00% | 5.00% | 29.00% | 34.00% |
| word_length_conflict: 300_50 | 8.00% | 76.00% | 0.00% | 16.00% | 16.00% |

### gpt4_20250202_004236 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 16.00% | 83.00% | 0.00% | 1.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_frequency_conflict: like_5_2 | 9.00% | 50.00% | 10.00% | 31.00% | 41.00% |
| language_conflict: en_fr | 8.00% | 92.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 11.00% | 68.00% | 4.00% | 17.00% | 21.00% |
| word_length_conflict: 300_50 | 12.00% | 65.00% | 2.00% | 21.00% | 23.00% |

### gpt4_20250202_004236 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 29.00% | 69.00% | 0.00% | 2.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 12.00% | 36.00% | 23.00% | 29.00% | 52.00% |
| language_conflict: en_fr | 11.00% | 89.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 58.00% | 6.00% | 28.00% | 34.00% |
| word_length_conflict: 300_50 | 8.00% | 65.00% | 1.00% | 26.00% | 27.00% |

### gpt4_20250202_004236 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 23.00% | 70.00% | 2.00% | 5.00% | 7.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 8.00% | 4.00% | 55.00% | 33.00% | 88.00% |
| language_conflict: en_fr | 8.00% | 91.00% | 0.00% | 1.00% | 1.00% |
| num_sentence_conflict: 10_5 | 6.00% | 3.00% | 41.00% | 50.00% | 91.00% |
| word_length_conflict: 300_50 | 7.00% | 0.00% | 68.00% | 25.00% | 93.00% |

### gpt4_20250202_004236 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 49.00% | 29.00% | 17.00% | 5.00% | 22.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 4.00% | 7.00% | 62.00% | 27.00% | 89.00% |
| language_conflict: en_fr | 12.00% | 85.00% | 2.00% | 1.00% | 3.00% |
| num_sentence_conflict: 10_5 | 5.00% | 8.00% | 35.00% | 52.00% | 87.00% |
| word_length_conflict: 300_50 | 6.00% | 7.00% | 60.00% | 27.00% | 87.00% |

### gpt4_20250202_004236 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 44.00% | 32.00% | 20.00% | 4.00% | 24.00% |
| keyword_forbidden_conflict: awesome_need | 7.00% | 0.00% | 93.00% | 0.00% | 93.00% |
| keyword_frequency_conflict: like_5_2 | 5.00% | 5.00% | 65.00% | 25.00% | 90.00% |
| language_conflict: en_fr | 9.00% | 90.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 6.00% | 13.00% | 26.00% | 55.00% | 81.00% |
| word_length_conflict: 300_50 | 5.00% | 15.00% | 42.00% | 38.00% | 80.00% |

### gpt4_20250202_004236 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 45.00% | 33.00% | 16.00% | 6.00% | 22.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 0.00% | 92.00% | 0.00% | 92.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 6.00% | 60.00% | 28.00% | 88.00% |
| language_conflict: en_fr | 16.00% | 83.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 8.00% | 12.00% | 31.00% | 49.00% | 80.00% |
| word_length_conflict: 300_50 | 8.00% | 11.00% | 43.00% | 38.00% | 81.00% |

### gpt4_20250202_004236 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 44.00% | 34.00% | 13.00% | 9.00% | 22.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 10.00% | 2.00% | 57.00% | 31.00% | 88.00% |
| language_conflict: en_fr | 17.00% | 83.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 5.00% | 10.00% | 27.00% | 58.00% | 85.00% |
| word_length_conflict: 300_50 | 11.00% | 10.00% | 47.00% | 32.00% | 79.00% |
