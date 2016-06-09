/* Alters the table that contains the traffic counts for the edges of the graph
 * and appends a column that contains the line widths which are used by QGIS. 
 * The traffic count-range is normalized into the range of 0.5-5.0 which is a 
 * nice line width for QGIS. To change the normalization range, change these
 * numbers.
 */
ALTER TABLE visualization.bk_traffic ADD line_width real;

UPDATE visualization.bk_traffic AS a
SET line_width = c.line_width
FROM (
    SELECT edge_id, cnt, line_width
        FROM (
            SELECT edge_id, cnt, (0.5 + (cnt-mn.low)*(5.0-0.5)/(mx.up-mn.low)) line_width
            FROM visualization.bk_traffic, 
                (SELECT min(cnt) low
                FROM visualization.bk_traffic
                WHERE cnt > 0) mn,
                (SELECT max(cnt) up
                FROM visualization.bk_traffic
                WHERE cnt > 0) mx
              ) AS b
      ) AS c
WHERE a.edge_id = c.edge_id;

UPDATE visualization.bk_traffic
SET line_width = 0
WHERE line_width < 0.5;

