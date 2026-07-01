-- 注意：本脚本会删除旧数据库 TreeAdoptionDB，适合演示或测试环境。
IF DB_ID('TreeAdoptionDB') IS NOT NULL
BEGIN
    ALTER DATABASE TreeAdoptionDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE TreeAdoptionDB;
END
GO

CREATE DATABASE TreeAdoptionDB;
GO
USE TreeAdoptionDB;
GO

CREATE TABLE company (
    companyId INT IDENTITY(1,1) PRIMARY KEY,
    companyName VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    contactPhone VARCHAR(20),
    description VARCHAR(500)
);

CREATE TABLE [user] (
    userId INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(10) DEFAULT 'user'
);

CREATE TABLE tree (
    treeId INT IDENTITY(1,1) PRIMARY KEY,
    companyId INT,
    treeType VARCHAR(50) NOT NULL,
    position VARCHAR(100),
    price DECIMAL(10, 2),
    status INT DEFAULT 0,
    coverImg VARCHAR(255),
    cameraSn VARCHAR(50),
    cameraIp VARCHAR(50),
    camUser VARCHAR(50),
    camPwd VARCHAR(50),
    FOREIGN KEY (companyId) REFERENCES company(companyId)
);

CREATE TABLE tree_order (
    orderId INT IDENTITY(1,1) PRIMARY KEY,
    userId INT NOT NULL,
    treeId INT NOT NULL,
    cycleMonth INT,
    createTime DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (userId) REFERENCES [user](userId),
    FOREIGN KEY (treeId) REFERENCES tree(treeId)
);

CREATE TABLE maintenance_record (
    recordId INT IDENTITY(1,1) PRIMARY KEY,
    treeId INT NOT NULL,
    workerId INT NOT NULL,
    maintainType VARCHAR(50),
    description VARCHAR(255),
    photoUrl VARCHAR(255),
    maintainTime DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (treeId) REFERENCES tree(treeId),
    FOREIGN KEY (workerId) REFERENCES [user](userId)
);
GO

INSERT INTO company(companyName, address, contactPhone, description) VALUES
('阳光生态农场', '一号农田 A 区', '0571-88886666', '提供果树与景观树认养服务'),
('青禾农业公司', '二号农田 B 区', '0571-66668888', '负责农田养护和摄像头监控'),
('绿源果园基地', '三号果园 C 区', '0571-99990000', '提供果树长期认养服务');

INSERT INTO [user](username, password, phone, role) VALUES
('admin01', '123456', '13900000001', 'admin'),
('test01', '123456', '13800138001', 'user'),
('test02', '123456', '13800138002', 'user');

INSERT INTO tree(companyId, treeType, position, price, status, coverImg, cameraSn, cameraIp, camUser, camPwd) VALUES
(1, '香樟树', '一号农田 A 区 001', 200.00, 1, '/tree/demo.svg', 'GU0249887', '192.168.1.101', 'admin', '123456'),
(1, '桂花树', '一号农田 A 区 002', 180.00, 0, '/tree/demo.svg', 'CAM-A002', '192.168.1.102', 'admin', '123456'),
(1, '银杏树', '一号农田 A 区 003', 260.00, 0, '/tree/demo.svg', 'CAM-A003', '192.168.1.103', 'admin', '123456'),
(2, '桃树',   '二号农田 B 区 001', 300.00, 1, '/tree/demo.svg', 'CAM-B001', '192.168.1.111', 'admin', '123456'),
(2, '梨树',   '二号农田 B 区 002', 280.00, 0, '/tree/demo.svg', 'CAM-B002', '192.168.1.112', 'admin', '123456'),
(3, '苹果树', '三号果园 C 区 001', 320.00, 0, '/tree/demo.svg', 'CAM-C001', '192.168.1.121', 'admin', '123456'),
(3, '柿子树', '三号果园 C 区 002', 220.00, 0, '/tree/demo.svg', 'CAM-C002', '192.168.1.122', 'admin', '123456');

INSERT INTO tree_order(userId, treeId, cycleMonth) VALUES
(2, 1, 12),
(3, 4, 6);

INSERT INTO maintenance_record(treeId, workerId, maintainType, description, photoUrl) VALUES
(1, 1, '浇水', '完成本周浇水，树木状态良好', '/cap/demo.svg'),
(1, 1, '施肥', '完成有机肥补充', '/cap/demo.svg'),
(4, 1, '修剪', '修剪枯枝，保持树形', '/cap/demo.svg');
GO
