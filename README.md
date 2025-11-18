# README TP Cloud SAOUDI Selim — FastAPI + Redis + Docker  

## Objectif  
Implémenter une API REST avec FastAPI, ajouter une persistance Redis, puis rendre l’ensemble portable grâce à Docker


## Structure du projet
```
CLOUD_API/
 ├── server.py
 ├── requirements.txt
 ├── Dockerfile
 └── README.md
```
---

## API FastAPI

### Lancement de l’API
```
python -m uvicorn server:app --reload
```

### Endpoints implémentés  
- `POST /products` — Créer un produit  
- `GET /products/{name}` — Lire un produit  
- `GET /products` — Lister les produits  

### Test via `curl`
```
curl -X POST http://localhost:8000/products/      -H "Content-Type: application/json"      -d "{\"name\":\"Orange\",\"price\":4,\"quantity\":12}"
```

```
curl http://localhost:8000/products/Orange
```

---

## Redis

### Démarrage du conteneur Redis
```
docker run -d --name redis -p 6379:6379 redis:7
```

### Test Redis
```
docker exec -it redis redis-cli PING
```
Reponse : `PONG`

### Vérification de la persistance  
1. POST d’un produit  
2. GET du produit  
3. Redémarrage de l’API  
   ```
   docker stop api
   docker start api
   ```
4. GET à nouveau  
Le produit est toujours présent = persistance OK

---

## Dockerisation de l’API

### `Dockerfile`
```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Construction de l’image
```
docker build -t fastapi_app .
```

### Lancement avec lien vers Redis
```
docker run --name api ^
    --link redis:redis ^
    -e REDIS_HOST=redis ^
    -p 8000:8000 ^
    fastapi_app
```

### Test final
```
curl http://localhost:8000/products/Orange
```
Produit trouvé = API + Redis + Docker 100% fonctionnels

---

## Test Docker Hub

### Tag
```
docker tag fastapi_app MON_DOCKER_ID/fastapi_app:v1
```

### Push
```
docker push MON_DOCKER_ID/fastapi_app:v1
```

### Pull
```
docker pull MON_DOCKER_ID/fastapi_app:v1
```


## Conclusion  

**API + Redis + Docker = système portable et persistant**
