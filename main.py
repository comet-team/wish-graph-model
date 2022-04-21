import pandas as pd

a = pd.DataFrame({'a':[1,2,2,3], 'b' : [55, 66, 4, 77]})
print(pd.unique(a['a']))