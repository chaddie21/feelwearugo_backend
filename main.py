# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, jsonify, request
from vision import model_pgslq
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)



model = model_pgslq

@app.route('/')
def index():
        # conn = model.open_db_connection()
        # cur = conn.cursor()
        # cur.execute(query_strings.DIJKSTRA)
        # rows = cur.fetchall()
        # conn.close()
        # data = []
        # for row1 in rows:
        #         data.append(dict(enumerate(row1)))
        #
        # return jsonify(nodes=data)
        nodes = model.get_test_path()
        return jsonify(nodes=nodes)


@app.route('/path/', methods=['GET'])
def get_path():
    source_id = request.args.get("a")
    target_id = request.args.get("b")
    data=model.get_path(source_id=source_id, target_id=target_id)
    return jsonify(nodes=data)


@app.route('/nodes/', methods=['GET'])
def get_nodes():
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")
    radius = request.args.get("radius")
    data=model.get_node_list(longitude=longitude, latitude=latitude, radius=2000)
    return jsonify(nodes=data)


@app.route('/edges/', methods=['GET'])
def get_edges():
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")
    data = model.get_node_list(longitude=longitude, latitude=latitude, radius=200)
    return jsonify(edges=data)


@app.route('/adj/', methods=['POST'])
def adj_edge():
    id = request.args.get("a")
    state = request.args.get("b")
    model.adjustEdgeWeight(edge_id=id, state=state)

@app.route('/node/', methods=['GET'])
def get_node():
    id = request.args.get("a")
    return  model.get_node_by_id(id)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)