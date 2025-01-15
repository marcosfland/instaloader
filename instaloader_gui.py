import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from instaloader import Instaloader, Profile

def download_photos():
    usernames = entry_usernames.get().split(',')
    if not usernames:
        messagebox.showerror("Erro", "Por favor, insira pelo menos um nome de usuário.")
        return

    download_path = filedialog.askdirectory()
    if not download_path:
        messagebox.showerror("Erro", "Por favor, selecione uma pasta de destino.")
        return

    username = entry_login.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showerror("Erro", "Por favor, insira seu login e senha do Instagram.")
        return

    loader = Instaloader()
    loader.login(username, password)

    total_posts = 0
    for username in usernames:
        profile = Profile.from_username(loader.context, username.strip())
        total_posts += profile.mediacount

    progress_bar['maximum'] = total_posts
    progress_bar['value'] = 0

    for username in usernames:
        try:
            profile = Profile.from_username(loader.context, username.strip())
            for post in profile.get_posts():
                if var_photos.get() and post.typename == 'GraphImage':
                    loader.download_post(post, target=f"{download_path}/{profile.username}")
                if var_videos.get() and post.typename == 'GraphVideo':
                    loader.download_post(post, target=f"{download_path}/{profile.username}")
                if var_reels.get() and post.typename == 'GraphSidecar':
                    loader.download_post(post, target=f"{download_path}/{profile.username}")
                progress_bar['value'] += 1
                root.update_idletasks()
            messagebox.showinfo("Sucesso", f"Mídias de {username} baixadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar mídias de {username}: {e}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Instaloader GUI")

tk.Label(root, text="Nome de usuário(s) do Instagram (separados por vírgula):").pack(pady=10)
entry_usernames = tk.Entry(root, width=50)
entry_usernames.pack(pady=5)

tk.Label(root, text="Login do Instagram:").pack(pady=10)
entry_login = tk.Entry(root, width=30)
entry_login.pack(pady=5)

tk.Label(root, text="Senha do Instagram:").pack(pady=10)
entry_password = tk.Entry(root, show='*', width=30)
entry_password.pack(pady=5)

var_photos = tk.BooleanVar()
var_videos = tk.BooleanVar()
var_reels = tk.BooleanVar()

tk.Checkbutton(root, text="Fotos", variable=var_photos).pack(pady=5)
tk.Checkbutton(root, text="Vídeos", variable=var_videos).pack(pady=5)
tk.Checkbutton(root, text="Reels", variable=var_reels).pack(pady=5)

tk.Button(root, text="Baixar Mídias", command=download_photos).pack(pady=20)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=20)

root.mainloop()