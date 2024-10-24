import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Load the dataset
penguins_df = pd.read_csv('penguins.csv')

# Create a Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Palmer Penguins Dataset Exploration"), className="text-center mb-4")
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("Select Feature"),
                    dbc.CardBody([
                        dcc.Dropdown(
                            id='feature-dropdown',
                            options=[{'label': col, 'value': col} for col in penguins_df.columns if col != 'species'],
                            value='bill_length_mm'
                        ),
                    ])
                ]),
                width=3
            ),
            dbc.Col(
                [
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{"name": i, "id": i} for i in penguins_df.columns],
                        data=penguins_df.to_dict('records'),
                        page_size=10,
                    ),
                    dcc.Graph(id='main-chart')
                ],
                width=9
            )
        ]
    )
])

@app.callback(
    dash.dependencies.Output('main-chart', 'figure'),
    dash.dependencies.Input('feature-dropdown', 'value')
)
def update_chart(selected_feature):
    fig = px.histogram(penguins_df, x=selected_feature, nbins=30, color='species', title=f'Distribution of {selected_feature}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



