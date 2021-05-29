import gspread
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input , Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import dash_bootstrap_components as dbc
import base64

import numpy as np

gc = gspread.service_account(filename='/Users/Zeeshan/PycharmProjects/DashProjects/credentials.json')
sh = gc.open_by_key('1UzKPiujJH97PLV7R4h4orp6ZeUPG8-W2vncsu1TunSA')
worksheet = sh.get_worksheet(0)
df = pd.DataFrame(worksheet.get_all_records())
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
image_filename = '/Users/Zeeshan/PycharmProjects/DashProjects/Collegedunia Logo.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = dbc.Container([
    dbc.Row([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'height':'20%', 'width':'20%'}),
        dbc.Col(html.H1("Telangana Dashboard",
                className="text-center text-primary,mb-4"),width=12)
        ]),
    dbc.Row([
        dbc.Col([
            html.H3("Proposal Shared"),
            dcc.Dropdown(
                id="AM_DD", multi=True,value=["Zeeshan","Rashika"],options=[{'label':x , "value": x}
                                                          for x in sorted(df["Account Manager"].unique())]
                ),
            dcc.Graph(
                id="Proposal_Shared",
                figure={}
                )
            ]),
        dbc.Col([
            html.H3("Deal Size"),
            dcc.Dropdown(
                id="AM_D2", multi=True,value=["Zeeshan","Rashika"],options=[{'label':x , "value": x}
                                                          for x in sorted(df["Account Manager"].unique())]
                ),
            dcc.Graph(
                id="Deal_Size",
                figure={}
                )
            ]),

        ],),

],fluid=True)

@app.callback(
    Output("Proposal_Shared","figure"),
    Input("AM_DD","value")
)
def update_graph(name):
        df = pd.DataFrame(worksheet.get_all_records())
        df3 = df[['Account Manager', 'Proposal Shared', "Deal Size", "S_No", "Account Status"]]
        df4 = df3.pivot_table(index=["Account Manager"], columns=["Proposal Shared"], values="S_No",
                              aggfunc="count").reset_index()
        df5=df4[df4["Account Manager"].isin(name)]
        fig1 = px.bar(df5, x="Account Manager", y=["Yes", "No"], barmode="group")
        return fig1

     # Deal Size Graph
@app.callback(
    Output("Deal_Size", "figure"),
    Input("AM_D2", "value")
)
def update_graph(name):
        dff = pd.DataFrame(worksheet.get_all_records())
        df6 = dff[['Account Manager', 'Proposal Shared', "Deal Size", "S_No", "Account Status"]]
        deal_size = df6.loc[df6["Proposal Shared"] == "Yes"].set_index("S_No").fillna(0).reset_index()
        df_dealsize = deal_size.pivot_table(index="Account Manager", columns="Account Status", values="Deal Size",
                                            aggfunc="sum").reset_index()
        df_dealsize_final = df_dealsize[df_dealsize["Account Manager"].isin(name)]
        fig2 = px.bar(df_dealsize_final, x="Account Manager", y=["Closed", "Open"], barmode="group")
        return fig2


if __name__ == '__main__':
    app.run_server(debug=True, port =8051)
