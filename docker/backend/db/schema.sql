CREATE TABLE Usuario (
    IdUsuario INT PRIMARY KEY IDENTITY(1,1),
    Nombres NVARCHAR(50) NOT NULL,
    Apellido NVARCHAR(50) NOT NULL,
    Correo NVARCHAR(50) UNIQUE NOT NULL,
    Celular NVARCHAR(15) NOT NULL,
    Clave NVARCHAR(50) NOT NULL
);

CREATE TABLE Boleta (
    IdBoleta INT PRIMARY KEY IDENTITY(1,1),
    FechaBoleta DATE NOT NULL,
    IdUsuario INT,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);

CREATE TABLE Productos (
    IdProducto INT PRIMARY KEY IDENTITY(1,1),
    Nombre NVARCHAR(50) NOT NULL,
    Cantidad INT,
    Categoria NVARCHAR(50) NOT NULL,
    PorcentajeConsumo INT,
    FechaVencimiento DATE,
    Costo FLOAT,
    IdBoleta INT,
    FOREIGN KEY (IdBoleta) REFERENCES Boleta(IdBoleta)
);

CREATE TABLE RecEnfermedades (
    IdRE INT PRIMARY KEY IDENTITY(1,1),
    Detalle NVARCHAR(3000) NOT NULL,
    FechaRecomendacion DATE,
    IdUsuario INT,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);

CREATE TABLE RecAlimentarias (
    IdRA INT PRIMARY KEY IDENTITY(1,1),
    Detalle NVARCHAR(3000) NOT NULL,
    FechaRecomendacion DATE,
    IdUsuario INT,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);

CREATE TABLE RecPrecedentes (
    IdRP INT PRIMARY KEY IDENTITY(1,1),
    Detalle NVARCHAR(3000) NOT NULL,
    IdUsuario INT,
    FOREIGN KEY (IdUsuario) REFERENCES Usuario(IdUsuario)
);
