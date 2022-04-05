import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from umap import UMAP


app = Dash(__name__)
app.title = "UMAP Projections"

app.layout = html.Div(
    [
        html.Div(
            children=[
                html.H1(
                    "UMAP Projections for MNIST and Fashion-MNIST Datasets",
                    style={"text-align": "center"},
                ),
                dcc.Markdown(
                    """
                    Test change. Uniform Manifold Approximation and Projection (UMAP) is a general-purpose dimension reduction algorithm. Similar to t-distributed stochastic neighbor embedding (t-SNE), you can use UMAP to visualize the relationships between data points. In this example, we are training a three-component UMAP model on MNIST datasets and then displaying the 3D graph of the result. The color of the point in the graph is based on the label. In the resulting graph, blobs of colors show that UMAP clustered data points with similar labels together.
                """,
                ),
            ],
            style={"padding": 10},
        ),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H1("Input"),
                        html.Label("Dataset"),
                        dcc.Dropdown(
                            ["MNIST-Digits", "MNIST-Fashion"], "MNIST-Digits", id="dataset_dropdown"
                        ),
                    ],
                    style={"padding": 10, "flex": 1},
                ),
                html.Div(
                    children=[
                        html.H1("Output"),
                        dcc.Loading(
                            id="loading-1",
                            children=[dcc.Graph(id="graph")],
                            type="circle",
                        ),
                    ],
                    style={"padding": 10, "flex": 3},
                ),
            ],
            style={"display": "flex", "flex-direction": "row"},
        ),
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("dataset_dropdown", "value"),
)
def update_figure(selected_dataset):
    if selected_dataset == "MNIST-Digits":
        X = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/mnist-1000-input.csv"
        )
        y = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/mnist-1000-labels.csv"
        )
        y = np.unique(y, return_inverse=True)[1]

    elif selected_dataset == "MNIST-Fashion":
        X = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/fashion-1000-input.csv"
        )
        y = pd.read_csv(
            "https://saturn-public-data.s3.us-east-2.amazonaws.com/MNIST-1000/fashion-1000-labels.csv"
        )
        y = np.unique(y, return_inverse=True)[1]

    else:
        return None, "Please select a dataset."

    umap_3d = UMAP(n_components=3, init="random", random_state=0)

    proj_3d = umap_3d.fit_transform(X, y=y)

    fig = px.scatter_3d(proj_3d, x=0, y=1, z=2, color=y)

    fig.update_layout(transition_duration=500, height=1000)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(marker_size=2)

    return fig


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8000")
