from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Iterator
from dataclasses import dataclass
import json
from pathlib import Path
import logging
from conflicts_dict import INSTRUCTION_CONFLICTS
import textwrap
logger = logging.getLogger(__name__)

@dataclass
class PolicyEvaluation:
    conflict_name: str
    policy_name: str
    primary_constraint_met: float
    secondary_constraint_met: float
    response: str
    system_prompt: str
    user_prompt: str
    base_instruction: str
    constraint1: str
    constraint2: str

class ConflictDataLoader:
    def __init__(self, data_path: Path):
        self.data_path = data_path
    
    def load_conflicts(self) -> Iterator[Dict]:
        with open(self.data_path, 'r') as f:
            for line in f:
                yield json.loads(line)

class PriorityControlPolicy(ABC):
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        """Get both system and user prompts according to the policy."""
        pass
        
    def prepare_evaluation_batch(self, conflicts: List[Dict]) -> Tuple[List[Dict], List[Tuple[str, str]]]:
        """Prepare a batch of prompts for evaluation."""
        conflict_data = []
        prompts = []
        
        for conflict in conflicts:
            system_prompt, user_prompt = self.get_prompts(
                base_instruction=conflict['base_instruction'],
                constraint1=conflict['constraint1'],
                constraint2=conflict['constraint2']
            )
            conflict_data.append(conflict)
            prompts.append((system_prompt, user_prompt))
            
        return conflict_data, prompts

    def evaluate_responses(self, conflict_data: List[Dict], responses: List[str], is_reversed: bool, conflicts_dict=INSTRUCTION_CONFLICTS) -> List[PolicyEvaluation]:
        """Evaluate a batch of responses."""
        results = []
        
        for conflict, response in zip(conflict_data, responses):

            conflict_pair = conflicts_dict[conflict['conflict_name']]['conflict_pair']
            eval_result = conflict_pair.evaluate_response(response)
            
            # If using reversed data, swap constraint results
            if is_reversed:
                primary_met = eval_result.constraint2_met
                secondary_met = eval_result.constraint1_met
            else:
                primary_met = eval_result.constraint1_met
                secondary_met = eval_result.constraint2_met
            
            system_prompt, user_prompt = self.get_prompts(
                base_instruction=conflict['base_instruction'],
                constraint1=conflict['constraint1'],
                constraint2=conflict['constraint2']
            )
            
            results.append(PolicyEvaluation(
                policy_name=self.name,
                conflict_name=conflict['conflict_name'],
                primary_constraint_met=primary_met,
                secondary_constraint_met=secondary_met,
                response=response,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                base_instruction=conflict['base_instruction'],
                constraint1=conflict['constraint1'],
                constraint2=conflict['constraint2']
            ))
            
        return results


# Set 1: Testing System/User Separation Effect
# Tests whether system/user prompt separation naturally creates priority


class ConstraintFollowingBaselineSystem(PriorityControlPolicy):
    """Base case: Instruction following behavior without conflicts."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = f"{base_instruction} {constraint1}"
        user_prompt = ""
        return system_prompt, user_prompt

class ConstraintFollowingBaseline(PriorityControlPolicy):
    """Base case: Instruction following behavior without conflicts."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = f"{base_instruction} {constraint1}"
        return system_prompt, user_prompt

class BaselineAllUserPolicy(PriorityControlPolicy):
    """Base case: Everything in user prompt.
    Tests natural instruction following behavior without intervention."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = f"{base_instruction} {constraint1} {constraint2}"
        return system_prompt, user_prompt

class BasicSeparationPolicy(PriorityControlPolicy):
    """Pure separation: Places primary instruction in system prompt to leverage implicit role-based priority. 
    Tests if system/user separation creates natural priority."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = f"{constraint1}"
        user_prompt = f"{base_instruction} {constraint2}"
        return system_prompt, user_prompt

class TaskSpecifiedSeparationPolicy(PriorityControlPolicy):
    """Base task in both prompts with separation.
    Tests if task specification affects priority."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = f"{base_instruction} {constraint1}"
        user_prompt = f"{base_instruction} {constraint2}"
        return system_prompt, user_prompt

class EmphasizedSeparationPolicy(PriorityControlPolicy):
    """Adds specific guidelines to separation.
    Tests if explicit emphasis enhances separation effect."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = f"You must always follow this constraint: {constraint1}"
        user_prompt = f"{base_instruction} {constraint2}"
        return system_prompt, user_prompt

# Set 2: Testing Conflict Resolution Policies
# Tests how different policy statements handle conflicts in user prompt

class UnmarkedSystemPolicyBasic(PriorityControlPolicy):
    """Basic system policy, unmarked constraints.
    Tests simple priority rule with original constraint text."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = "When constraints conflict, follow the first constraint provided."
        user_prompt = f"{base_instruction} {constraint1} {constraint2}"
        return system_prompt, user_prompt

class MarkedSystemPolicyBasic(PriorityControlPolicy):
    """Basic system policy, marked constraints.
    Tests if constraint marking improves policy effectiveness."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = "When constraints conflict, follow Constraint 1 over Constraint 2."
        user_prompt = f"{base_instruction} Constraint 1: {constraint1} Constraint 2: {constraint2}"
        return system_prompt, user_prompt

class UnmarkedUserPolicyBasic(PriorityControlPolicy):
    """Basic policy in user prompt, unmarked constraints.
    Tests policy effectiveness in user prompt."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = f"When constraints conflict, follow the first constraint provided. {base_instruction} {constraint1} {constraint2}"
        return system_prompt, user_prompt

class MarkedUserPolicyBasic(PriorityControlPolicy):
    """Basic policy in user prompt, marked constraints.
    Tests marking effect in user prompt."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = f"When constraints conflict, follow Constraint 1 over Constraint 2. {base_instruction} Constraint 1: {constraint1} Constraint 2: {constraint2}"
        return system_prompt, user_prompt

class UnmarkedSystemPolicyDetailed(PriorityControlPolicy):
    """Detailed system policy, unmarked constraints.
    Tests explicit processing steps with original text."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = textwrap.dedent("""
            When processing multiple constraints:
            1. First constraint must be satisfied
            2. Second constraint only if compatible with first
            3. In conflicts, first constraint takes precedence
            """).strip()
        user_prompt = f"{base_instruction} {constraint1} {constraint2}"
        return system_prompt, user_prompt

class MarkedSystemPolicyDetailed(PriorityControlPolicy):
    """Detailed system policy, marked constraints.
    Tests if marking enhances detailed policy."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = textwrap.dedent("""
            When processing multiple constraints:
            1. Primary Constraint must be satisfied
            2. Secondary Constraint only if compatible with Primary
            3. In conflicts, Primary Constraint takes precedence
            """).strip()
        user_prompt = f"{base_instruction} Primary Constraint: {constraint1} Secondary Constraint: {constraint2}"
        return system_prompt, user_prompt

class UnmarkedUserPolicyDetailed(PriorityControlPolicy):
    """Detailed policy in user prompt, unmarked constraints.
    Tests detailed policy effectiveness in user location."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = textwrap.dedent(f"""
            When processing multiple constraints:
            1. First constraint must be satisfied
            2. Second constraint only if compatible with first
            3. In conflicts, first constraint takes precedence
            
            {base_instruction} {constraint1} {constraint2}
            """).strip()
        return system_prompt, user_prompt

class MarkedUserPolicyDetailed(PriorityControlPolicy):
    """Detailed policy in user prompt, marked constraints.
    Tests marking effect with detailed policy in user prompt."""
    
    def get_prompts(self, base_instruction: str, constraint1: str, constraint2: str, **kwargs) -> Tuple[str, str]:
        system_prompt = ""
        user_prompt = textwrap.dedent(f"""
            When processing multiple constraints:
            1. Primary Constraint must be satisfied
            2. Secondary Constraint only if compatible with Primary
            3. In conflicts, Primary Constraint takes precedence
            
            {base_instruction} Primary Constraint: {constraint1} Secondary Constraint: {constraint2}
            """).strip()
        return system_prompt, user_prompt