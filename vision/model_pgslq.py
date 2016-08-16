import psycopg2
import query_strings
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from main import app
builtin_list = list

db = SQLAlchemy()
def init_app(app):
    db.init_app(app)


class Node(db.Model):
    _tablename_ = 'node'

    node_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(255))
    contact_number = db.Column(db.String(255))
    address =  db.Column(db.String(255))
    purpose_description =  db.Column(db.String(255))
    isPlace =  db.Column(db.String(255))
    isBusTerminal =  db.Column(db.String(255))
    isRestRoom = db.Column(db.String(255))
    isIntersection = db.Column(db.String(255))
    latitude  =  db.Column(db.String(255))
    longitude =  db.Column(db.String(255))
    altitude =  db.Column(db.String(255))

    def __init__(self,name,contact_number,address,purpose_description, isPlace,isBusTerminal,isRestRoom,
                 isIntersection,latitude,longitude,altitude):
        self.name = name
        self.contact_number = contact_number
        self.address = address
        self.purpose_description = purpose_description
        self.isPlace = isPlace
        self.isBusTerminal = isBusTerminal
        self.isRestRoom = isRestRoom
        self.isIntersection = isIntersection
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def _repr_(self):
        return "<node_id: %s>" %(self.node_id)

    def get_node_json(self):
        return jsonify(node_id = self.node_id,
                       name = self.name,
                       contact_number = self.contact_number,
                       address = self.address,
                       purpose_description  = self.purpose_description,
                       isPlace = self.isPlace,
                       isBusTerminal = self.isBusTerminal,
                       isRestRoom = self.isRestRoom,
                       isIntersection = self.isIntersection,
                       latitude = self.latitude,
                       longitude = self.longitude,
                       altitude = self.altitude)

    def get_type(self):
        if(self.isPlace):
            return 0
        elif(self.isBusTerminal):
            return 1
        elif(self.isRestRoom):
            return 2
        elif(self.isIntersection):
            return 3
        else:
            return -1



def open_db_connection():
    connection = psycopg2.connect(
        database="map_dB",
        user="postgres",
        host="localhost"
    )
    return connection

def execute_cursor(cursor, string):
    cursor.execute(string)
    rows = cursor.fetchall()
    return rows

def close_db_connection(connection):
    connection.close()

def _to_dict_(row):
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

def get_test_path():

    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute(query_strings.DIJKSTRA)
    rows = cur.fetchall()
    conn.close()
    data = []
    for row1 in rows:
        data.append(dict(enumerate(row1)))
    return data

def get_path(source_id, target_id):
    conn = open_db_connection()
    cursor = conn.cursor()
    cursor.execute(query_strings.DIJKSTRA2, (source_id, target_id))
    rows = cursor.fetchall()
    conn.close()
    data = []
    for row in rows:
        data.append(dict(enumerate(row)))
    return data

def get_node_list(longitude, latitude, radius=200):
    connection=open_db_connection()
    cursor = connection.cursor()
    cursor.execute(query_strings.QUERY_NODES, (longitude, latitude, radius))
    rows = cursor.fetchall()
    connection.close()
    data = []
    for row in rows:
        data.append(dict(enumerate(row)))
    return data

def get_edge_list(longitude, latitude, radius=200):
    connection=open_db_connection()
    cursor = connection.cursor()
    cursor.execute(query_strings.QUERY_EDGES, (longitude, latitude, radius))
    rows = cursor.fetchall()
    connection.close()
    data = []
    for row in rows:
        data.append(dict(enumerate(row)))
    return data

def adjustEdgeWeight(edge_id, state=True):
    connection = open_db_connection()
    cursor = connection.cursor()
    cursor.execute(query_strings.UPDATE_EDGE_WEIGHT, (edge_id, state))
    rows = cursor.fetchall()
    connection.close()
    data = []
    for row in rows:
        data.append(dict(enumerate(row)))
    return data

def get_node_by_id(id):
    return  Node.query.get(id).get_node_json()



