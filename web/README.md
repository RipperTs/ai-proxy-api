# AI接口转发前端项目

## Nginx伪静态示例
```
location /web/ {    
  proxy_pass http://127.0.0.1:3001/;          #接口服务地址
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

```
