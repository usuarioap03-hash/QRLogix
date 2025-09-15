CREATE OR REPLACE VIEW vista_resumen AS
SELECT
    c.id AS id_camion,
    DATE(e.fecha_hora) AS fecha,
    c.placa,
    TO_CHAR(MAX(CASE WHEN LOWER(e.punto) = 'punto1' THEN e.fecha_hora END), 'HH12:MI:SS AM') AS punto1,
    TO_CHAR(MAX(CASE WHEN LOWER(e.punto) = 'punto2' THEN e.fecha_hora END), 'HH12:MI:SS AM') AS punto2,
    TO_CHAR(MAX(CASE WHEN LOWER(e.punto) = 'punto3' THEN e.fecha_hora END), 'HH12:MI:SS AM') AS punto3,
    TO_CHAR(MAX(CASE WHEN LOWER(e.punto) = 'punto4' THEN e.fecha_hora END), 'HH12:MI:SS AM') AS punto4
FROM escaneos e
JOIN sesiones s ON e.sesion_id = s.id
JOIN camiones c ON s.camion_id = c.id
GROUP BY c.id, DATE(e.fecha_hora), c.placa
ORDER BY fecha DESC;
