DROP FUNCTION IF EXISTS basic.station_route_count;
CREATE OR REPLACE FUNCTION basic.station_route_count(
	table_area TEXT, 
	where_filter TEXT,
	start_time interval,
	end_time interval,
	weekday integer
)
RETURNS TABLE(stop_id text, stop_name text, access_time smallint, trip_cnt jsonb, geom geometry, route_ids jsonb, h3_3 integer)
LANGUAGE plpgsql
AS $function$
DECLARE
	temp_table_stops TEXT := 'temporal.' || '"' || REPLACE(uuid_generate_v4()::TEXT, '-', '') || '"';
	temp_table_area TEXT := 'temporal.' || '"' || REPLACE(uuid_generate_v4()::TEXT, '-', '') || '"'; 
BEGIN

	-- Build table reference area
	-- PERFORM basic.create_distributed_polygon_table
	-- (
	--	table_area,
	--	'id',
	--	where_filter,
	--	30, 
	--	temp_table_area
	-- ); 
	
	-- Create temporary table and execute dynamic SQL
	EXECUTE format(
		'DROP TABLE IF EXISTS %s;
		CREATE TABLE %s
		(
			stop_id text,
			access_time smallint,
			h3_3 integer
		);', temp_table_stops, temp_table_stops
	);
	-- Distribute the table with stops
	PERFORM create_distributed_table(temp_table_stops, 'h3_3');

	-- Get relevant stations
	EXECUTE format(
		'INSERT INTO %s
		SELECT st.stop_id, b.integer_attr1, st.h3_3
		FROM basic.stops_v2 st, %s b
		WHERE ST_Intersects(st.geom, b.geom)
		AND (st.location_type IS NULL OR st.location_type = ''0'')',
		temp_table_stops, table_area
	);

	-- Count trips per station and transport mode in respective time interval
	RETURN QUERY EXECUTE format(
		'WITH route_cnt AS
		(
			SELECT c.stop_id, c.access_time, j.route_type, cnt AS cnt, j.route_ids, c.h3_3
			FROM %s c
			CROSS JOIN LATERAL (
				SELECT t.route_type, SUM(weekdays[$1]::integer) cnt, ARRAY_AGG(route_id) AS route_ids
				FROM basic.stop_times_optimized t, basic.stops_v2 s
				WHERE t.stop_id = s.stop_id
				AND s.stop_id = c.stop_id
				AND s.h3_3 = c.h3_3
				AND t.h3_3 = s.h3_3
				AND t.arrival_time BETWEEN $2 AND $3
				AND weekdays[$4] = True
				GROUP BY t.route_type
			) j
		),
		o AS (
			SELECT stop_id, access_time, jsonb_object_agg(route_type, cnt) AS route_cnt, jsonb_object_agg(route_type, g.route_ids) AS route_ids, h3_3
			FROM route_cnt g
			WHERE cnt <> 0
			GROUP BY stop_id, access_time, h3_3
		)
		SELECT s.stop_id, s.stop_name, o.access_time, o.route_cnt, s.geom, o.route_ids, o.h3_3
		FROM o, basic.stops_v2 s
		WHERE o.stop_id = s.stop_id
		AND s.h3_3 = o.h3_3', temp_table_stops) USING weekday, start_time, end_time, weekday;

	-- Drop the temporary table
	EXECUTE format(
		'DROP TABLE IF EXISTS %s; DROP TABLE IF EXISTS %s;',
		temp_table_stops, temp_table_area
	);
END;
$function$
PARALLEL SAFE;
/*
SELECT *
FROM basic.station_route_count('06:00','20:00', 1, 'SELECT geom
FROM user_data.polygon_744e4fd1685c495c8b02efebce875359') s
*/