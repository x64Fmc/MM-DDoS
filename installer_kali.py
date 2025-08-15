#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os

# Detecta gerenciador de pacotes
def detect_package_manager():
    managers = ["apt", "dnf", "yum", "pacman", "zypper"]
    for m in managers:
        if shutil.which(m):
            return m
    return None

def run_command(cmd):
    """Executa comando e para se houver erro."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar: {' '.join(cmd)}")
        sys.exit(1)

def is_installed(program):
    """Verifica se um comando existe."""
    return shutil.which(program) is not None

# Instala pacote pelo gerenciador correto
def install_package(pkg):
    if is_installed(pkg.split()[0]):
        print(f"✅ {pkg} já instalado.")
        return
    if PKG_MANAGER == "apt":
        run_command(["sudo", "apt", "install", "-y"] + pkg.split())
    elif PKG_MANAGER == "dnf":
        run_command(["sudo", "dnf", "install", "-y"] + pkg.split())
    elif PKG_MANAGER == "yum":
        run_command(["sudo", "yum", "install", "-y"] + pkg.split())
    elif PKG_MANAGER == "pacman":
        run_command(["sudo", "pacman", "-S", "--noconfirm"] + pkg.split())
    elif PKG_MANAGER == "zypper":
        run_command(["sudo", "zypper", "install", "-y"] + pkg.split())

# Instala o Java
def install_java():
    java_versions = [
        "openjdk-21-jdk", "java-21-openjdk", 
        "openjdk-20-jdk", "java-20-openjdk",
        "openjdk-19-jdk", "java-19-openjdk",
        "openjdk-18-jdk", "java-18-openjdk",
        "openjdk-17-jdk", "java-17-openjdk",
        "openjdk-11-jdk", "java-11-openjdk",
        "openjdk-8-jdk", "java-1.8.0-openjdk"
    ]
    for version in java_versions:
        print(f"📦 Tentando instalar {version}...")
        try:
            install_package(version)
            print(f"✅ {version} instalado com sucesso.")
            return
        except SystemExit:
            continue
    print("⚠️ Não foi possível instalar o Java automaticamente.")

# Instala pacotes npm globalmente
def npm_install(pkg):
    try:
        subprocess.run(["npm", "list", "-g", pkg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"✅ {pkg} já instalado (npm global).")
    except subprocess.CalledProcessError:
        print(f"📦 Instalando {pkg} (npm global)...")
        run_command(["sudo", "npm", "install", "-g", pkg])

# ======================
# Início do script
# ======================
PKG_MANAGER = detect_package_manager()
if not PKG_MANAGER:
    print("❌ Nenhum gerenciador de pacotes suportado encontrado (apt/dnf/yum/pacman/zypper).")
    sys.exit(1)

print(f"🔍 Detectado gerenciador de pacotes: {PKG_MANAGER}")

# Atualiza lista de pacotes (se aplicável)
if PKG_MANAGER in ["apt", "dnf", "yum", "zypper"]:
    run_command(["sudo", PKG_MANAGER, "update", "-y"])
elif PKG_MANAGER == "pacman":
    run_command(["sudo", "pacman", "-Syu", "--noconfirm"])

# Instalar dependências
install_java()
install_package("nodejs")
install_package("npm")

# Pacotes Node.js necessários
node_packages = ["axios", "request", "header-generator"]
for pkg in node_packages:
    npm_install(pkg)

# Executa script Node.js
if os.path.exists("MegaMedusa.js"):
    print("🚀 Executando MegaMedusa.js...")
    run_command(["node", "MegaMedusa.js"])
else:
    print("⚠️ Arquivo MegaMedusa.js não encontrado.")

print("\033[31m[\033[33mMedusa\033[31m]\033[0m \033[32m> \033[33mInstalação concluída com sucesso 🚀")
