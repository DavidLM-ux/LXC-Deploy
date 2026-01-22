# LXC Deploy

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![License](https://img.shields.io/badge/license-GPL-orange.svg)

**LXC Deploy** est un outil d'automatisation pour le déploiement rapide et simple de containers LXC sous Linux.

```
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   ██╗     ██╗  ██╗ ██████╗                                       ║
    ║   ██║     ╚██╗██╔╝██╔════╝                                       ║
    ║   ██║      ╚███╔╝ ██║                                            ║
    ║   ██║      ██╔██╗ ██║                                            ║
    ║   ███████╗██╔╝ ██╗╚██████╗                                       ║
    ║   ╚══════╝╚═╝  ╚═╝ ╚═════╝                                       ║
    ║                                                                  ║
    ║   ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗             ║
    ║   ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝             ║
    ║   ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝              ║
    ║   ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝               ║
    ║   ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║                ║
    ║   ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝                ║
    ║                                                                  ║
    ║        ⚡  Automated Container Deployment Framework  ⚡            ║
    ╚══════════════════════════════════════════════════════════════════╝
```

## Fonctionnalités

- Déploiement automatisé de containers LXC
- Support de multiples systèmes d'exploitation (Ubuntu, Debian)
- Déploiement de clients et serveurs
- Configuration automatique (Web, BDD, LAMP, Pare-feu)
- Mise à jour automatique des containers
- Installation automatique SSH (client/serveur)
- Interface utilisateur intuitive

## Prérequis

- **OS** : Linux (testé sur Ubuntu/Debian)
- **Python** : 3.6 ou supérieur
- **Privilèges** : Accès root/sudo
- **LXC** : Sera installé automatiquement si absent

## Installation

### Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/davidlmsec/lxc-deploy.git
cd lxc-deploy

# Rendre le script exécutable
chmod +x lxc_deploy.py

# Lancer le script
sudo ./lxc_deploy.py
```

### Installation manuelle de LXC (optionnel)

```bash
sudo apt update
sudo apt install -y lxc lxc-templates debootstrap
```

## Utilisation

### Démarrage

```bash
sudo python3 lxc_deploy.py
```

### Menu principal

```
[1] Déployer des clients
[2] Déployer des serveurs
[3] Lister les containers
[4] Démarrer un container
[5] Arrêter un container
[6] Supprimer un container
[7] Quitter
```

### Exemples d'utilisation

#### Déployer 3 clients Ubuntu

1. Sélectionner l'option `[1] Déployer des clients`
2. Entrer le nombre : `3`
3. Choisir l'OS : `[1] Ubuntu 24.04`
4. Nom de base : `client`
5. Confirmer

Résultat : 3 containers nommés `client-1`, `client-2`, `client-3`

#### Déployer un serveur LAMP

1. Sélectionner l'option `[2] Déployer des serveurs`
2. Entrer le nombre : `1`
3. Type de serveur : `[3] LAMP`
4. Choisir l'OS : `[3] Debian 13`
5. Nom : `lamp-server`
6. Confirmer

## Architecture

```
lxc-deploy/
├── lxc_deploy.py          # Script principal
├── README.md              # Documentation
├── LICENSE                # Licence GPL
└── .gitignore             # Fichiers à ignorer
```

## Types de serveurs supportés

| Type | Packages installés |
| --- | --- |
| **Web** | Apache2 |
| **Base de données** | MySQL Server & Client |
| **LAMP** | Apache2 + MySQL + PHP |
| **Pare-feu** | iptables + iptables-persistent |

## Systèmes d'exploitation supportés

- Ubuntu 24.04 (Noble)
- Ubuntu 22.04 (Jammy)
- Debian 13 (Trixie)
- Debian 12 (Bookworm)

## Sécurité

- Vérification des privilèges root
- Installation automatique SSH serveur sur les serveurs
- Installation automatique SSH client sur les clients
- Mise à jour système automatique (`apt update && apt upgrade`)

## Développement

### Structure du code

Le projet est organisé en sections claires :

- **Configuration** : OS et types de serveurs
- **Fonctions utilitaires** : Helpers pour l'affichage
- **Vérifications système** : Root et LXC
- **Déploiement** : Clients et serveurs
- **Menu principal** : Interface utilisateur

### Contribuer

Les contributions sont les bienvenues !

1. Fork le projet
2. Crée une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit tes changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push sur la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvre une Pull Request

## TODO / Roadmap

- [ ] Support de plus d'OS (Alpine, CentOS, Rocky Linux)
- [ ] Configuration réseau personnalisée
- [ ] Snapshots et backups automatiques
- [ ] Interface web (Django/Flask)
- [ ] Export/Import de configurations
- [ ] Support Docker en plus de LXC
- [ ] Tests unitaires
- [ ] Logs détaillés dans fichier

## Problèmes connus

- Nécessite une connexion internet pour télécharger les templates
- Certains OS nécessitent plus de temps de démarrage (ajuster `sleep`)

## Licence

Ce projet est sous licence GPL. Voir le fichier LICENSE pour plus de détails.

## Auteur

**DavidLM-ux**

- GitHub: [@DavidLM-ux](https://github.com/DavidLM-ux)

## Support

Pour toute question ou problème :

- Ouvrir une [issue](https://github.com/DavidLM-ux/lxc-deploy/issues)
- Contact : lemeur.david@proton.me
