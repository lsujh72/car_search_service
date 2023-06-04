SQL_QUERY = """
                SELECT ca.description, ca.weight, l_1.lat lat_1, l_1.lng lng_1, 
                l_2.lat lat_2, l_2.lng lng_2
                FROM cargo ca 
                JOIN location l_1 ON l_1.id=ca.location_pick_up_id
                JOIN location l_2 ON l_2.id=ca.location_delivery_id
            """


SQL_QUERY_RANDOM_LOCATION = """
                                SELECT id FROM location ORDER BY RANDOM();
                            """
