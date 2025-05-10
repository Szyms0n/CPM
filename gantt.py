import pandas as pd
import plotly.express as px
from Node import node_tab
from datetime import timedelta, datetime


start_date = datetime.today()

#  dane do wykresu Gantta
records = []
for node in node_tab:
    start = start_date + timedelta(days=int(node.ES))
    end = start_date + timedelta(days=int(node.EF))
    records.append(dict(Task=node.name, Start=start, Finish=end))

# DataFrame i wykres
df = pd.DataFrame(records)
fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
fig.update_yaxes(autorange="reversed")
fig.update_layout(title="Wykres Gantta - CPM")

# zapis do pliku HTML
fig.write_html("gantt.html")
print("Wykres Gantta zapisany jako gantt.html")
