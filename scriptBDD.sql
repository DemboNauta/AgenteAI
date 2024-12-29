-- Crear la base de datos
CREATE DATABASE MobiliaAI;
GO

-- Usar la base de datos recién creada
USE MobiliaAI;
GO

-- Crear la tabla de Agentes
CREATE TABLE Agentes (
    IdAgente INT PRIMARY KEY IDENTITY(1,1), -- Identificador único, autoincremental
    Nombre NVARCHAR(100) NOT NULL,          -- Nombre del agente
    Correo NVARCHAR(100) NOT NULL,          -- Correo electrónico
    Telefono NVARCHAR(15) NULL              -- Número de teléfono (opcional)
);
GO

-- Insertar datos de ejemplo en la tabla de Agentes
INSERT INTO Agentes (Nombre, Correo, Telefono) VALUES
('Juan Pérez', 'juan.perez@inmobiliaria.com', '555-1234'),
('María Gómez', 'maria.gomez@inmobiliaria.com', '555-5678'),
('Carlos López', 'carlos.lopez@inmobiliaria.com', '555-8765'),
('Ana Martín', 'ana.martin@inmobiliaria.com', '555-4321'),
('Luis Torres', 'luis.torres@inmobiliaria.com', '555-1122'),
('Marta Díaz', 'marta.diaz@inmobiliaria.com', '555-3344'),
('Pedro Sánchez', 'pedro.sanchez@inmobiliaria.com', '555-5566'),
('Lucía Fernández', 'lucia.fernandez@inmobiliaria.com', '555-7788'),
('Jorge Ruiz', 'jorge.ruiz@inmobiliaria.com', '555-9900'),
('Elena Rojas', 'elena.rojas@inmobiliaria.com', '555-2244'),
('Diego Castro', 'diego.castro@inmobiliaria.com', '555-6688'),
('Laura Gil', 'laura.gil@inmobiliaria.com', '555-4422'),
('Sofía Vega', 'sofia.vega@inmobiliaria.com', '555-7766'),
('Tomás Herrera', 'tomas.herrera@inmobiliaria.com', '555-8822'),
('Isabel Molina', 'isabel.molina@inmobiliaria.com', '555-9988');
GO

-- Crear la tabla de Solicitudes
CREATE TABLE Solicitudes (
    IdSolicitud INT PRIMARY KEY IDENTITY(1,1), -- Identificador único, autoincremental
    IdAgente INT NOT NULL,                    -- Relación con la tabla de Agentes
    FechaSolicitud DATETIME NOT NULL DEFAULT GETDATE(), -- Fecha de la solicitud
    Descripcion NVARCHAR(500) NOT NULL,       -- Descripción de la solicitud
    FOREIGN KEY (IdAgente) REFERENCES Agentes(IdAgente) -- Clave foránea a la tabla de Agentes
);
GO

-- Insertar datos de ejemplo en la tabla de Solicitudes
INSERT INTO Solicitudes (IdAgente, Descripcion) VALUES
(1, 'Solicitud de compra de un apartamento en el centro.'),
(1, 'Solicitud de alquiler de una casa con jardín.'),
(2, 'Interesado en un local comercial en el sur de la ciudad.'),
(3, 'Búsqueda de una propiedad cerca de colegios.'),
(3, 'Compra de terreno para construir una casa.'),
(4, 'Solicitud de una propiedad en la playa.'),
(5, 'Interesado en un piso pequeño para estudiantes.'),
(6, 'Solicitud de un ático con terraza.'),
(7, 'Búsqueda de una oficina en el centro.'),
(8, 'Interesado en una casa de campo.'),
(9, 'Solicitud de alquiler de una propiedad temporal.'),
(10, 'Compra de un chalet con piscina.'),
(11, 'Interesado en un duplex moderno.'),
(12, 'Búsqueda de una propiedad para inversión.'),
(13, 'Solicitud de un local para restaurante.'),
(14, 'Interesado en un apartamento cerca del transporte público.'),
(15, 'Búsqueda de una propiedad con vistas al mar.');
GO

-- Crear la tabla de Propiedades
CREATE TABLE Propiedades (
    IdPropiedad INT PRIMARY KEY IDENTITY(1,1), -- Identificador único, autoincremental
    Direccion NVARCHAR(200) NOT NULL,         -- Dirección de la propiedad
    Precio DECIMAL(18, 2) NOT NULL,           -- Precio de la propiedad
    Habitaciones INT NOT NULL,                -- Número de habitaciones
    Banos INT NOT NULL,                       -- Número de baños
    Tamano INT NOT NULL,                      -- Tamaño en metros cuadrados
    Disponible BIT NOT NULL DEFAULT 1,        -- Disponibilidad de la propiedad
    IdAgente INT NOT NULL,                    -- Relación con la tabla de Agentes
    FOREIGN KEY (IdAgente) REFERENCES Agentes(IdAgente) -- Clave foránea a la tabla de Agentes
);
GO

-- Insertar datos de ejemplo en la tabla de Propiedades
INSERT INTO Propiedades (Direccion, Precio, Habitaciones, Banos, Tamano, IdAgente) VALUES
('Calle Mayor 123, Madrid', 250000.00, 3, 2, 120, 1),
('Avenida del Sol 45, Valencia', 320000.00, 4, 3, 150, 2),
('Plaza de la Luna 12, Sevilla', 200000.00, 2, 1, 80, 3),
('Calle de la Playa 1, Málaga', 450000.00, 5, 4, 200, 4),
('Calle Jardines 89, Granada', 180000.00, 3, 2, 100, 1),
('Calle del Comercio 56, Zaragoza', 300000.00, 4, 3, 140, 2),
('Avenida Principal 78, Bilbao', 400000.00, 5, 4, 220, 3),
('Calle Peatonal 34, Barcelona', 275000.00, 3, 2, 110, 4),
('Calle Nueva 89, Madrid', 150000.00, 2, 1, 70, 5),
('Paseo del Río 23, Sevilla', 360000.00, 4, 3, 160, 6),
('Plaza Mayor 56, Valencia', 290000.00, 3, 2, 130, 7),
('Calle Real 101, Granada', 310000.00, 4, 3, 140, 8),
('Avenida del Parque 12, Málaga', 500000.00, 6, 5, 250, 9),
('Calle Serena 8, Zaragoza', 220000.00, 3, 2, 90, 10),
('Calle Larga 43, Madrid', 190000.00, 2, 1, 85, 11);
GO

-- Verificar los datos
SELECT * FROM Agentes;
SELECT * FROM Solicitudes;
SELECT * FROM Propiedades;
GO
