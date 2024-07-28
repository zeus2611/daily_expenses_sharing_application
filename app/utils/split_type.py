"""
app/utils/split_type.py
This module contains an enum class representing the types of expense splits.
"""

import enum

class SplitTypeEnum(enum.Enum):
    """
    Enum class representing the types of expense splits.
    
    Attributes:
        EQUAL: Represents an equal split among participants.
        EXACT: Represents an exact split where each participant pays a specific amount.
        PERCENTAGE: Represents a split based on percentages assigned to each participant.
    """
    EQUAL = "EQUAL"
    EXACT = "EXACT"
    PERCENTAGE = "PERCENTAGE"