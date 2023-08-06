import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from src.simple_chart import Simple_chart

simple = Simple_chart('BBCA.JK')
df = simple.ingest()
df = simple.set_ma(100)

print(df.tail())

simple.visualize(df,
                ['Open', 'Close'])