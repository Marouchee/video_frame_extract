import tkinter as tk
from tkinter import filedialog, messagebox
import cv2, os

def extract_frames(video_path, out_root):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    folder = os.path.join(out_root, video_name)
    os.makedirs(folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] 비디오 열기 실패: {video_path}")
        return 0

    idx = 0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"[DEBUG] 총 프레임 수: {total}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_path = os.path.join(folder, f"{video_name}_{idx:05d}.jpg")
        ok = cv2.imwrite(frame_path, frame)
        print(f"[DEBUG] 쓰기 시도 #{idx}: {frame_path} → {'성공' if ok else '실패'}")
        idx += 1
    cap.release()
    return idx

def select_video():
    path = filedialog.askopenfilename(filetypes=[("MP4 파일","*.mp4")])
    if path: video_var.set(path)

def select_folder():
    path = filedialog.askdirectory()
    if path: folder_var.set(path)

def start_extraction():
    video = video_var.get()
    out   = folder_var.get()
    if not video or not out:
        messagebox.showwarning("경고", "비디오 파일과 저장 폴더를 모두 선택하세요.")
        return
    count = extract_frames(video, out)
    messagebox.showinfo("완료", f"{count}개의 프레임이 저장되었습니다.")

# GUI 구성
root = tk.Tk()
root.title("Video to Frames")

video_var  = tk.StringVar()
folder_var = tk.StringVar()

tk.Label(root, text="비디오 파일:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=video_var, width=40).grid(row=0, column=1)
tk.Button(root, text="찾아보기", command=select_video).grid(row=0, column=2)

tk.Label(root, text="저장 폴더:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=folder_var, width=40).grid(row=1, column=1)
tk.Button(root, text="찾아보기", command=select_folder).grid(row=1, column=2)

tk.Button(root, text="추출 시작", command=start_extraction).grid(row=2, column=1, pady=10)

root.mainloop()