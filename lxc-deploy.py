#!/usr/bin/env python3
import os
import subprocess
from time import sleep
import sys

def print_banner():
    """Affiche une bannière stylée."""
    c = '\033[1;36m'  # Cyan
    y = '\033[1;33m'  # Jaune
    m = '\033[1;35m'  # Magenta
    g = '\033[1;32m'  # Vert
    r = '\033[0m'     # Reset
    
    banner = f"""
    
    LXC-Deploy  Copyright (C) 2025  David LE MEUR
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions; Read LICENCE file for more informations.
    
{c}
    ╔══════════════════════════════════════════════════════════════════╗
    ║ {m}                                                                {c} ║
    ║ {y}   ██╗     ██╗  ██╗ ██████╗                                     {c} ║
    ║ {y}   ██║     ╚██╗██╔╝██╔════╝                                     {c} ║
    ║ {y}   ██║      ╚███╔╝ ██║                                          {c} ║
    ║ {y}   ██║      ██╔██╗ ██║                                          {c} ║
    ║ {y}   ███████╗██╔╝ ██╗╚██████╗                                     {c} ║
    ║ {y}   ╚══════╝╚═╝  ╚═╝ ╚═════╝                                     {c} ║
    ║ {y}                                                                {c} ║
    ║ {y}   ██████╗ ███████╗██████╗ ██╗      ██████╗ ██╗   ██╗           {c} ║
    ║ {y}   ██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗╚██╗ ██╔╝           {c} ║
    ║ {y}   ██║  ██║█████╗  ██████╔╝██║     ██║   ██║ ╚████╔╝            {c} ║
    ║ {y}   ██║  ██║██╔══╝  ██╔═══╝ ██║     ██║   ██║  ╚██╔╝             {c} ║
    ║ {y}   ██████╔╝███████╗██║     ███████╗╚██████╔╝   ██║              {c} ║
    ║ {y}   ╚═════╝ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═╝              {c} ║
    ║ {y}                                                                {c} ║
    ║ {c}        ⚡  Automated Container Deployment Framework  ⚡        {c} ║
    ║ {y}                     ━━━━━  v1.0.0  ━━━━━                       {c} ║
    ║ {m}                                                                {c} ║
    ╚══════════════════════════════════════════════════════════════════╝
{r}
    """
    print(banner)

def main_menu():
    """Affiche le menu principal."""
    while True:
        clear_screen()
        print_banner()
        print("\n[1] Déployer des clients")

# ==================== CONFIGURATION ====================
OS_CHOICES = {
    "1": {"name": "Ubuntu 24.04", "dist": "ubuntu", "release": "noble"},
    "2": {"name": "Ubuntu 22.04", "dist": "ubuntu", "release": "jammy"},
    "3": {"name": "Debian 13 (Trixie)", "dist": "debian", "release": "trixie"},
    "4": {"name": "Debian 12 (Bookworm)", "dist": "debian", "release": "bookworm"},
}

SERVER_TYPES = {
    "1": {"name": "Web (Apache2)", "packages": ["apache2"]},
    "2": {"name": "Base de données (MySQL)", "packages": ["mysql-server", "mysql-client"]},
    "3": {"name": "LAMP", "packages": ["apache2", "mysql-server", "mysql-client", "php", "libapache2-mod-php", "php-mysql"]},
    "4": {"name": "Pare-feu (iptables)", "packages": ["iptables", "iptables-persistent"]},
}

ARCH = "amd64"

# ==================== FONCTIONS UTILITAIRES ====================

def clear_screen():
    """Efface l'écran."""
    os.system('clear' if os.name != 'nt' else 'cls')

def print_header(text):
    """Affiche un en-tête formaté."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(text):
    """Affiche une étape."""
    print(f"\n>>> {text}")

def ask_yes_no(question, default_yes=True):
    """Pose une question oui/non avec valeur par défaut."""
    prompt = f"{question} [{'Y/n' if default_yes else 'y/N'}] : "
    response = input(prompt).strip().lower()
    
    if response == '':
        return default_yes
    return response in ('y', 'yes', 'oui')

def run_command(cmd, error_msg="Erreur lors de l'exécution de la commande"):
    """Exécute une commande et gère les erreurs."""
    try:
        if isinstance(cmd, str):
            subprocess.run(cmd, shell=True, check=True)
        else:
            subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  {error_msg}")
        print(f"   Détails: {e}")
        return False

# ==================== VÉRIFICATIONS SYSTÈME ====================

def check_root():
    """Vérifie que le script est exécuté en root."""
    if os.geteuid() != 0:
        print("   Ce script doit être exécuté en tant que root.")
        print("   Veuillez réessayer avec 'sudo'")
        sys.exit(1)
    print("✓ Privilèges root confirmés")

def check_lxc():
    """Vérifie et installe LXC si nécessaire."""
    print_step("Vérification de LXC")
    
    if not os.path.exists("/usr/bin/lxc-create"):
        print("   LXC n'est pas installé sur votre système")
        
        if ask_yes_no("Voulez-vous l'installer?"):
            print_step("Installation de LXC")
            if run_command(["apt", "update"], "Impossible de mettre à jour les paquets"):
                if run_command(
                    ["apt", "install", "-y", "lxc", "lxc-templates", "debootstrap"],
                    "Impossible d'installer LXC"
                ):
                    print("✓ LXC installé avec succès")
                    return
            sys.exit(1)
        else:
            print("  Ce programme ne peut fonctionner sans LXC")
            sys.exit(1)
    else:
        print("✓ LXC est déjà installé")

# ==================== SÉLECTION OS ====================

def select_os():
    """Permet à l'utilisateur de choisir un OS."""
    print("\n--- Choix du système d'exploitation ---")
    for key, os_info in OS_CHOICES.items():
        print(f"[{key}] {os_info['name']}")
    
    while True:
        choice = input("\nVotre choix : ").strip()
        if choice in OS_CHOICES:
            return OS_CHOICES[choice]
        print("  Choix invalide. Veuillez réessayer.")

# ==================== DÉPLOIEMENT CLIENT ====================

def deploy_client(name, os_info):
    """Déploie un container client."""
    print_header(f"Déploiement du client: {name}")
    
    # Création du container
    print_step(f"Création du container {name}")
    cmd_create = (
        f"lxc-create --template=download --name={name} -- "
        f"-d {os_info['dist']} -r {os_info['release']} -a {ARCH}"
    )
    
    if not run_command(cmd_create, f"Échec de la création de {name}"):
        return False
    
    # Démarrage
    print_step(f"Démarrage de {name}")
    if not run_command(f"lxc-start -n {name}", f"Échec du démarrage de {name}"):
        return False
    
    sleep(3)  # Attente du démarrage complet
    
    # Mise à jour
    print_step("Mise à jour du système")
    run_command(f"lxc-attach -n {name} -- apt update", "Échec de apt update")
    run_command(f"lxc-attach -n {name} -- apt upgrade -y", "Échec de apt upgrade")
    
    # Installation SSH client
    print_step("Installation du client SSH")
    run_command(f"lxc-attach -n {name} -- apt install -y openssh-client", "Échec de l'installation SSH client")
    
    print(f"✓ Client {name} déployé avec succès!")
    return True

def create_clients():
    """Gère la création de plusieurs clients."""
    print_header("DÉPLOIEMENT DE CLIENTS")
    
    try:
        nb_clients = int(input("Nombre de clients à déployer : "))
    except ValueError:
        print("  Veuillez entrer un nombre valide")
        return
    
    if nb_clients < 1:
        print("  Le nombre doit être supérieur à 0")
        return
    
    # Choix de l'OS
    os_info = select_os()
    print(f"\n✓ OS sélectionné: {os_info['name']}")
    
    # Nom de base
    base_name = input("Nom de base pour les clients (ex: 'client') : ").strip() or "client"
    
    # Confirmation
    if nb_clients == 1:
        names = [base_name]
    else:
        names = [f"{base_name}-{i+1}" for i in range(nb_clients)]
    
    print(f"\n  Containers à créer: {', '.join(names)}")
    
    if not ask_yes_no("Confirmer le déploiement?"):
        print("  Déploiement annulé")
        return
    
    # Déploiement
    success = 0
    for i, name in enumerate(names, 1):
        print(f"\n{'='*60}")
        print(f"  Client {i}/{nb_clients}")
        print(f"{'='*60}")
        if deploy_client(name, os_info):
            success += 1
        else:
            if not ask_yes_no("Une erreur s'est produite. Continuer?"):
                break
    
    print_header(f"RÉSULTAT: {success}/{nb_clients} client(s) déployé(s)")

# ==================== DÉPLOIEMENT SERVEUR ====================

def select_server_type():
    """Permet de choisir le type de serveur."""
    print("\n--- Type de serveur ---")
    for key, srv_info in SERVER_TYPES.items():
        print(f"[{key}] {srv_info['name']}")
    
    while True:
        choice = input("\nVotre choix : ").strip()
        if choice in SERVER_TYPES:
            return SERVER_TYPES[choice]
        print("  Choix invalide. Veuillez réessayer.")

def deploy_server(name, os_info, server_type):
    """Déploie un container serveur."""
    print_header(f"Déploiement du serveur: {name}")
    
    # Création du container
    print_step(f"Création du container {name}")
    cmd_create = (
        f"lxc-create --template=download --name={name} -- "
        f"-d {os_info['dist']} -r {os_info['release']} -a {ARCH}"
    )
    
    if not run_command(cmd_create, f"Échec de la création de {name}"):
        return False
    
    # Démarrage
    print_step(f"Démarrage de {name}")
    if not run_command(f"lxc-start -n {name}", f"Échec du démarrage de {name}"):
        return False
    
    sleep(3)
    
    # Mise à jour
    print_step("Mise à jour du système")
    run_command(f"lxc-attach -n {name} -- apt update", "Échec de apt update")
    run_command(f"lxc-attach -n {name} -- apt upgrade -y", "Échec de apt upgrade")
    
    # Installation SSH serveur
    print_step("Installation du serveur SSH")
    run_command(f"lxc-attach -n {name} -- apt install -y openssh-server", "Échec de l'installation SSH serveur")
    
    # Installation des packages spécifiques
    print_step(f"Installation de {server_type['name']}")
    packages = " ".join(server_type['packages'])
    run_command(
        f"lxc-attach -n {name} -- apt install -y {packages}",
        f"Échec de l'installation de {server_type['name']}"
    )
    
    # Configuration spécifique pour pare-feu
    if "iptables" in server_type['packages']:
        print_step("Configuration du pare-feu")
        run_command(f"lxc-attach -n {name} -- systemctl enable netfilter-persistent")
    
    print(f"✓ Serveur {name} ({server_type['name']}) déployé avec succès!")
    return True

def create_servers():
    """Gère la création de plusieurs serveurs."""
    print_header("DÉPLOIEMENT DE SERVEURS")
    
    try:
        nb_servers = int(input("Nombre de serveurs à déployer : "))
    except ValueError:
        print("  Veuillez entrer un nombre valide")
        return
    
    if nb_servers < 1:
        print("  Le nombre doit être supérieur à 0")
        return
    
    servers_config = []
    
    for i in range(nb_servers):
        print(f"\n{'─'*60}")
        print(f"  Configuration du serveur {i+1}/{nb_servers}")
        print(f"{'─'*60}")
        
        # Type de serveur
        server_type = select_server_type()
        
        # OS
        os_info = select_os()
        
        # Nom
        default_name = f"{server_type['name'].split()[0].lower()}-{i+1}"
        name = input(f"Nom du serveur [{default_name}] : ").strip() or default_name
        
        servers_config.append({
            'name': name,
            'os_info': os_info,
            'server_type': server_type
        })
    
    # Résumé
    print("\n  Résumé des serveurs à créer:")
    for cfg in servers_config:
        print(f"  • {cfg['name']}: {cfg['server_type']['name']} sur {cfg['os_info']['name']}")
    
    if not ask_yes_no("\nConfirmer le déploiement?"):
        print("  Déploiement annulé")
        return
    
    # Déploiement
    success = 0
    for i, cfg in enumerate(servers_config, 1):
        print(f"\n{'='*60}")
        print(f"  Serveur {i}/{nb_servers}")
        print(f"{'='*60}")
        if deploy_server(cfg['name'], cfg['os_info'], cfg['server_type']):
            success += 1
        else:
            if not ask_yes_no("Une erreur s'est produite. Continuer?"):
                break
    
    print_header(f"RÉSULTAT: {success}/{nb_servers} serveur(s) déployé(s)")

# ==================== MENU PRINCIPAL ====================

def main_menu():
    """Affiche le menu principal."""
    while True:
        clear_screen()
        print_header("GESTIONNAIRE DE CONTAINERS LXC")
        print("\n[1] Déployer des clients")
        print("[2] Déployer des serveurs")
        print("[3] Lister les containers")
        print("[4] Démarrer un container")
        print("[5] Arrêter un container")
        print("[6] Supprimer un container")
        print("[7] Quitter")
        print("="*60)
        
        choice = input("\nVotre choix : ").strip()
        
        if choice == '1':
            create_clients()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '2':
            create_servers()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '3':
            print_header("CONTAINERS EXISTANTS")
            run_command("lxc-ls -f")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '4':
            name = input("Nom du container à démarrer : ").strip()
            if run_command(f"lxc-start -n {name}"):
                print(f"✓ Container {name} démarré")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '5':
            name = input("Nom du container à arrêter : ").strip()
            if run_command(f"lxc-stop -n {name}"):
                print(f"✓ Container {name} arrêté")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '6':
            delete_container()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choice == '7':
            print("\n  Au revoir!")
            sys.exit(0)
        else:
            print("  Choix invalide")
            sleep(1)

def delete_container():
    """Supprime un container."""
    print_header("SUPPRESSION DE CONTAINER")
    run_command("lxc-ls")
    
    name = input("\nNom du container à supprimer : ").strip()
    
    if not name:
        print("  Nom invalide")
        return
    
    if ask_yes_no(f"   Confirmer la suppression de '{name}'?", default_yes=False):
        run_command(f"lxc-stop -n {name}")
        if run_command(f"lxc-destroy -n {name}"):
            print(f"✓ Container {name} supprimé")
        else:
            print(f"  Impossible de supprimer {name}")

# ==================== MAIN ====================

if __name__ == "__main__":
    clear_screen()
    print_banner()
    input("Appuyer sur Entrée pour continuer...")
    try:
        check_root()
        check_lxc()
        main_menu()
    except KeyboardInterrupt:
        print("\n\n   Interruption par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Erreur inattendue: {e}")
        sys.exit(1)
