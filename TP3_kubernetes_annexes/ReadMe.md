# TP3 : Orchestration de Conteneurs avec Kubernetes

## 📝 Présentation du Projet
Ce document regroupe les travaux pratiques réalisés sur **Kubernetes** (via Minikube en local). Il est divisé en deux parties principales :
1. **Orchestration de Microservices** (Dossier `TP3_Orchestration_avec_Kubernetes`) : Gestion de deux APIs indépendantes (`service-user` et `service-order`).
2. **Déploiement Frontend + Backend** (Dossier `TP3_kubernetes_annexes`) : Mise en place d'une interface web communiquant avec une API REST via le réseau interne du cluster.

---

## 🛠️ Prérequis Généraux
- **Docker Desktop** installé et en cours d'exécution.
- **Minikube** et **kubectl** installés et configurés.
- Commandes de vérification :
  ```powershell
  docker ps
  minikube status
  kubectl get nodes
  ```

---

## 🚀 Partie 1 : Microservices User & Order

### 🏗️ Architecture
- **Backend** : Deux microservices développés en Python avec le framework Flask.
- **Conteneurisation** : Un `Dockerfile` par service exposant les ports `5001` (User) et `5002` (Order).
- **Kubernetes** : Déploiements et Services configurés pour exposer les APIs. Utilisation de la règle `imagePullPolicy: Never` pour forcer Kubernetes à utiliser le cache local des images Docker et éviter les erreurs de téléchargement (ImagePullBackOff).

### 💻 Commandes de lancement
```powershell
# 1. Configurer le terminal pour utiliser le daemon Docker de Minikube
& "C:\Program Files\Kubernetes\Minikube\minikube.exe" docker-env | Invoke-Expression

# 2. Construire les images localement
docker build -t user-service:latest ./service-user
docker build -t order-service:latest ./service-order

# 3. Déployer sur Kubernetes (via manifestes ou ligne de commande)
kubectl apply -f Deployment.yaml
kubectl apply -f Service.yaml

# 4. Exposer l'URL localement (spécifique à Minikube pour contourner l'External-IP en pending)
minikube service service-order --url
```

---

## 🌐 Partie 2 : Application Frontend + Backend

### 🏗️ Architecture
- **Backend (API)** : Serveur Python (Flask) tournant sur le port `5000`. Expose la route `/api/message` qui renvoie un flux JSON (`{"message": "Hello from backend"}`).
- **Frontend (UI)** : Serveur web Python (Flask + HTML) tournant sur le port `8080`. Effectue une requête HTTP au backend en utilisant le nom DNS du service Kubernetes (`http://backend-service:5000/api/message`) et génère une page web avec la réponse.
- **Kubernetes (k8s/)** :
  - `backend-service` : Service de type `ClusterIP` (accessible uniquement en interne).
  - `frontend-service` : Service de type `NodePort` (accessible depuis le navigateur de la machine hôte).

### 💻 Commandes de lancement
```powershell
# 1. Construire les images Docker
cd backend
docker build -t tp-backend:v1 .
cd ../frontend
docker build -t tp-frontend:v1 .

# 2. Déployer l'infrastructure sur Kubernetes
cd ../k8s
kubectl apply -f backend.yaml
kubectl apply -f frontend.yaml

# 3. Accéder à l'interface Web
minikube service frontend-service --url
```

---

## 🧠 Explications Théoriques

Dans le cadre de ce TP, plusieurs concepts clés ont été mis en pratique :

* **Docker Compose vs Kubernetes :** - *Docker Compose* est un outil d'orchestration conçu pour des environnements locaux ou sur un seul serveur (mononœud). Il est idéal pour le développement et les tests.
  - *Kubernetes* est conçu pour la production à grande échelle. Il assure la haute disponibilité, la répartition de charge et le déploiement sur plusieurs serveurs (multinœuds).
* **Rôle d'un Pod :** C'est la plus petite unité déployable dans Kubernetes. Un Pod enveloppe un ou plusieurs conteneurs Docker (qui partagent le même réseau et stockage), lui attribuant une IP locale unique au sein du cluster.
* **Rôle d'un Deployment :** Il gère le cycle de vie des Pods de manière déclarative. Il s'assure que le bon nombre de réplicas tourne en permanence (auto-healing) et gère les mises à jour (rolling updates) sans interruption de service.
* **Rôle d'un Service :** Les Pods étant éphémères (leur IP change s'ils sont recréés), le Service fournit une adresse IP fixe et un nom DNS stable. C'est grâce à lui que notre frontend peut toujours joindre le backend en appelant simplement le nom `backend-service`, peu importe l'état des Pods sous-jacents.
* **Pourquoi séparer code et manifestes ?** Cela respecte le principe de séparation des préoccupations (fondamental en culture DevOps). Les développeurs gèrent le code applicatif (dossiers `frontend/` et `backend/`), tandis que les opérations gèrent l'infrastructure et l'orchestration (dossier `k8s/`).