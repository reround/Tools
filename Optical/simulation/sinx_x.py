
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objects as go

x = np.linspace(-100, 100, 10000)

y = 10*np.log10(np.sin(x)/x)


fig = go.Figure()

fig.add_trace(go.Scatter(x=x,y=y,name='lines'))
fig.update_yaxes(
    title={'font': {'size': 18}, 'text': '归一化天线方向 /dB', 'standoff': 10}
)
fig.update_xaxes(
    title = {'font': {'size': 18},'text' : '角度 / rad'}
)
fig.show()
