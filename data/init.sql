create table abilities
(
    model_name varchar(100) default '' null comment '模型名称',
    channel_id int          default 0  null comment '渠道ID',
    enabled    tinyint(1)   default 1  null comment '是否启用'
)
    comment '渠道模型';

create table channels
(
    id                  int auto_increment
        primary key,
    type                tinyint(3)   default 1   null comment '渠道类型',
    `key`               varchar(255) default ''  null comment '鉴权秘钥',
    status              tinyint(3)   default 1   null comment '渠道状态,1启用,2禁用',
    name                varchar(100) default ''  null comment '渠道名称',
    weight              int          default 100 null comment '权重',
    created_time        datetime                 null comment '创建时间',
    test_time           datetime                 null comment '测试时间',
    response_time       int          default 0   null comment '响应时长(ms)',
    base_url            varchar(255) default ''  null comment '请求url',
    balance             int          default 0   null comment '渠道余额(分)',
    balance_update_time datetime                 null comment '渠道余额更新时间',
    models              longtext                 null comment '允许使用的模型列表',
    used_quota          int          default 0   null comment '总请求次数'
)
    comment '渠道表';

create table logs
(
    id             int auto_increment
        primary key,
    type           tinyint(3)   default 1  null comment '类型,1消耗,2增加',
    content        varchar(255) default '' null comment '日志内容',
    token_name     varchar(100) default '' null,
    model_name     varchar(100) default '' null comment '模型名称',
    request_tokens int          default 0  null comment '请求消耗tokens',
    channel_id     int          default 0  null comment '渠道ID',
    channel_name   varchar(100) default '' null comment '渠道名称',
    created_time   datetime                null
)
    comment '请求日志';

create table tokens
(
    id           int auto_increment
        primary key,
    user_id      int          default 0  null,
    `key`        varchar(255) default '' null,
    status       tinyint(3)   default 1  null,
    name         varchar(50)  default '' null,
    created_time datetime                null,
    expired_time datetime                null comment '过期时间'
)
    comment '令牌列表';

create table users
(
    id           int auto_increment
        primary key,
    username     varchar(100) default '' null comment '用户名称',
    email        varchar(100) default '' null comment '邮箱',
    password     varchar(255)            null comment '密码',
    status       tinyint(3)   default 1  null comment '状态',
    created_time datetime                null,
    constraint users_pk2
        unique (email)
)
    comment '用户表';

