# ☸️ TP3 : Orchestration de Microservices avec Kubernetes

## 📝 Description du projet

Ce projet a pour objectif de **déployer et d'orchestrer une architecture orientée microservices** en utilisant **Kubernetes** via **Minikube** en environnement local.

Il simule un **environnement d’e-commerce simplifié** composé de deux APIs indépendantes :

- **Service User** : gère les informations des utilisateurs  
- **Service Order** : gère les commandes (items et statuts)

Chaque service est **conteneurisé avec Docker** puis **déployé sur Kubernetes** afin d’illustrer les bases de l’orchestration de microservices.

---

# 🏗️ Architecture

L’architecture repose sur **Docker pour la conteneurisation** et **Kubernetes pour l’orchestration**.

```
Client
   │
   ▼
Kubernetes Service
   │
   ├── User Service (Flask API)
   │       └── Pod
   │
   └── Order Service (Flask API)
           └── Pod
```

---

## 🔹 Backend

Deux microservices sont développés en **Python avec le framework Flask** :

- **User Service**
  - gère les utilisateurs
  - port exposé : `5001`

- **Order Service**
  - gère les commandes
  - port exposé : `5002`

---

## 🔹 Conteneurisation

Chaque service possède son propre **Dockerfile** qui :

- installe les dépendances via `requirements.txt`
- copie le code source de l’application
- expose le port nécessaire
- démarre l’application Flask

---

## 🔹 Ressources Kubernetes

Le déploiement repose sur deux types de ressources principales.

### Deployments

Les **Deployments** permettent de :

- créer et gérer les **Pods**
- définir le nombre de **réplicas**
- redémarrer automatiquement les conteneurs en cas d’erreur

### Services

Les **Services Kubernetes** permettent :

- d’exposer les Pods
- d’assurer la communication réseau
- de fournir un **point d’accès stable aux microservices**

---

# 🚀 Commandes minimales pour lancer le projet

## 1️⃣ Démarrer le cluster Minikube

```bash
minikube start
```

---

## 2️⃣ Configurer Docker pour utiliser l’environnement de Minikube

Cela permet à Kubernetes **d’accéder aux images construites localement sans passer par Docker Hub**.

```powershell
& "C:\Program Files\Kubernetes\Minikube\minikube.exe" docker-env | Invoke-Expression
```

---

## 3️⃣ Construire les images Docker

```bash
docker build -t user-service:latest ./service-user
docker build -t order-service:latest ./service-order
```

---

## 4️⃣ Déployer les ressources Kubernetes

```bash
kubectl apply -f Deployment.yaml
kubectl apply -f Service.yaml
```

Ces commandes permettent de créer :

- les **Deployments**
- les **Pods**
- les **Services**

---

## 5️⃣ Tester et exposer l’API (spécifique à Minikube)

```bash
minikube service service-order --url
```

Cette commande génère une **URL accessible depuis la machine locale**.

Il suffit ensuite d’ouvrir l’URL générée dans un navigateur et d’ajouter :

```
/orders
```

à la fin de l’adresse.

---

# 🧠 Notes et explications supplémentaires

## Problème d'image locale (ErrImagePull / ImagePullBackOff)

Par défaut, Kubernetes tente de **télécharger les images avec le tag `latest` depuis un registre distant**, généralement **Docker Hub**.

Comme les images sont **construites localement dans Minikube**, il est nécessaire d’ajouter dans les manifestes Kubernetes :

```yaml
imagePullPolicy: Never
```

Cela force Kubernetes à **utiliser l’image locale déjà présente dans l’environnement Minikube**.

---

## External-IP en `Pending`

Dans un environnement cloud classique (AWS, GCP, Azure), un service de type **LoadBalancer** reçoit automatiquement une **IP publique**.

En environnement local avec **Minikube**, cette IP reste bloquée sur :

```
<pending>
```

Pour contourner ce comportement, on utilise la commande suivante :

```bash
minikube service <nom-du-service> --url
```

Cette commande crée un **tunnel réseau entre Kubernetes et la machine hôte**, permettant d’accéder au service depuis le navigateur.

---

# ✨ Features en bonus (pistes d’amélioration)

## 1️⃣ Ingress Controller

Implémenter un **Ingress Controller** afin de router le trafic vers les différents services via **une seule URL d’entrée**.

Exemple :

```
/api/users
/api/orders
```

Avantages :

- point d’entrée unique
- gestion du routage HTTP
- architecture plus proche d’un environnement de production

---

## 2️⃣ ConfigMaps

Ajouter des **ConfigMaps Kubernetes** pour gérer dynamiquement les variables d’environnement.

Exemples :

- port de l’application Flask
- variables de configuration

Avantages :

- séparation entre **configuration et code**
- modification possible **sans reconstruire les images Docker**