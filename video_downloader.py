import os
import requests
import instaloader
import yt_dlp

def baixar_youtube(url):
    output_path = "videos"
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': 'mp4',
        'cookiefile': 'cookies/youtube_cookies.txt',  # <-- aqui o arquivo de cookies
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("📥 Baixando vídeo do YouTube...")
        ydl.download([url])
        print("✅ Download concluído!")

def baixar_stories(usuario, senha):
    loader = instaloader.Instaloader(dirname_pattern="stories/{target}")
    print("🔐 Fazendo login no Instagram...")
    loader.login(usuario, senha)

    perfil = input("Digite o nome do perfil (sem @): ")
    print(f"📥 Baixando stories de @{perfil}...")
    loader.download_stories(userids=[perfil])
    print("✅ Stories baixados!")

def baixar_link_direto(url):
    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)

    print("📥 Baixando arquivo do link direto...")
    r = requests.get(url)
    nome_arquivo = url.split("/")[-1].split("?")[0]
    caminho = os.path.join(output_path, nome_arquivo)

    with open(caminho, 'wb') as f:
        f.write(r.content)
    print(f"✅ Download concluído: {caminho}")

def main():
    print("Escolha uma opção (1, 2 ou 3):")
    print("1 - Baixar vídeo do YouTube")
    print("2 - Baixar stories do Instagram")
    print("3 - Baixar link direto (MP4, etc.)")

    escolha = input("Opção: ")

    if escolha == '1':
        url = input("Cole o link do YouTube: ")
        baixar_youtube(url)
    elif escolha == '2':
        usuario = input("Usuário do Instagram: ")
        senha = input("Senha: ")
        baixar_stories(usuario, senha)
    elif escolha == '3':
        url = input("Cole o link direto do arquivo: ")
        baixar_link_direto(url)
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
