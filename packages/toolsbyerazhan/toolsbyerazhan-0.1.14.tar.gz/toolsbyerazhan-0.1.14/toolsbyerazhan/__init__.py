#from toolsbyerazhan import *#无效
#from toolsbyerazhan import timetools,gpu4tftools#有效

#可直接用timetools.py和gputools.py文件中的所有函数
#from .timetools import *
#from .gputools import *

__version__ = "0.1.14"

from . import gputools,jsontools,layers,models,ostools,timetools
from . import pandastools,tensorflowtools,transformers,xgboostools

from .gputools import set_gpu_memory_tf
set_gpu_memory_tf()
from .quicktools import whether_to_transfer
