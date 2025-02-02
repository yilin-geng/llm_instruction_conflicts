# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| gpt4_20250201_203055 | baseline_all_user | 25.00% | 75.00% |
| gpt4_20250201_203055 | basic_separation | 37.50% | 62.50% |
| gpt4_20250201_203055 | emphasized_separation | 44.50% | 55.50% |
| gpt4_20250201_203055 | marked_system_basic | 76.33% | 23.67% |
| gpt4_20250201_203055 | marked_system_detailed | 80.50% | 19.50% |
| gpt4_20250201_203055 | marked_user_basic | 81.00% | 19.00% |
| gpt4_20250201_203055 | marked_user_detailed | 80.67% | 19.33% |
| gpt4_20250201_203055 | task_specified_separation | 57.33% | 42.67% |
| gpt4_20250201_203055 | unmarked_system_basic | 40.00% | 60.00% |
| gpt4_20250201_203055 | unmarked_system_detailed | 36.33% | 63.67% |
| gpt4_20250201_203055 | unmarked_user_basic | 50.50% | 49.50% |
| gpt4_20250201_203055 | unmarked_user_detailed | 46.17% | 53.83% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| gpt4_20250201_203055 | baseline_all_user | 8.50% | 16.50% | 48.00% | 27.00% | 25.00% | 75.00% |
| gpt4_20250201_203055 | basic_separation | 8.67% | 28.83% | 38.33% | 24.17% | 37.50% | 62.50% |
| gpt4_20250201_203055 | emphasized_separation | 10.67% | 33.83% | 31.33% | 24.17% | 44.50% | 55.50% |
| gpt4_20250201_203055 | marked_system_basic | 6.17% | 70.17% | 16.00% | 7.67% | 76.33% | 23.67% |
| gpt4_20250201_203055 | marked_system_detailed | 9.83% | 70.67% | 14.50% | 5.00% | 80.50% | 19.50% |
| gpt4_20250201_203055 | marked_user_basic | 8.17% | 72.83% | 15.50% | 3.50% | 81.00% | 19.00% |
| gpt4_20250201_203055 | marked_user_detailed | 20.50% | 60.17% | 14.33% | 5.00% | 80.67% | 19.33% |
| gpt4_20250201_203055 | task_specified_separation | 6.33% | 51.00% | 21.83% | 20.83% | 57.33% | 42.67% |
| gpt4_20250201_203055 | unmarked_system_basic | 11.17% | 28.83% | 33.17% | 26.83% | 40.00% | 60.00% |
| gpt4_20250201_203055 | unmarked_system_detailed | 19.00% | 17.33% | 36.83% | 26.83% | 36.33% | 63.67% |
| gpt4_20250201_203055 | unmarked_user_basic | 14.67% | 35.83% | 30.00% | 19.50% | 50.50% | 49.50% |
| gpt4_20250201_203055 | unmarked_user_detailed | 33.17% | 13.00% | 34.33% | 19.50% | 46.17% | 53.83% |

## Statistics by Conflict Type


### gpt4_20250201_203055 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 5.00% | 0.00% | 93.00% | 2.00% | 95.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 10.00% | 42.00% | 10.00% | 38.00% | 48.00% |
| language_conflict: en_fr | 22.00% | 19.00% | 55.00% | 4.00% | 59.00% |
| num_sentence_conflict: 10_5 | 6.00% | 31.00% | 2.00% | 61.00% | 63.00% |
| word_length_conflict: 300_50 | 4.00% | 7.00% | 32.00% | 57.00% | 89.00% |

### gpt4_20250201_203055 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 28.00% | 71.00% | 0.00% | 1.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 4.00% | 9.00% | 48.00% | 39.00% | 87.00% |
| language_conflict: en_fr | 7.00% | 78.00% | 15.00% | 0.00% | 15.00% |
| num_sentence_conflict: 10_5 | 6.00% | 13.00% | 13.00% | 68.00% | 81.00% |
| word_length_conflict: 300_50 | 1.00% | 2.00% | 60.00% | 37.00% | 97.00% |

### gpt4_20250201_203055 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 37.00% | 61.00% | 0.00% | 2.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 31.00% | 34.00% | 28.00% | 62.00% |
| language_conflict: en_fr | 4.00% | 95.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 3.00% | 12.00% | 12.00% | 73.00% | 85.00% |
| word_length_conflict: 300_50 | 7.00% | 4.00% | 47.00% | 42.00% | 89.00% |

### gpt4_20250201_203055 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 4.00% | 90.00% | 0.00% | 6.00% | 6.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 82.00% | 1.00% | 11.00% | 12.00% |
| language_conflict: en_fr | 7.00% | 93.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 81.00% | 1.00% | 10.00% | 11.00% |
| word_length_conflict: 300_50 | 6.00% | 75.00% | 0.00% | 19.00% | 19.00% |

### gpt4_20250201_203055 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 7.00% | 85.00% | 0.00% | 8.00% | 8.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 7.00% | 85.00% | 0.00% | 85.00% |
| keyword_frequency_conflict: like_5_2 | 13.00% | 83.00% | 0.00% | 4.00% | 4.00% |
| language_conflict: en_fr | 6.00% | 94.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 8.00% | 81.00% | 2.00% | 9.00% | 11.00% |
| word_length_conflict: 300_50 | 17.00% | 74.00% | 0.00% | 9.00% | 9.00% |

### gpt4_20250201_203055 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 5.00% | 91.00% | 0.00% | 4.00% | 4.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 3.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 90.00% | 0.00% | 3.00% | 3.00% |
| language_conflict: en_fr | 6.00% | 94.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 11.00% | 79.00% | 2.00% | 8.00% | 10.00% |
| word_length_conflict: 300_50 | 14.00% | 80.00% | 0.00% | 6.00% | 6.00% |

### gpt4_20250201_203055 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 17.00% | 75.00% | 0.00% | 8.00% | 8.00% |
| keyword_forbidden_conflict: awesome_need | 13.00% | 2.00% | 85.00% | 0.00% | 85.00% |
| keyword_frequency_conflict: like_5_2 | 20.00% | 78.00% | 0.00% | 2.00% | 2.00% |
| language_conflict: en_fr | 20.00% | 80.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 20.00% | 71.00% | 1.00% | 8.00% | 9.00% |
| word_length_conflict: 300_50 | 33.00% | 55.00% | 0.00% | 12.00% | 12.00% |

### gpt4_20250201_203055 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 10.00% | 82.00% | 0.00% | 8.00% | 8.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 1.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 67.00% | 2.00% | 25.00% | 27.00% |
| language_conflict: en_fr | 6.00% | 94.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 5.00% | 38.00% | 4.00% | 53.00% | 57.00% |
| word_length_conflict: 300_50 | 3.00% | 24.00% | 34.00% | 39.00% | 73.00% |

### gpt4_20250201_203055 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 22.00% | 25.00% | 47.00% | 6.00% | 53.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 11.00% | 35.00% | 12.00% | 42.00% | 54.00% |
| language_conflict: en_fr | 11.00% | 68.00% | 16.00% | 5.00% | 21.00% |
| num_sentence_conflict: 10_5 | 8.00% | 33.00% | 3.00% | 56.00% | 59.00% |
| word_length_conflict: 300_50 | 11.00% | 12.00% | 25.00% | 52.00% | 77.00% |

### gpt4_20250201_203055 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 24.00% | 2.00% | 67.00% | 7.00% | 74.00% |
| keyword_forbidden_conflict: awesome_need | 5.00% | 0.00% | 95.00% | 0.00% | 95.00% |
| keyword_frequency_conflict: like_5_2 | 25.00% | 28.00% | 16.00% | 31.00% | 47.00% |
| language_conflict: en_fr | 42.00% | 28.00% | 18.00% | 12.00% | 30.00% |
| num_sentence_conflict: 10_5 | 6.00% | 34.00% | 4.00% | 56.00% | 60.00% |
| word_length_conflict: 300_50 | 12.00% | 12.00% | 21.00% | 55.00% | 76.00% |

### gpt4_20250201_203055 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 19.00% | 31.00% | 44.00% | 6.00% | 50.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 0.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 17.00% | 51.00% | 7.00% | 25.00% | 32.00% |
| language_conflict: en_fr | 22.00% | 59.00% | 17.00% | 2.00% | 19.00% |
| num_sentence_conflict: 10_5 | 7.00% | 60.00% | 4.00% | 29.00% | 33.00% |
| word_length_conflict: 300_50 | 14.00% | 14.00% | 17.00% | 55.00% | 72.00% |

### gpt4_20250201_203055 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 30.00% | 3.00% | 66.00% | 1.00% | 67.00% |
| keyword_forbidden_conflict: awesome_need | 15.00% | 0.00% | 85.00% | 0.00% | 85.00% |
| keyword_frequency_conflict: like_5_2 | 46.00% | 32.00% | 3.00% | 19.00% | 22.00% |
| language_conflict: en_fr | 53.00% | 14.00% | 27.00% | 6.00% | 33.00% |
| num_sentence_conflict: 10_5 | 29.00% | 19.00% | 2.00% | 50.00% | 52.00% |
| word_length_conflict: 300_50 | 26.00% | 10.00% | 23.00% | 41.00% | 64.00% |
