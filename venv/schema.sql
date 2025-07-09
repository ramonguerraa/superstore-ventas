DROP TABLE IF EXISTS Calendario;

CREATE TABLE Calendario (
  Fecha TEXT,
  dia INTEGER,
  mes INTEGER,
  anio INTEGER,
  dia_semana TEXT,
  dia_semana_corto TEXT,
  num_dia_semana INTEGER,
  semana_anio INTEGER,
  mes_corto TEXT,
  trimestre INTEGER,
  semestre INTEGER
);

WITH RECURSIVE fechas(fecha) AS (
  SELECT DATE('2015-01-01')
  UNION ALL
  SELECT DATE(fecha, '+1 day')
  FROM fechas
  WHERE fecha < DATE('2018-12-31')
)
INSERT INTO Calendario (
  Fecha, dia, mes, anio, dia_semana, dia_semana_corto,
  num_dia_semana, semana_anio, mes_corto, trimestre, semestre
)
SELECT
  fecha,
  CAST(STRFTIME('%d', fecha) AS INTEGER),
  CAST(STRFTIME('%m', fecha) AS INTEGER),
  CAST(STRFTIME('%Y', fecha) AS INTEGER),
  CASE STRFTIME('%w', fecha)
    WHEN '0' THEN 'domingo' WHEN '1' THEN 'lunes' WHEN '2' THEN 'martes'
    WHEN '3' THEN 'miércoles' WHEN '4' THEN 'jueves' WHEN '5' THEN 'viernes'
    ELSE 'sábado' END,
  CASE STRFTIME('%w', fecha)
    WHEN '0' THEN 'dom' WHEN '1' THEN 'lun' WHEN '2' THEN 'mar'
    WHEN '3' THEN 'mié' WHEN '4' THEN 'jue' WHEN '5' THEN 'vie' ELSE 'sáb' END,
  CAST(STRFTIME('%w', fecha) AS INTEGER) + 1,
  CAST(STRFTIME('%W', fecha) AS INTEGER) + 1,
  SUBSTR('ene feb mar abr may jun jul ago sep oct nov dic', (CAST(STRFTIME('%m', fecha) AS INTEGER)-1)*4+1, 3),
  CASE 
    WHEN CAST(STRFTIME('%m', fecha) AS INTEGER) BETWEEN 1 AND 3 THEN 1
    WHEN CAST(STRFTIME('%m', fecha) AS INTEGER) BETWEEN 4 AND 6 THEN 2
    WHEN CAST(STRFTIME('%m', fecha) AS INTEGER) BETWEEN 7 AND 9 THEN 3
    ELSE 4 END,
  CASE 
    WHEN CAST(STRFTIME('%m', fecha) AS INTEGER) <= 6 THEN 1 ELSE 2 END
FROM fechas;

