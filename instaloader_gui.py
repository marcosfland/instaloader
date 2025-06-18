import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from instaloader import Instaloader, Profile
import os
import threading
from tkinter import filedialog

def download_photos():
    usernames = entry_usernames.get().split(',')
    if not usernames or usernames == ['']:
        messagebox.showerror("Erro", "Por favor, insira pelo menos um nome de usuário.")
        return

    download_path = entry_download_path.get()
    os.makedirs(download_path, exist_ok=True)

    sessionfile = entry_sessionfile.get()
    username = entry_login.get()
    password = entry_password.get()
    loader = Instaloader()
    try:
        if sessionfile:
            loader.load_session_from_file(username, sessionfile)
        else:
            if not username or not password:
                messagebox.showerror("Erro", "Por favor, insira seu login e senha do Instagram ou um sessionfile.")
                return
            loader.login(username, password)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao fazer login: {e}")
        return

    total_posts = 0
    for username in usernames:
        try:
            profile = Profile.from_username(loader.context, username.strip())
            total_posts += profile.mediacount
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter perfil {username}: {e}")
            return

    progress_bar['maximum'] = total_posts
    progress_bar['value'] = 0
    label_progress['text'] = f"0/{total_posts}"

    count = 0
    for username in usernames:
        try:
            profile = Profile.from_username(loader.context, username.strip())
            for post in profile.get_posts():
                try:
                    if var_photos.get() and post.typename == 'GraphImage':
                        loader.download_post(post, target=f"{download_path}/{profile.username}")
                    if var_videos.get() and post.typename == 'GraphVideo':
                        loader.download_post(post, target=f"{download_path}/{profile.username}")
                    if var_reels.get() and post.typename == 'GraphSidecar':
                        loader.download_post(post, target=f"{download_path}/{profile.username}")
                    count += 1
                    progress_bar['value'] = count
                    label_progress['text'] = f"{count}/{total_posts}"
                    root.update_idletasks()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao baixar post: {e}")
            messagebox.showinfo("Sucesso", f"Mídias de {username} baixadas com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao baixar mídias de {username}: {e}")

def download_photos_thread():
    threading.Thread(target=download_photos, daemon=True).start()

def clear_fields():
    entry_usernames.delete(0, tk.END)
    entry_login.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_sessionfile.delete(0, tk.END)
    var_photos.set(False)
    var_videos.set(False)
    var_reels.set(False)
    progress_bar['value'] = 0
    label_progress['text'] = ""
    entry_download_path.delete(0, tk.END)
    entry_download_path.insert(0, default_download_path)


def toggle_password():
    if entry_password.cget('show') == '':
        entry_password.config(show='*')
        btn_toggle_password.config(text='Mostrar')
    else:
        entry_password.config(show='')
        btn_toggle_password.config(text='Ocultar')


def choose_directory():
    path = filedialog.askdirectory()
    if path:
        entry_download_path.delete(0, tk.END)
        entry_download_path.insert(0, path)

def choose_sessionfile():
    path = filedialog.askopenfilename(filetypes=[("Arquivo de sessão", "*.session")])
    if path:
        entry_sessionfile.delete(0, tk.END)
        entry_sessionfile.insert(0, path)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Instaloader GUI")

# Diretório padrão
default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", "Instaloader")

tk.Label(root, text="Nome de usuário(s) do Instagram (separados por vírgula):").pack(pady=10)
entry_usernames = tk.Entry(root, width=50)
entry_usernames.pack(pady=5)

tk.Label(root, text="Login do Instagram:").pack(pady=10)
entry_login = tk.Entry(root, width=30)
entry_login.pack(pady=5)

# Campo senha com botão mostrar/ocultar
frame_password = tk.Frame(root)
frame_password.pack(pady=5)
tk.Label(frame_password, text="Senha do Instagram:").pack(side=tk.LEFT)
entry_password = tk.Entry(frame_password, show='*', width=30)
entry_password.pack(side=tk.LEFT, padx=5)
btn_toggle_password = tk.Button(frame_password, text="Mostrar", command=toggle_password)
btn_toggle_password.pack(side=tk.LEFT)

var_photos = tk.BooleanVar()
var_videos = tk.BooleanVar()
var_reels = tk.BooleanVar()

tk.Checkbutton(root, text="Fotos", variable=var_photos).pack(pady=5)
tk.Checkbutton(root, text="Vídeos", variable=var_videos).pack(pady=5)
tk.Checkbutton(root, text="Reels", variable=var_reels).pack(pady=5)

# Campo para sessionfile
frame_session = tk.Frame(root)
frame_session.pack(pady=5)
tk.Label(frame_session, text="Sessionfile (opcional):").pack(side=tk.LEFT)
entry_sessionfile = tk.Entry(frame_session, width=40)
entry_sessionfile.pack(side=tk.LEFT, padx=5)
tk.Button(frame_session, text="Escolher...", command=choose_sessionfile).pack(side=tk.LEFT)

# Campo para diretório de download
frame_path = tk.Frame(root)
frame_path.pack(pady=5)
tk.Label(frame_path, text="Diretório de download:").pack(side=tk.LEFT)
entry_download_path = tk.Entry(frame_path, width=40)
entry_download_path.pack(side=tk.LEFT, padx=5)
entry_download_path.insert(0, default_download_path)
tk.Button(frame_path, text="Escolher...", command=choose_directory).pack(side=tk.LEFT)

# Botão limpar campos
btn_clear = tk.Button(root, text="Limpar Campos", command=clear_fields)
btn_clear.pack(pady=5)

# Botão baixar mídias (agora chama a thread)
tk.Button(root, text="Baixar Mídias", command=download_photos_thread).pack(pady=20)

progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=5)
label_progress = tk.Label(root, text="")
label_progress.pack()

root.mainloop()