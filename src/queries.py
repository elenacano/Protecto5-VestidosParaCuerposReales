querie_creacion_marcas = """create table if not exists marcas (
                            id_marca SERIAL primary key,
                            nombre varchar(100) unique not null);"""

querie_creacion_categorias = """create table if not exists categorias (
                            id_categoria SERIAL primary key,
                            nombre varchar(100) unique not null);"""


querie_creacion_vestidos = """create table if not exists vestidos (
                            id_vestido SERIAL primary key,
                            nombre varchar(500) not null,
                            id_marca int not null,
                            precio numeric not null,
                            color varchar(200),
                            talla varchar(10) not null,
                            id_categoria int not null,
                            foreign key (id_marca) references marcas(id_marca) on delete restrict on update cascade,
                            foreign key (id_categoria) references categorias(id_categoria) on delete restrict on update cascade);"""

querie_creacion_vestidos_forever21 = """create table if not exists vestidos_forever21 (
                            id_vestido_f21 SERIAL primary key,
                            nombre varchar(500) not null,
                            id_marca int not null,
                            precio numeric not null,
                            color varchar(200),
                            talla varchar(10) not null,
                            stock int,
                            id_categoria int not null,
                            foreign key (id_marca) references marcas(id_marca) on delete restrict on update cascade,
                            foreign key (id_categoria) references categorias(id_categoria) on delete restrict on update cascade);"""


query_carga_marcas = """INSERT INTO marcas (nombre)  VALUES (%s)""" 

query_carga_categorias = """INSERT INTO categorias (nombre)  VALUES (%s)""" 


