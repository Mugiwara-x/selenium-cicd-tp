1️⃣ Avantages observés
• Avantages de l’automatisation des tests

Détection rapide des erreurs

Régression automatique à chaque modification

Gain de temps par rapport aux tests manuels

Exécution reproductible et fiable

Possibilité d’exécution en environnement CI

• Apport du CI/CD sur la qualité

Tests lancés automatiquement à chaque push / PR

Empêche l’intégration de code cassé

Historique clair des exécutions

Rapport de tests et couverture visibles

Amélioration continue du projet

2️⃣ Défis rencontrés
• Difficultés avec Selenium

Gestion du ChromeDriver (versions, permissions Linux)

Problème de droits d’exécution en CI

Synchronisation (attente des éléments)

Tests parfois instables sans WebDriverWait

• Amélioration possible de la stabilité

Utiliser systématiquement WebDriverWait

Éviter les time.sleep

Ajouter des assertions plus précises

Isoler les tests indépendamment

Utiliser un environnement Docker stable

3️⃣ Métriques importantes

Pour ce projet :

✅ Taux de réussite des tests

✅ Couverture de code (pytest-cov)

✅ Temps de chargement (performance)

✅ Rapport HTML automatisé

✅ Stabilité en CI