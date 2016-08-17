import psycopg2
import query_strings
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import re

from datetime import datetime
# from main import app
builtin_list = list

db = SQLAlchemy()
def init_app(app):
    db.init_app(app)


class Node(db.Model):
    __tablename__ = "node"

    node_id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(255))
    phone_contact = db.Column(db.String(255))
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
        self.phone_contact = contact_number
        self.address = address
        self.purpose_description = purpose_description
        self.isPlace = isPlace
        self.isBusTerminal = isBusTerminal
        self.isRestRoom = isRestRoom
        self.isIntersection = isIntersection
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __repr__(self):
        return "<node_id: %s>" %(self.node_id)

    def to_json(self):
        return jsonify(node_id = self.node_id,
                       name = self.name,
                       contact_number = self.phone_contact,
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

class Edge(db.Model):
    __tablename__ = 'edge_data'

    edge_id =  db.Column(db.Integer(), primary_key=True)
    start_node = db.Column(db.Integer())
    end_node = db.Column(db.Integer())
    length = db.Column(db.String())
    reverse_length = db.Column(db.String())
    isRoad = db.Column(db.String())
    hasPedestrian =  db.Column(db.String())
    hasStreetConnect =  db.Column(db.String())
    isPassable =  db.Column(db.String())

    def __init__(self, edge_id, start_node, end_node,length,reverse_length, isRoad, hasPedestrian, hasStreetConnect,
                 isPassable):
        self.edge_id = edge_id
        self.start_node = start_node
        self.end_node  = end_node
        self.length =length
        self.reverse_length= reverse_length
        self.isRoad= isRoad
        self.hasPedestrian= hasPedestrian
        self.hasStreetConnect= hasStreetConnect
        self.isPassable= isPassable

    def __repr__(self):
        return "<start_node: %s, target_node: %s>" %(self.start_node, self.end_node)

    def to_json(self):
        return jsonify(
            edge_id = self.edge_id,
            start_node = self.start_node,
            end_node = self.end_node,
            length = self.length,
            reverse_length = self.reverse_length,
            isRoad = self.isRoad,
            hasPedestrian = self.hasPedestrian,
            hasStreetConnect = self.hasStreetConnect,
            isPassable = self.isPassable
        )
    def passable(self):
        self.isPassable = True

    def impassable(self):
        self.isPassable = False

    def is_passable(self):
        return self.isPassable

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
    return  Node.query.get(id).to_json()

def get_edge_by_id(id):
    return Edge.query.get(id).to_json()

def set_edge_passable(id, isPassable = True):
    edge = Edge.query.get(id)
    edge.isPassable = isPassable
    db.session.commit()




