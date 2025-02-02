# Detailed Conflict Resolution Analysis

## Overall Performance Rates

| Model | Policy | Success Rate | Failure Rate |
|-------|---------|--------------|-------------|
| gpt4_20250201_222556 | baseline_all_user | 25.00% | 75.00% |
| gpt4_20250201_222556 | basic_separation | 37.50% | 62.50% |
| gpt4_20250201_222556 | emphasized_separation | 44.50% | 55.50% |
| gpt4_20250201_222556 | marked_system_basic | 70.50% | 29.50% |
| gpt4_20250201_222556 | marked_system_detailed | 70.83% | 29.17% |
| gpt4_20250201_222556 | marked_user_basic | 75.50% | 24.50% |
| gpt4_20250201_222556 | marked_user_detailed | 69.00% | 31.00% |
| gpt4_20250201_222556 | task_specified_separation | 57.33% | 42.67% |
| gpt4_20250201_222556 | unmarked_system_basic | 40.00% | 60.00% |
| gpt4_20250201_222556 | unmarked_system_detailed | 45.50% | 54.50% |
| gpt4_20250201_222556 | unmarked_user_basic | 46.00% | 54.00% |
| gpt4_20250201_222556 | unmarked_user_detailed | 48.83% | 51.17% |

## Detailed Rates

| Model | Policy | Recognized | Primary Only | Secondary Only | None Met | Success Rate | Failure Rate |
|-------|---------|------------|--------------|----------------|----------|--------------|-------------|
| gpt4_20250201_222556 | baseline_all_user | 8.50% | 16.50% | 48.00% | 27.00% | 25.00% | 75.00% |
| gpt4_20250201_222556 | basic_separation | 8.67% | 28.83% | 38.33% | 24.17% | 37.50% | 62.50% |
| gpt4_20250201_222556 | emphasized_separation | 10.67% | 33.83% | 31.33% | 24.17% | 44.50% | 55.50% |
| gpt4_20250201_222556 | marked_system_basic | 9.50% | 61.00% | 15.00% | 14.50% | 70.50% | 29.50% |
| gpt4_20250201_222556 | marked_system_detailed | 15.67% | 55.17% | 16.00% | 13.17% | 70.83% | 29.17% |
| gpt4_20250201_222556 | marked_user_basic | 10.00% | 65.50% | 9.67% | 14.83% | 75.50% | 24.50% |
| gpt4_20250201_222556 | marked_user_detailed | 18.17% | 50.83% | 17.17% | 13.83% | 69.00% | 31.00% |
| gpt4_20250201_222556 | task_specified_separation | 6.33% | 51.00% | 21.83% | 20.83% | 57.33% | 42.67% |
| gpt4_20250201_222556 | unmarked_system_basic | 11.17% | 28.83% | 33.17% | 26.83% | 40.00% | 60.00% |
| gpt4_20250201_222556 | unmarked_system_detailed | 18.83% | 26.67% | 49.83% | 4.67% | 45.50% | 54.50% |
| gpt4_20250201_222556 | unmarked_user_basic | 21.00% | 25.00% | 46.50% | 7.50% | 46.00% | 54.00% |
| gpt4_20250201_222556 | unmarked_user_detailed | 21.67% | 27.17% | 46.00% | 5.17% | 48.83% | 51.17% |

## Statistics by Conflict Type


### gpt4_20250201_222556 - baseline_all_user

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 5.00% | 0.00% | 93.00% | 2.00% | 95.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 10.00% | 42.00% | 10.00% | 38.00% | 48.00% |
| language_conflict: en_fr | 22.00% | 19.00% | 55.00% | 4.00% | 59.00% |
| num_sentence_conflict: 10_5 | 6.00% | 31.00% | 2.00% | 61.00% | 63.00% |
| word_length_conflict: 300_50 | 4.00% | 7.00% | 32.00% | 57.00% | 89.00% |

### gpt4_20250201_222556 - basic_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 28.00% | 71.00% | 0.00% | 1.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 4.00% | 9.00% | 48.00% | 39.00% | 87.00% |
| language_conflict: en_fr | 7.00% | 78.00% | 15.00% | 0.00% | 15.00% |
| num_sentence_conflict: 10_5 | 6.00% | 13.00% | 13.00% | 68.00% | 81.00% |
| word_length_conflict: 300_50 | 1.00% | 2.00% | 60.00% | 37.00% | 97.00% |

### gpt4_20250201_222556 - emphasized_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 37.00% | 61.00% | 0.00% | 2.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 6.00% | 0.00% | 94.00% | 0.00% | 94.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 31.00% | 34.00% | 28.00% | 62.00% |
| language_conflict: en_fr | 4.00% | 95.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 3.00% | 12.00% | 12.00% | 73.00% | 85.00% |
| word_length_conflict: 300_50 | 7.00% | 4.00% | 47.00% | 42.00% | 89.00% |

### gpt4_20250201_222556 - marked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 11.00% | 87.00% | 0.00% | 2.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 91.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 49.00% | 15.00% | 30.00% | 45.00% |
| language_conflict: en_fr | 14.00% | 83.00% | 3.00% | 0.00% | 3.00% |
| num_sentence_conflict: 10_5 | 7.00% | 13.00% | 46.00% | 34.00% | 80.00% |
| word_length_conflict: 300_50 | 10.00% | 43.00% | 26.00% | 21.00% | 47.00% |

### gpt4_20250201_222556 - marked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 21.00% | 77.00% | 1.00% | 1.00% | 2.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 92.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 9.00% | 53.00% | 13.00% | 25.00% | 38.00% |
| language_conflict: en_fr | 38.00% | 60.00% | 2.00% | 0.00% | 2.00% |
| num_sentence_conflict: 10_5 | 9.00% | 11.00% | 47.00% | 33.00% | 80.00% |
| word_length_conflict: 300_50 | 9.00% | 38.00% | 33.00% | 20.00% | 53.00% |

### gpt4_20250201_222556 - marked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 14.00% | 83.00% | 0.00% | 3.00% | 3.00% |
| keyword_forbidden_conflict: awesome_need | 11.00% | 89.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 64.00% | 8.00% | 22.00% | 30.00% |
| language_conflict: en_fr | 18.00% | 81.00% | 1.00% | 0.00% | 1.00% |
| num_sentence_conflict: 10_5 | 5.00% | 23.00% | 31.00% | 41.00% | 72.00% |
| word_length_conflict: 300_50 | 6.00% | 53.00% | 18.00% | 23.00% | 41.00% |

### gpt4_20250201_222556 - marked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 20.00% | 79.00% | 0.00% | 1.00% | 1.00% |
| keyword_forbidden_conflict: awesome_need | 18.00% | 81.00% | 1.00% | 0.00% | 1.00% |
| keyword_frequency_conflict: like_5_2 | 7.00% | 48.00% | 16.00% | 29.00% | 45.00% |
| language_conflict: en_fr | 40.00% | 55.00% | 5.00% | 0.00% | 5.00% |
| num_sentence_conflict: 10_5 | 8.00% | 14.00% | 39.00% | 39.00% | 78.00% |
| word_length_conflict: 300_50 | 16.00% | 28.00% | 42.00% | 14.00% | 56.00% |

### gpt4_20250201_222556 - task_specified_separation

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 10.00% | 82.00% | 0.00% | 8.00% | 8.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 1.00% | 91.00% | 0.00% | 91.00% |
| keyword_frequency_conflict: like_5_2 | 6.00% | 67.00% | 2.00% | 25.00% | 27.00% |
| language_conflict: en_fr | 6.00% | 94.00% | 0.00% | 0.00% | 0.00% |
| num_sentence_conflict: 10_5 | 5.00% | 38.00% | 4.00% | 53.00% | 57.00% |
| word_length_conflict: 300_50 | 3.00% | 24.00% | 34.00% | 39.00% | 73.00% |

### gpt4_20250201_222556 - unmarked_system_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 22.00% | 25.00% | 47.00% | 6.00% | 53.00% |
| keyword_forbidden_conflict: awesome_need | 4.00% | 0.00% | 96.00% | 0.00% | 96.00% |
| keyword_frequency_conflict: like_5_2 | 11.00% | 35.00% | 12.00% | 42.00% | 54.00% |
| language_conflict: en_fr | 11.00% | 68.00% | 16.00% | 5.00% | 21.00% |
| num_sentence_conflict: 10_5 | 8.00% | 33.00% | 3.00% | 56.00% | 59.00% |
| word_length_conflict: 300_50 | 11.00% | 12.00% | 25.00% | 52.00% | 77.00% |

### gpt4_20250201_222556 - unmarked_system_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 54.00% | 15.00% | 26.00% | 5.00% | 31.00% |
| keyword_forbidden_conflict: awesome_need | 12.00% | 88.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 8.00% | 10.00% | 65.00% | 17.00% | 82.00% |
| language_conflict: en_fr | 15.00% | 46.00% | 39.00% | 0.00% | 39.00% |
| num_sentence_conflict: 10_5 | 11.00% | 1.00% | 86.00% | 2.00% | 88.00% |
| word_length_conflict: 300_50 | 13.00% | 0.00% | 83.00% | 4.00% | 87.00% |

### gpt4_20250201_222556 - unmarked_user_basic

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 61.00% | 18.00% | 11.00% | 10.00% | 21.00% |
| keyword_forbidden_conflict: awesome_need | 9.00% | 91.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 8.00% | 9.00% | 63.00% | 20.00% | 83.00% |
| language_conflict: en_fr | 22.00% | 31.00% | 47.00% | 0.00% | 47.00% |
| num_sentence_conflict: 10_5 | 13.00% | 0.00% | 82.00% | 5.00% | 87.00% |
| word_length_conflict: 300_50 | 13.00% | 1.00% | 76.00% | 10.00% | 86.00% |

### gpt4_20250201_222556 - unmarked_user_detailed

| Conflict Type | Recognized | Primary | Secondary | None | Failure Rate |
|---------------|------------|---------|-----------|------|-------------|
| case_conflict | 61.00% | 12.00% | 25.00% | 2.00% | 27.00% |
| keyword_forbidden_conflict: awesome_need | 8.00% | 92.00% | 0.00% | 0.00% | 0.00% |
| keyword_frequency_conflict: like_5_2 | 12.00% | 12.00% | 58.00% | 18.00% | 76.00% |
| language_conflict: en_fr | 22.00% | 46.00% | 32.00% | 0.00% | 32.00% |
| num_sentence_conflict: 10_5 | 14.00% | 1.00% | 82.00% | 3.00% | 85.00% |
| word_length_conflict: 300_50 | 13.00% | 0.00% | 79.00% | 8.00% | 87.00% |
