CREATE TABLE IF NOT EXISTS camiones (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    dispositivo_id VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS sesiones (
    id SERIAL PRIMARY KEY,
    camion_id INT REFERENCES camiones(id) ON DELETE CASCADE,
    inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fin TIMESTAMP NOT NULL  -- calculado desde Python
);

CREATE TABLE IF NOT EXISTS escaneos (
    id SERIAL PRIMARY KEY,
    sesion_id INT REFERENCES sesiones(id) ON DELETE CASCADE,
    punto VARCHAR(50) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Placas autorizadas (lista blanca)
CREATE TABLE IF NOT EXISTS placas_autorizadas (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL
);

-- Dispositivos autorizados vinculados a una placa
CREATE TABLE IF NOT EXISTS dispositivos_autorizados (
    id SERIAL PRIMARY KEY,
    dispositivo_id VARCHAR(128) UNIQUE NOT NULL,
    placa VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_dispositivos_autorizados_placa 
    ON dispositivos_autorizados (placa);

CREATE INDEX IF NOT EXISTS idx_placas_autorizadas_placa 
    ON placas_autorizadas (placa);
