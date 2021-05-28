import gspread
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np

gc = gspread.service_account(filename='/Users/Zeeshan/PycharmProjects/DashProjects/credentials.json')
sh = gc.open_by_key('1lS8M-wzWsBZke27JfBnTuZM--t7Lwvyg8hUqmk2L_aA')
worksheet = sh.get_worksheet(0)
res = worksheet.get_all_records()
df = pd.DataFrame(res)

app = dash.Dash(__name__)
# Proposal Shared Graph

df3 = df[['Account Manager', 'Proposal Shared', "Deal Size", "S_No", "Account Status"]]
df4 = df3.pivot_table(index=["Account Manager"], columns=["Proposal Shared"], values="S_No",
                      aggfunc="count").reset_index()
fig1 = px.bar(df4, x="Account Manager", y=["Yes", "No"], barmode="group")

# Deal Size Graph

deal_size = df3.loc[df3["Proposal Shared"] == "Yes"].set_index("S_No").fillna(0).reset_index()
df_dealsize = deal_size.pivot_table(index="Account Manager", columns="Account Status", values="Deal Size",
                                    aggfunc="sum").reset_index()
fig2 = px.bar(df_dealsize, x="Account Manager", y=["Closed", "Open"], barmode="group", text=(["Closed"], ["Open"]))

app.layout = html.Div(children=[
    html.H1(children='Telangana Dasboard'),
    dcc.Graph(
        id='Proposal_Shared',
        figure = fig1
    ),
    html.H1(children='Deal Size'),
    dcc.Graph(
        id='Deal_Size',
        figure=fig2
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)

