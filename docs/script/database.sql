-- DROP DATABASE IF EXISTS autosolution;

CREATE DATABASE IF NOT EXISTS autosolution DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

USE autosolution;

-- change table column name
-- alter table case_lib change case_info case_info varchar(1024) null;
-- alter table case_lib change case_type case_type varchar(1024) null;

-- modify table column properties
-- ALTER TABLE case_lib MODIFY column case_info varchar(1024) NULL COMMENT '错误信息';
-- ALTER TABLE case_lib MODIFY column case_type varchar(256) NULL COMMENT '错误类型';
CREATE TABLE IF NOT EXISTS `case_lib` (
    `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT 'id',
    `case_key` varchar(256) NOT NULL COMMENT '关键字',
    `case_info` varchar(1024) COMMENT '错误信息',
    `case_type` varchar(256) COMMENT '错误类型',
    `case_description` varchar(1024) COMMENT '错误描述',
    `case_solution` varchar(1024) COMMENT '解决方案（推荐）',
    `case_remark` varchar(512) COMMENT '备注'
);

INSERT INTO case_lib(case_key, case_info, case_type, case_description, case_solution, case_remark) VALUES(
    'case_key1',
    'case_info1',
    'case_type1',
    'case_description1',
    'case_solution1',
    'case_remark1'
);

INSERT INTO case_lib(case_key, case_info, case_type, case_description, case_solution, case_remark) VALUES(
    'case_key2',
    'case_info2',
    'case_type2',
    'case_description2',
    'case_solution2',
    'case_remark2'
);

INSERT INTO case_lib(case_key, case_info, case_type, case_description, case_solution, case_remark) VALUES(
    'case_key3',
    'case_info3',
    'case_type3',
    'case_description3',
    'case_solution3',
    'case_remark3'
);


CREATE TABLE IF NOT EXISTS `build_info` (
    `id` int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT COMMENT 'id',
    `job_name` varchar(256) NOT NULL COMMENT '工程名',
    `build_number` varchar(1024) NOT NULL COMMENT '构建编号',
    `build_url` varchar(256) UNIQUE NOT NULL COMMENT '构建地址',
    `recipients` varchar(1024) COMMENT '邮件接收人',
    `err_info` varchar(1024) COMMENT '错误信息',
    `err_key` varchar(512) COMMENT '错误关键字'
);
