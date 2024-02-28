# Meta-Heuristic Optimization Tool for CVRP
Meta-Heuristic Optimization Tool is a comprehensive Python library tailored for solving complex Capacitated Vehicle Routing Problems (CVRP). It leverages various optimization techniques and heuristics to generate efficient routing plans that adhere to vehicle capacity constraints and customer demands.

## Features
- Custom Heuristics: Implements Nearest Neighbor and Hierarchical Clustering to generate initial feasible solutions.
- Optimization Techniques: Utilizes 2-opt, 3-opt, and Lin-Kernighan heuristics for route improvement.
- Flask Web Application: Comes with an integrated Flask app for visualizing routes and node distributions on maps.
- Scalability: Engineered to handle large datasets with thousands of nodes efficiently.
- Data Visualization: Supports various libraries like Matplotlib, Seaborn, and Plotly for insightful data analytics.
- Geographical Tools: Incorporates Folium for interactive map visuals, along with GeoPy and Shapely for geospatial analysis.

## Installation
To set up the Meta-Heuristic Optimization Tool, clone the repository and install the required dependencies.

```bash
git clone https://github.com/artuloda/meta-tool-test.git
cd meta-tool-test
pip install -r requirements.txt
```

## Flask Application
The tool includes a Flask web application for interactive visualization and management of routing solutions.
```python
# app.py
from flask import Flask, render_template, jsonify
import main

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/clientes')
def clientes():
    return render_template('clientes.html', data=main.nodes_df)

@app.route('/vehiculos')
def vehiculos():
    return render_template('vehiculos.html', vehicle_data=main.fleet_df)

@app.route('/mapa')
def mapa():
    return render_template('map.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/graph/data')
def graph_data():
    return jsonify(main.result_graph_json)

if __name__ == '__main__':
    nodes_df, fleet_df, result_df, result_graph_json = main.main()
    app.run()
````

To run the Flask application:
```bash
python app.py
```

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact
Arturo López Damas Oliveres  - @artuloda

Project Link: https://github.com/artuloda/meta-tool-test

## Acknowledgements
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [NumPy](https://numpy.org/doc/stable/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Scikit-Learn](https://scikit-learn.org/stable/auto_examples/index.html)
- [NetworkX](https://networkx.org/documentation/stable/reference/index.html)
- [Folium](https://python-visualization.github.io/folium/latest/user_guide.html)

