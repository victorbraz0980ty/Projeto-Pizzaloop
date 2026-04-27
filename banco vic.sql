CREATE DATABASE IF NOT EXISTS pizzaloop;
USE pizzaloop;

-- 1. Criar produtos primeiro (para os pedidos poderem referenciar)
CREATE TABLE IF NOT EXISTS produtos (
    id_Produto INT NOT NULL AUTO_INCREMENT,
    nome_do_produto VARCHAR(100) NOT NULL,
    descricao_do_produto TEXT,
    preco_do_produto DECIMAL(10, 2) NOT NULL,
    categoria ENUM('Pizza', 'Bebida', 'Acompanhamento') NOT NULL,
    PRIMARY KEY (id_Produto)
);

-- 2. Criar clientes
CREATE TABLE IF NOT EXISTS cliente (
    id_cliente INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    telefone VARCHAR(11) NOT NULL,
    cep CHAR(8) NOT NULL,
    endereco VARCHAR(100) NOT NULL,
    cpf CHAR(12) NOT NULL,
    PRIMARY KEY (id_cliente)
);

-- 3. Criar pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedidos INT NOT NULL AUTO_INCREMENT,
    id_cliente INT,
    data_hora DATETIME NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    status_pedido ENUM('Em preparo', 'Saiu para entrega', 'Entregue') NOT NULL,
    PRIMARY KEY (id_pedidos),
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
);

-- 4. Criar itens (Agora ele acha o id_Produto lá de cima)
CREATE TABLE IF NOT EXISTS itens_pedidos (
    id_item INT NOT NULL AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    observacao TEXT,
    PRIMARY KEY (id_item),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedidos),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_Produto)
);    


create table if not exists funcionarios(
id_funcionarios int not null auto_increment,
nome varchar (100) not null,
cargo varchar (50) not null,
login varchar (50) unique not null,
senha_hash varchar (255) not null,
primary key (id_funcionarios)
);    


create table if not exists login(
id_login int not null auto_increment,
email varchar (150) not null,
senha varchar (30) not null,
primary key (id_login)
);  
