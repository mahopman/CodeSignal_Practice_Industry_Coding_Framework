import json
import math
import string
import re
import random
import sys
import traceback
import functools
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
from decimal import Decimal, ROUND_HALF_UP

import numpy
import sortedcontainers

def simulate_banking_system(operations_list):
    """
    Simulates a banking system with various operations.
    
    Parameters:
    operations_list (List[List[str]]): A list of operations to perform.
    
    Expected operations include:
    - CREATE_ACCOUNT, CREATE_ACCOUNT_AT
    - GET_BALANCE, GET_BALANCE_AT  
    - DEPOSIT, DEPOSIT_AT
    - WITHDRAW, WITHDRAW_AT
    - TRANSFER, TRANSFER_AT
    - FREEZE_ACCOUNT, FREEZE_ACCOUNT_AT
    - UNFREEZE_ACCOUNT, UNFREEZE_ACCOUNT_AT
    
    Returns:
    List[str]: Results of each operation
    """
    pass