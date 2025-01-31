import sys
from pathlib import Path
root_dir = Path(__file__).parent.parent
import instructions
from conflicts import ConflictingInstructionPair

INSTRUCTION_CONFLICTS = {
    "language_conflict: en_fr": {
        "related_instruction_ids": ["language:response_language"],
        "conflict_pair": ConflictingInstructionPair(
            instructions.ResponseLanguageChecker("lang1"),
            instructions.ResponseLanguageChecker("lang2"), 
            [{"language": "en"}, {"language": "fr"}],
            "language_conflict: en_fr"
        )
    },
    
    "case_conflict": {
        "related_instruction_ids": [
            "change_cases:english_capital",
            "change_cases:english_lowercase",
            "change_cases:capital_word_frequency"
        ],
        "conflict_pair": ConflictingInstructionPair(
            instructions.CapitalLettersEnglishChecker("caps"),
            instructions.LowercaseLettersEnglishChecker("lower"),
            [{}, {}],
            "case_conflict"
        )
    },
    
    "word_length_conflict: 300_50": {
        "related_instruction_ids": [
            "length_constraints:number_words"
        ],
        "conflict_pair": ConflictingInstructionPair(
            instructions.NumberOfWords("words1"),
            instructions.NumberOfWords("words2"),
            [{"num_words": 300, "relation": "at least"}, 
             {"num_words": 50, "relation": "less than"}],
            "word_length_conflict: 300_50"
        )
    },
    
    "num_sentence_conflict: 10_5": {
        "related_instruction_ids": [
            "length_constraints:number_sentences",
            "length_constraints:number_paragraphs"
        ],
        "conflict_pair": ConflictingInstructionPair(
            instructions.NumberOfSentences("sent1"),  
            instructions.NumberOfSentences("sent2"),
            [{"num_sentences": 10, "relation": "at least"},
             {"num_sentences": 5, "relation": "less than"}],
            "num_sentence_conflict: 10_5"
        )
    },
    
    "keyword_forbidden_conflict: awesome_need": {
        "related_instruction_ids": [
            "keywords:existence",
            "keywords:forbidden_words"
        ],
        "conflict_pair": ConflictingInstructionPair(
            instructions.KeywordChecker("keywords"), 
            instructions.ForbiddenWords("forbidden"),
            [{"keywords": ["awesome, need"]}, 
             {"forbidden_words": ["awesome, need"]}],
            "keyword_forbidden_conflict: awesome_need"
        )
    },
    
    "keyword_frequency_conflict: like_5_2": {
        "related_instruction_ids": [
            "keywords:frequency"
        ],
        "conflict_pair": ConflictingInstructionPair(
            instructions.KeywordFrequencyChecker("freq1"),
            instructions.KeywordFrequencyChecker("freq2"),
            [{"keyword": "like", "frequency": 5, "relation": "at least"},
             {"keyword": "like", "frequency": 2, "relation": "less than"}],
            "keyword_frequency_conflict: like_5_2"
        )
    },

      #     "num_paragraph_conflict: 1_5": {
    #     "related_instruction_ids": [
    #         "length_constraints:number_paragraphs"
    #     ],
    #     "conflict_pair": ConflictingInstructionPair(
    #         instructions.ParagraphChecker("para1"),
    #         instructions.ParagraphChecker("para2"),
    #         [{"num_paragraphs": 1},
    #          {"num_paragraphs": 5}],
    #         "num_paragraph_conflict: 1_5"
    #     )
    # },
    
    # "json_colon_conflict": {
    #     "related_instruction_ids": [
    #         "detectable_format:json_format"
    #     ],
    #     "conflict_pair": ConflictingInstructionPair(
    #         instructions.JsonFormat("json"),
    #         instructions.LetterFrequencyChecker("no_colon"),
    #         [{}, {"letter": ":", "let_frequency": 1, "let_relation": "less than"}],
    #         "json_colon_conflict"
    #     )
    # },

} 