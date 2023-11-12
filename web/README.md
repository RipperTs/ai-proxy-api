# AI接口转发前端项目

## 启动项目
```bash
# 安装依赖
npm install

# 运行服务
npm run serve

# 打包上传
npm run build
```

## Nginx伪静态示例
```
location /web/ {    
  proxy_pass http://127.0.0.1:3000/;
}
location /v1/ {    
  proxy_pass http://127.0.0.1:3000/v1/;
}
location / {
  try_files $uri $uri/ /index.html;
}

proxy_redirect off;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header Upgrade $http_upgrade;		# Websocket配置
proxy_set_header Connection $connection_upgrade;	
proxy_buffering off;
proxy_max_temp_file_size 0;
client_max_body_size 10m;
client_body_buffer_size 128k;
proxy_connect_timeout 90;
proxy_send_timeout 90;
proxy_read_timeout 90;
proxy_buffer_size 4k;
proxy_buffers 4 32k;
proxy_busy_buffers_size 64k;
proxy_temp_file_write_size 64k;

```
