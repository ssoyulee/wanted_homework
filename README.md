# wanted_homework
wanted_homework

## 실행 방법
```
  # git 소스를 받아온다.
  $ git clone https://github.com/ssoyulee/wanted_homework.git
  
  # docker 폴더로 이동한다.
  $ cd wanted_homework/docker
  
  # docker-compose를 실행한다.
  $ docker-compose up -d 
```

## 접속 방법
### Port 
```
기본 포트 : 80
포트 변경이 필요할 경우
wanted_homework/docker/docker-compose.yml 파일 내 포트를 수정하시면 됩니다.
- '80:5000'
```

### DB Data init
```
http://{host}/init
```

### Swagger URL
```
http://{host}/wanted/doc
```

