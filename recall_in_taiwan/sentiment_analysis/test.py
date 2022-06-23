import numpy as np
# import pandas as pd
import warnings
from snownlp import SnowNLP

s = SnowNLP(
u"""
基本上，以前是定點在做公費快篩，那時候等於是定點監測計畫的一環，有五個計畫
，包括廢水計畫、血清計畫、機場監測及邊境食品監測等，那時候是一個計畫型的，所以到 6
月 30 日。現在快篩是普遍要使用，如果這些醫療機構覺得有必要繼續施行，我也不反對。因為
現在更廣泛、已經很廣泛，他們若要做，我們就繼續做。
""")
print( "{:.20f}".format(s.sentiments) )
