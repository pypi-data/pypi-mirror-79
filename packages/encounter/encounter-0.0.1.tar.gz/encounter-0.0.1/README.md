
SQL Cheatsheet



Find all the aicraft on a particular hour over Haight St, San Fran:

.. code-block:: SQL

    select * from state_vectors_data4 where hour=1480759200 and lat > 38.0000 and lat < 39.0000 and lon > -123.0000 and lon < -122.0000;


Count all the timestamps in the same location but over about a week:

.. code-block:: SQL

    SELECT COUNT(*) FROM state_vectors_data4 WHERE hour>=1598918400 AND hour<=1599523200  and lat > 38.0000 and lat < 39.0000 and lon > -123.0000 and lon < -122.0000;


Count aircraft which arrived or departed or crossed Frankfurt airport during a certain hour:

.. code-block:: SQL 

    SELECT COUNT(DISTINCT icao24) FROM state_vectors_data4 WHERE lat<=50.07 AND lat>=49.98 AND lon<=8.62 AND lon>=8.48 AND hour=1493892000;