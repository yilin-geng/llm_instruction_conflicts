import unittest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock

from conflicts import ConflictingInstructionPair, ConflictEvaluation, check_conflict_recognition_llm
from conflicts_dict import INSTRUCTION_CONFLICTS

class TestConflicts(unittest.TestCase):
    def setUp(self):
        # Get conflict pairs directly from INSTRUCTION_CONFLICTS
        self.language_conflict_pair = INSTRUCTION_CONFLICTS["language_conflict: en_fr"]["conflict_pair"]
        self.case_conflict_pair = INSTRUCTION_CONFLICTS["case_conflict"]["conflict_pair"]
        self.word_length_conflict_pair = INSTRUCTION_CONFLICTS["word_length_conflict: 300_50"]["conflict_pair"]
        self.num_sentence_conflict_pair = INSTRUCTION_CONFLICTS["num_sentence_conflict: 10_5"]["conflict_pair"]
        self.keyword_forbidden_conflict_pair = INSTRUCTION_CONFLICTS["keyword_forbidden_conflict"]["conflict_pair"]
        self.keyword_frequency_conflict_pair = INSTRUCTION_CONFLICTS["keyword_frequency_conflict"]["conflict_pair"]


    def test_language_conflict(self):


        response_en = "This is an English response."
        eval_en = self.language_conflict_pair.evaluate_response(response_en)
        self.assertEqual(eval_en.constraint1_met, 1.0)  # English constraint met
        self.assertEqual(eval_en.constraint2_met, 0.0)  # French constraint not met
        self.assertEqual(eval_en.conflict_recognized, 0.0) 

        response_fr = "C'est une réponse en français."
        eval_fr = self.language_conflict_pair.evaluate_response(response_fr)
        self.assertEqual(eval_fr.constraint1_met, 0.0)  # English constraint not met
        self.assertEqual(eval_fr.constraint2_met, 1.0)  # French constraint met
        self.assertEqual(eval_fr.conflict_recognized, 0.0) 


    def test_case_conflict(self):

        
        # Test uppercase response
        response_upper = "THIS IS ALL UPPERCASE"
        eval_upper = self.case_conflict_pair.evaluate_response(response_upper)
        self.assertEqual(eval_upper.constraint1_met, 1.0)  # Uppercase constraint met
        self.assertEqual(eval_upper.constraint2_met, 0.0)  # Lowercase constraint not met
        self.assertEqual(eval_upper.conflict_recognized, 0.0) 
        # Test lowercase response
        response_lower = "this is all lowercase"
        eval_lower = self.case_conflict_pair.evaluate_response(response_lower)
        self.assertEqual(eval_lower.constraint1_met, 0.0)  # Uppercase constraint not met
        self.assertEqual(eval_lower.constraint2_met, 1.0)  # Lowercase constraint met
        self.assertEqual(eval_lower.conflict_recognized, 0.0) 


    def test_word_length_conflict(self):

        
        # Generate responses of different lengths
        short_response = " ".join(["word"] * 40)  # 40 words
        long_response = " ".join(["word"] * 350)  # 350 words
        
        eval_short = self.word_length_conflict_pair.evaluate_response(short_response)
        self.assertEqual(eval_short.constraint1_met, 0.0)  # At least 300 words not met
        self.assertEqual(eval_short.constraint2_met, 1.0)  # Less than 50 words not met
        self.assertEqual(eval_short.conflict_recognized, 0.0) 
        
        eval_long = self.word_length_conflict_pair.evaluate_response(long_response)
        self.assertEqual(eval_long.constraint1_met, 1.0)  # At least 300 words met
        self.assertEqual(eval_long.constraint2_met, 0.0)  # Less than 50 words not met
        self.assertEqual(eval_long.conflict_recognized, 0.0) 


    def test_num_sentence_conflict(self):

        few_sentences = "This is one. This is two. This is three."
        many_sentences = ". ".join(["This is sentence"] * 12)
        recognized = "There is a confliction in the instructions given. It is not possible to meet the requirements."
        
        eval_few = self.num_sentence_conflict_pair.evaluate_response(few_sentences)
        self.assertEqual(eval_few.constraint1_met, 0.0)  
        self.assertEqual(eval_few.constraint2_met, 1.0) 
        self.assertEqual(eval_few.conflict_recognized, 0.0) 
        
        eval_many = self.num_sentence_conflict_pair.evaluate_response(many_sentences)
        self.assertEqual(eval_many.constraint1_met, 1.0)  
        self.assertEqual(eval_many.constraint2_met, 0.0)
        self.assertEqual(eval_many.conflict_recognized, 0.0) 

        eval_recognized = self.num_sentence_conflict_pair.evaluate_response(recognized)
        self.assertEqual(eval_recognized.constraint1_met, 0.0)  
        self.assertEqual(eval_recognized.constraint2_met, 1.0)
        self.assertEqual(eval_recognized.conflict_recognized, 1.0)
        self.assertEqual(eval_recognized.joint_satisfaction, 0.0)


    def test_keyword_forbidden_conflict(self):

        with_keywords = "This example is a test of the system."
        without_keywords = "This is a simple response."
        
        eval_with = self.keyword_forbidden_conflict_pair.evaluate_response(with_keywords)
        self.assertEqual(eval_with.constraint1_met, 1.0)  # Keywords present
        self.assertEqual(eval_with.constraint2_met, 0.0)  
        self.assertEqual(eval_with.conflict_recognized, 0.0) 
        eval_without = self.keyword_forbidden_conflict_pair.evaluate_response(without_keywords)
        self.assertEqual(eval_without.constraint1_met, 0.0)  # Keywords not present
        self.assertEqual(eval_without.constraint2_met, 1.0)  
        self.assertEqual(eval_without.conflict_recognized, 0.0) 

    def test_keyword_frequency_conflict(self):
        
        few_keywords = "This is an example of a response."
        many_keywords = " example ".join(["This is an"] * 12)
        
        eval_few = self.keyword_frequency_conflict_pair.evaluate_response(few_keywords)
        self.assertEqual(eval_few.constraint1_met, 0.0)  # At least 10 occurrences not met
        self.assertEqual(eval_few.constraint2_met, 1.0)  # Less than 2 occurrences met
        self.assertEqual(eval_few.conflict_recognized, 0.0) 
        eval_many = self.keyword_frequency_conflict_pair.evaluate_response(many_keywords)
        self.assertEqual(eval_many.constraint1_met, 1.0)  # At least 10 occurrences met
        self.assertEqual(eval_many.constraint2_met, 0.0)  # Less than 2 occurrences not met
        self.assertEqual(eval_many.conflict_recognized, 0.0) 


if __name__ == '__main__':
    unittest.main()
