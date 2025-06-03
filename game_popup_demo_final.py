import tkinter as tk
from tkinter import messagebox

play_minutes = 0
time_limit = 2  # 縮短模擬用（分鐘），3秒 = 1分鐘，2分鐘約6秒觸發
game_running = True  # 本局遊戲是否進行中
warning_shown = False  # 是否已顯示超時提醒（避免重複彈窗）

root = tk.Tk()
root.title("遊戲防沉迷提示系統")
root.geometry("420x400")
root.resizable(False, False)

title_label = tk.Label(root, text="🎮 遊戲時間管理", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

play_time_label = tk.Label(root, text=f"目前已遊玩：{play_minutes} 分鐘", font=("Helvetica", 12))
play_time_label.pack()

def update_play_label():
    play_time_label.config(text=f"目前已遊玩：{play_minutes} 分鐘")
    root.after(1000, update_play_label)

def show_warning_dialog():
    global game_running, warning_shown
    warning_shown = True

    warn_win = tk.Toplevel(root)
    warn_win.title("時間提醒")
    warn_win.geometry("320x180")
    warn_win.grab_set()

    msg = f"你已經遊玩了 {play_minutes} 分鐘，建議休息一下。"
    tk.Label(warn_win, text=msg, wraplength=280, font=("Helvetica", 11)).pack(pady=20)

    btn_frame = tk.Frame(warn_win)
    btn_frame.pack(pady=10)

    if game_running:
        # 遊戲還沒結束，提供繼續遊戲和立即結束
        tk.Button(btn_frame, text="⚠️ 繼續遊戲", width=12, command=warn_win.destroy).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="✅ 立即結束", width=12, command=root.quit).grid(row=0, column=1, padx=10)
    else:
        # 遊戲已結束，只能查看統計或立即結束
        def show_stats():
            stats_msg = (
                f"📊 本週統計：\n"
                f"- 累積時間：13 小時 47 分鐘\n"
                f"- 平均每日：1 小時 58 分鐘（+23%）\n"
                f"- 熱門時段：晚上 10:00–12:00"
            )
            messagebox.showinfo("本週遊戲統計", stats_msg)

        tk.Button(btn_frame, text="📈 查看本週統計", width=12, command=show_stats).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="✅ 立即結束", width=12, command=root.quit).grid(row=0, column=1, padx=10)

def check_time_limit():
    global play_minutes, warning_shown
    if game_running:
        play_minutes += 1
        if play_minutes >= time_limit and not warning_shown:
            show_warning_dialog()
    root.after(3000, check_time_limit)

def rest_now():
    messagebox.showinfo("休息成功", "你已選擇結束今日遊戲，請好好休息！")
    root.quit()

def simulate_game_end():
    global game_running, warning_shown
    game_running = False
    warning_shown = False  # 遊戲結束重置提醒狀態，避免彈窗沒出現
    messagebox.showinfo("遊戲結束", "本局遊戲已結束。提醒視窗將只能結束或查看統計。")

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn1 = tk.Button(btn_frame, text="✅ 結束今日遊戲", command=rest_now, width=18)
btn1.grid(row=0, column=0, padx=5, pady=5)

btn3 = tk.Button(root, text="📈 查看本週統計", command=lambda: messagebox.showinfo("本週遊戲統計", 
    "📊 本週統計：\n- 累積時間：13 小時 47 分鐘\n- 平均每日：1 小時 58 分鐘（+23%）\n- 熱門時段：晚上 10:00–12:00"), width=38)
btn3.pack(pady=5)

# 模擬遊戲結束按鈕，調整大小及位置，固定在右下角
btn2 = tk.Button(root, text="🎮 模擬遊戲結束", command=simulate_game_end, width=12)
btn2.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor='se')  

root.after(3000, check_time_limit)
update_play_label()

root.mainloop()