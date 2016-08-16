DIJKSTRA = "with temp_data as ( select seq, id1 from pgr_dijkstra( 'select edge_id as id, start_node::integer as source, end_node::integer as target, length::double precision as cost, reverse_length::double precision as reverse_cost from topo.edge_data', 10, 20, false, true ) ) select seq, node_id, name, latitude, longitude from temp_data,topo.node where topo.node.node_id = temp_data.id1;"

DIJKSTRA2 = "with temp_data as ( select seq, id1 from pgr_dijkstra( 'select edge_id as id, start_node::integer as " \
             "source, end_node::integer as target, length::double precision as cost, reverse_length::double precision as reverse_cost from topo.edge_data', (%s), (%s), false, true ) ) select seq, node_id, name, latitude, longitude from temp_data,topo.node where topo.node.node_id = temp_data.id1;"

QUERY_NODES = 'SELECT * FROM topo.node WHERE ST_Distance_Sphere(geom, ST_MakePoint(%s,%s)) <= %s;'

QUERY_EDGES = 'SELECT * FROM topo.edge_data WHERE ST_Distance_Sphere(geom, ST_MakePoint(%s,%s)) <= 200;'

UPDATE_EDGE_WEIGHT = 'update topo.edge_data set "isPassable"= %s where edge_id = %s;'