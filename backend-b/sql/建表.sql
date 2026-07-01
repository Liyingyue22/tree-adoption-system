-- 1. 创建并使用数据库
CREATE DATABASE TreeAdoptionDB;
GO
USE TreeAdoptionDB;
GO

-- 2. 创建公司主体表 (company)
CREATE TABLE company (
    companyId INT IDENTITY(1,1) PRIMARY KEY,
    companyName VARCHAR(100) NOT NULL,
    address VARCHAR(200),
    contactPhone VARCHAR(20),
    description VARCHAR(500)
);

-- 3. 创建用户表 (user)
CREATE TABLE [user] (
    userId INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(10) DEFAULT 'user'
);

-- 4. 创建树木表 (tree) - 新增了 companyId 外键
CREATE TABLE tree (
    treeId INT IDENTITY(1,1) PRIMARY KEY,
    companyId INT,                             -- 归属哪个公司
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

-- 5. 创建订单表 (tree_order)
CREATE TABLE tree_order (
    orderId INT IDENTITY(1,1) PRIMARY KEY,     
    userId INT NOT NULL,                       
    treeId INT NOT NULL,                       
    cycleMonth INT,                            
    createTime DATETIME DEFAULT GETDATE(),     
    FOREIGN KEY (userId) REFERENCES [user](userId),
    FOREIGN KEY (treeId) REFERENCES tree(treeId)
);

-- 6. 创建养护记录表 (maintenance_record)
CREATE TABLE maintenance_record (
    recordId INT IDENTITY(1,1) PRIMARY KEY,
    treeId INT NOT NULL,                       -- 哪棵树
    workerId INT NOT NULL,                     -- 哪个管理员操作的
    maintainType VARCHAR(50),                  -- 比如：浇水、施肥
    description VARCHAR(255),                  -- 具体情况说明
    photoUrl VARCHAR(255),                     -- 养护现场照片链接
    maintainTime DATETIME DEFAULT GETDATE(),   -- 养护时间
    FOREIGN KEY (treeId) REFERENCES tree(treeId),
    FOREIGN KEY (workerId) REFERENCES [user](userId)
);