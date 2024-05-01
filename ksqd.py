# 导入所需的模块
import tkinter as tk  # 用于创建图形用户界面
import os  # 用于操作系统功能，如文件和目录操作
import base64  # 用于编码和解码数据
import ctypes  # 用于调用C语言库函数
from tkinter import filedialog  # 用于打开文件对话框
from tkinter import messagebox  # 用于显示消息框

# 初始化变量
first_time = True  # 标记是否是第一次运行
xz_dir_path = ""  # 存储选择的文件夹路径
child = None  # 存储Toplevel窗口的引用
mm_entry = None  # 存储密码输入框的引用
button4 = None  # 存储“确定”按钮的引用

# 定义取消隐藏文件的函数
def show_pz(pz_path):
    # Windows API 常量，用于清除文件属性
    FILE_ATTRIBUTE_NORMAL = 0x80

    # 将文件路径转换为宽字符串，以便在Windows API中使用
    pz_path_w = pz_path.encode('utf-8').decode('unicode-escape')

    # 调用Windows API函数设置文件属性，清除文件的隐藏属性
    ctypes.windll.kernel32.SetFileAttributesW(pz_path_w, FILE_ATTRIBUTE_NORMAL)

# 定义隐藏文件的函数
def hide_pz(pz_path):
    # Windows API 常量，用于设置文件属性
    FILE_ATTRIBUTE_HIDDEN = 0x2

    # 将文件路径转换为宽字符串，以便在Windows API中使用
    pz_path_w = pz_path.encode('utf-8').decode('unicode-escape')

    # 调用Windows API函数设置文件属性，将文件标记为隐藏
    ctypes.windll.kernel32.SetFileAttributesW(pz_path_w, FILE_ATTRIBUTE_HIDDEN)

# 定义按钮1的点击事件处理函数
def on_button1_click():
    # 弹出文件选择对话框来选择一个文件夹
    global xz_dir_path  # 使用全局变量存储选择的文件夹路径
    xz_dir_path = filedialog.askdirectory(title="选择一个文件夹")
    # 更新文本输入框的内容为选择的文件夹路径
    if xz_dir_path != "":
        xz_entry_var.set(xz_dir_path)

# 定义按钮2的点击事件处理函数
def on_button2_click():
    # 检查是否已经选择了文件夹
    if xz_entry_var.get() == "":
        messagebox.showinfo("错误：", "发生错误：路径为空")
    else:
        # 检查dir_path.txt文件是否存在
        if os.path.exists('dir_path.txt'):
            show_pz('dir_path.txt')  # 如果存在，先取消隐藏
        # 将选择的文件夹路径写入文件，并隐藏该文件
        with open('dir_path.txt', 'w', encoding='utf-8') as xz_dir:
            xz_dir.write(xz_dir_path)
            hide_pz('dir_path.txt')  # 隐藏dir_path.txt文件
            messagebox.showinfo("提示：", "保存成功！")

# 定义按钮3的第一次点击事件处理函数
def on_button3_first_click():
    global child, mm_entry, button4  # 使用全局变量存储Toplevel窗口和组件的引用
    # 创建一个Toplevel窗口，用于输入密码
    child = tk.Toplevel()
    # 设置Toplevel窗口的标题
    child.title("密码：")
    # 创建文本输入框，用于输入密码
    mm_entry = tk.Entry(child, width=6)
    mm_entry.place(x=80, y=10)
    # 创建按钮4，用于提交密码
    button4 = tk.Button(child, text="确定", command=on_button4_click)
    button4.place(x=85, y=40)
    # 将Toplevel窗口居中显示
    center_window(child, 210, 80)

# 定义密码错误的处理函数
def on_mm_error():
    messagebox.showinfo("错误：", "密码错误！")

# 定义按钮4的点击事件处理函数
def on_button4_click():
    global mm_entry, button3, xz_entry_var  # 使用全局变量存储密码输入框和按钮的引用
    # 获取输入的密码
    mm_entry_var = mm_entry.get()
    # 检查密码是否正确
    if mm_entry_var != "114514":
        # 如果密码错误，显示错误消息并关闭Toplevel窗口
        on_mm_error()
        child.destroy()
    else:
        # 如果密码正确，更新全局变量 first_time 并更改 button3 的命令
        global first_time
        first_time = False
        button3.config(command=on_button3_second_click)
        # 清除密码输入框
        mm_entry.delete(0, tk.END)
        # 尝试读取dir_path.txt文件内容并更新文本输入框
        if os.path.exists('dir_path.txt'):
            with open('dir_path.txt', 'r', encoding='utf-8') as xz_dir:
                xz_entry_var.set(xz_dir.read().strip())  # 读取并设置文本输入框内容
        # 销毁Toplevel窗口
        child.destroy()

# 定义按钮3的第二次点击事件处理函数
def on_button3_second_click():
    try:
        # 读取保存的文件夹路径
        with open('dir_path.txt', 'r', encoding='utf-8') as xz_dir:
            xz_dir_path = xz_dir.read().strip()  # 读取并去除可能的空白字符
            # 使用系统默认程序打开文件夹
            os.startfile(xz_dir_path)
    except IOError as e:
        # 如果发生错误，显示错误消息
        messagebox.showinfo("错误：", f"发生错误：{e}")

# 定义居中显示窗口的函数
def center_window(root, width, height):
    # 获取屏幕的宽度和高度
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    # 计算窗口的位置，使其居中
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) // 2, (screenheight - height) // 2)
    # 设置窗口的几何属性
    root.geometry(size)

# 创建主窗口
root = tk.Tk()
# 将主窗口居中显示
center_window(root, 230, 80)
# 设置窗口标题
root.title("快速启动")
# 禁止调整窗口大小
root.resizable(False, False)

# 创建文本输入框的变量
xz_entry_var = tk.StringVar()
# 创建文本输入框，并放置在窗口中
xz_entry = tk.Entry(root, textvariable=xz_entry_var, width=28)
xz_entry.place(x=15, y=10)

# 创建按钮1，并绑定点击事件
button1 = tk.Button(root, text="浏览", command=on_button1_click)
button1.place(x=15, y=40)

# 创建按钮2，并绑定点击事件
button2 = tk.Button(root, text="保存", command=on_button2_click)
button2.place(x=69, y=40)

# 创建按钮3，并根据first_time变量动态设置点击事件
button3 = tk.Button(root, text="打开", width=12)
button3.place(x=122, y=40)
# 绑定按钮的点击事件，根据first_time变量的值决定调用哪个函数
button3.config(command=lambda: on_button3_first_click() if first_time else on_button3_second_click())

# 运行主循环，显示窗口
root.mainloop()