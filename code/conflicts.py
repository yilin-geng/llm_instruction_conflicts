import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass


root_dir = Path(__file__).parent.parent
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import instructions


@dataclass
class ConflictEvaluation:
   constraint1_met: float  
   constraint2_met: float
#    conflict_recognized: float
#    joint_satisfaction: float # When both constraints are satisfied, which should not happen and suggests that the conflict definition is problematic.
   
class ConflictingInstructionPair:
   def __init__(
       self,
       constraint1: instructions.Instruction,
       constraint2: instructions.Instruction, 
       conflicting_kwargs: Dict,
       name: str
   ):
       self.constraint1 = constraint1
       self.constraint2 = constraint2
       self.kwargs = conflicting_kwargs
       self.name = name

   def get_constraints(self) -> Tuple[str, str]:
       constraint1 = self.constraint1.build_description(**self.kwargs[0])
       constraint2 = self.constraint2.build_description(**self.kwargs[1])
       return constraint1, constraint2

   def evaluate_response(self, response: str) -> ConflictEvaluation:
       # First build the descriptions with the kwargs
       constraint1 = self.constraint1.build_description(**self.kwargs[0])
       constraint2 = self.constraint2.build_description(**self.kwargs[1])
       
       # Then check following
       met1 = self.constraint1.check_following(response)
       met2 = self.constraint2.check_following(response)
       
       # Use LLM to check conflict recognition
    #    recognized = check_conflict_recognition_llm(response)

       # sanity check
       if met1 and met2:
           logger.warning(f"Conflict between {constraint1} and {constraint2} are simultaneously met in {self.name}. Modify the conflict definition.")
       
       return ConflictEvaluation(
           float(met1), 
           float(met2),
        #    float(recognized),
        #    float(met1 and met2)
       )

# def check_conflict_recognition_llm(response: str) -> float:
#     """Use GPT-4o to check if the response recognizes a conflict between instructions."""

#     system_prompt = """You are analyzing whether the instructions given to a LLM has conflicts based on its response. Your task is to determine if a given response 
#     recognizes or acknowledges a conflict explicitly. Return only a number between 0 and 1, where:
#     0 = No recognition of conflict
#     1 = Recognition of conflict"""
    
#     user_prompt = f"""
#     Response to analyze:
#     {response}
    
#     Does this response recognize any conflict from instructions?
#     Return only a integer (0 or 1)."""
    
#     from llm_api import get_completion_gpt4omini
#     decision = get_completion_gpt4omini(system_prompt, user_prompt).strip()
#     try:
#         return float(decision)
#     except:
#         # when we are not getting a number output the llm decision
#         print('failed')
#         return 0.0



