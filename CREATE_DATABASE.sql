CREATE TABLE camiones (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(20) UNIQUE NOT NULL,
    dispositivo_id VARCHAR(100)
);

CREATE TABLE sesiones (
    id SERIAL PRIMARY KEY,
    camion_id INT REFERENCES camiones(id),
    inicio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fin TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + interval '12 hours')
);

CREATE TABLE escaneos (
    id SERIAL PRIMARY KEY,
    sesion_id INT REFERENCES sesiones(id),
    punto VARCHAR(50) NOT NULL,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alertas (
    id SERIAL PRIMARY KEY,
    sesion_id INT REFERENCES sesiones(id),
    punto_saltado VARCHAR(50),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    correo_enviado BOOLEAN DEFAULT FALSE
);