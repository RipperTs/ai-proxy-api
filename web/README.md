# AI接口转发前端项目

## Nginx伪静态示例
```
    location /meetai/ {    
      proxy_pass http://127.0.0.1:3000/;          #接口服务地址
    }
    location /meetapi/ {    
      proxy_pass http://10.6.80.35:9500/;          #接口服务地址
    }
    location / {
      try_files $uri $uri/ /index.html;
    }
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_buffering off;
```
