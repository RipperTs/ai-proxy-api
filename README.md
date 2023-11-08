# 转发API (AI接口服务中间件)
> 类似`one-api`的项目,但是未作计费,仅做接口转发,支持多种第三方接口转发. 尽最大可能免去频繁适配第三方接口的烦恼.

## 项目初始化

- 安装依赖
```bash
pip install -r requirements.txt
```

- 初始化数据库
`data/init.sql` 文件为数据库初始化文件,请自行导入数据库

## 支持的第三方转发
- OhMyGPT [查看官网地址](https://www.ohmygpt.com/)

## 渠道类型说明
- 1: 原生OpenAI
- 2: OhMyGPT
- 3: 所有One-API程序转发的接口
- 4: OpenSB
- 5: 灵石-Qwen模型接口,包括(7b,14b,plus,turbo)

## 接口文档
- [查看接口文档](https://apifox.com/apidoc/shared-2c467c83-554d-4a60-b640-edbcc877f383)