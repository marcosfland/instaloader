import instaloader
import time

# Configurações iniciais
PROFILES_TO_MONITOR = ["perfil1", "perfil2"]  # Substitua pelos nomes dos perfis que deseja monitorar
CHECK_INTERVAL = 300  # Tempo em segundos entre cada verificação (5 minutos)
SESSION_FILE = "session"  # Nome do arquivo para manter a sessão ativa

def login(loader):
    """Faz login no Instagram usando uma sessão salva ou pedindo credenciais."""
    try:
        # Tenta carregar uma sessão existente
        loader.load_session_from_file("username", SESSION_FILE)
        print("Sessão carregada com sucesso!")
    except:
        # Se não houver sessão salva, faz login manual
        print("Fazendo login manual...")
        username = input("Digite seu usuário do Instagram: ")
        password = input("Digite sua senha: ")
        loader.login(username, password)
        loader.save_session_to_file(SESSION_FILE)
        print("Sessão salva para uso futuro.")

def monitor_profiles():
    """Monitora perfis e baixa novos posts automaticamente."""
    loader = instaloader.Instaloader(download_videos=True, download_comments=False)
    login(loader)
    
    last_post_times = {profile: None for profile in PROFILES_TO_MONITOR}

    while True:
        for profile_name in PROFILES_TO_MONITOR:
            try:
                profile = instaloader.Profile.from_username(loader.context, profile_name)
                latest_post = next(profile.get_posts())
                
                if last_post_times[profile_name] != latest_post.date_utc:
                    print(f"Novo post detectado em {profile_name}! Baixando...")
                    loader.download_post(latest_post, target=profile_name)
                    last_post_times[profile_name] = latest_post.date_utc
                else:
                    print(f"Nenhum novo post em {profile_name}.")
            except Exception as e:
                print(f"Erro ao verificar {profile_name}: {e}")
        
        print(f"Aguardando {CHECK_INTERVAL} segundos para a próxima verificação...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_profiles()
