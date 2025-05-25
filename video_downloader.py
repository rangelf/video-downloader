import os
import requests
from pytube import YouTube
import instaloader

def baixar_youtube(url, output_path='videos'):
    yt = YouTube(url)
    video = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
    print(f"Baixando YouTube: {yt.title}")
    video.download(output_path)
    print("✔ Download do YouTube concluído.")

def baixar_instagram_story(username, output_path='videos'):
    L = instaloader.Instaloader(dirname_pattern=output_path, download_video_thumbnails=False)

    # Login necessário
    user = input("Seu usuário do Instagram: ")
    senha = input("Sua senha do Instagram: ")
    try:
        L.login(user, senha)
    except Exception as e:
        print(f"Erro ao logar: {e}")
        return

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"Baixando stories de: {username}")
        for story in L.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                L.download_storyitem(item, f"{output_path}/{username}_stories")
        print("✔ Download dos stories concluído.")
    except Exception as e:
        print(f"Erro ao baixar stories: {e}")

def baixar_direto(url, output_path='videos'):
    local_filename = url.split('/')[-1]
    os.makedirs(output_path, exist_ok=True)
    path = os.path.join(output_path, local_filename)

    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("✔ Download direto concluído.")

def main():
    print("1 - Baixar vídeo do YouTube")
    print("2 - Baixar stories do Instagram")
    print("3 - Baixar link direto (MP4, etc.)")
    escolha = input("Escolha uma opção (1, 2 ou 3): ")

    if escolha == '1':
        url = input("Cole o link do YouTube: ")
        baixar_youtube(url)
    elif escolha == '2':
        username = input("Digite o @ do perfil (sem o @): ")
        baixar_instagram_story(username)
    elif escolha == '3':
        url = input("Cole o link direto (MP4): ")
        baixar_direto(url)
    else:
        print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
