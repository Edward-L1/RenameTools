import os
import sys
import re
import random
import string
from collections import defaultdict
from xml.etree import ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading

class RenameToolGUI:
    # init函数
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Android 资源批量重命名工具")
        self.win.geometry("800x800")
        
        # ========== 根目录设置 ==========
        self.main_frame = ttk.Frame(self.win, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.setup_root_dir_section()
        # ========== 包体选择 ==========
        self.setup_package_select_section()
        # ========== 重命名模式 ==========
        self.setup_rename_mode_section()
        # ========== 操作按钮 ==========
        self.setup_action_buttons()
        # ========== 日志输出区 ==========
        self.setup_log_console()

    # 根目录选择触发逻辑，依据是否存在
    def setup_root_dir_section(self):
        root_frame = ttk.LabelFrame(self.main_frame, text="项目根目录设置", padding="5")
        root_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.root_dir_var = tk.StringVar()
        entry = ttk.Entry(root_frame, textvariable=self.root_dir_var, width=60)
        entry.grid(row=0, column=0, padx=5)
        ttk.Button(root_frame, text="选择目录", command=self.select_root_dir).grid(row=0, column=1)
        self.path_status_label = ttk.Label(root_frame, text="")
        self.path_status_label.grid(row=0, column=2, padx=5)

        entry.bind("<FocusOut>", lambda e: self.on_root_dir_change())
        entry.bind("<KeyRelease>", lambda e: self.on_root_dir_change())

    # 根目录选择触发逻辑刷新
    def select_root_dir(self):
        path = filedialog.askdirectory(title="选择项目根目录")
        if path:
            self.root_dir_var.set(path)
            self.validate_path(path)
            if hasattr(self, 'refresh_package_checkbuttons'):
                self.refresh_package_checkbuttons()

    def validate_path(self, path):
        if os.path.exists(os.path.join(path, "app/src/main/res")):
            self.path_status_label.config(text="✓ 路径正确", foreground="green")
            return True
        else:
            self.path_status_label.config(text="✗ 路径错误", foreground="red")
            return False
    
    def on_root_dir_change(self):
        path = self.root_dir_var.get()
        self.validate_path(path)
        if hasattr(self, 'refresh_package_checkbuttons'):
            self.refresh_package_checkbuttons()

    # ========== 包体选择区 ==========
    def setup_package_select_section(self):
        package_frame = ttk.LabelFrame(self.main_frame, text="选择包体（可多选，app包体默认勾选）", padding="5")
        package_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.package_check_vars = {}
        self.package_check_buttons = {}
        self.package_dirs = []
        self.package_frame = package_frame
        # 预留区域，初始化时就显示
        self.refresh_package_checkbuttons()

    def refresh_package_checkbuttons(self):
        # 清空旧的
        for widget in self.package_frame.winfo_children():
            widget.destroy()
        root_dir = self.root_dir_var.get()
        if not root_dir or not os.path.isdir(root_dir):
            self.package_dirs = []
            # 预留占位
            tk.Label(self.package_frame, text="暂无可用包体，请先选择有效项目根目录", foreground="gray").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            return
        self.package_dirs = self.scan_package_dirs(root_dir)
        self.package_dirs.sort(key=lambda x: x.lower())  # 按首字母排序（不区分大小写）
        if not self.package_dirs:
            tk.Label(self.package_frame, text="未检测到包体", foreground="gray").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
            return
        for idx, pkg in enumerate(self.package_dirs):
            check_var = tk.BooleanVar(value=(pkg == "app"))
            check = tk.Checkbutton(self.package_frame, text=pkg, variable=check_var)
            check.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
            self.package_check_vars[pkg] = check_var
            self.package_check_buttons[pkg] = check

    def get_selected_packages(self):
        # 返回所有勾选的包体
        return [pkg for pkg, var in self.package_check_vars.items() if var.get()]

    # 重命名模式选择
    def setup_rename_mode_section(self):
        mode_frame = ttk.LabelFrame(self.main_frame, text="重命名模式", padding="5")
        mode_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(mode_frame, text="前缀:").grid(row=0, column=0, padx=5)
        self.prefix_var = tk.StringVar(value="prefix")
        self.prefix_entry = ttk.Entry(mode_frame, textvariable=self.prefix_var, width=20)
        self.prefix_entry.grid(row=0, column=1, padx=5)

        self.first_letter_mode = tk.BooleanVar(value=False)
        self.first_letter_check = ttk.Checkbutton(
            mode_frame, text="启用首字母模式", variable=self.first_letter_mode, command=self.update_rename_example
        )
        self.first_letter_check.grid(row=0, column=2, padx=5)

        self.example_label = ttk.Label(mode_frame, text="")
        self.example_label.grid(row=0, column=3, padx=10)

        self.prefix_var.trace_add("write", lambda *args: self.update_rename_example())
        self.update_rename_example()
    def update_rename_example(self):
        prefix = self.prefix_var.get()
        example_src = "app_name"
        if self.first_letter_mode.get():
            example_dst = f"{prefix}_{'_'.join([w[0] for w in example_src.split('_')])}"
        else:
            example_dst = f"{prefix}_{example_src}"
        self.example_label.config(text=f"示例: '{example_src}' → '{example_dst}'")

    # 动作按钮
    def setup_action_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.rename_btn = ttk.Button(button_frame, text="开始重命名", command=self.start_rename)
        self.rename_btn.grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="退出", command=self.win.quit).grid(row=0, column=1, padx=5)

    # 运行
    def run(self):
        self.win.mainloop()

    # 防止重命名重复设置
    def generate_unique_name(self, base_name, existing_names):
        unique_name = base_name
        count = 0
        # 如果之后仍然重复，只增加随机字母
        while unique_name in existing_names:
            if (count == 0):
                unique_name += "_"
            unique_name += random.choice(string.ascii_lowercase)
            count+=1
        return unique_name

    # 重命名文件名，fileType 参数的作用是指定要重命名的文件所在的目录的前缀， 生成一个字典用于存储原始文件名和新文件名的映射关系。
    def rename_files(self, directories, fileType):
        rename_counter = defaultdict(int)
        rename_map = {}
        
        self.log(f"开始处理 {fileType} 类型文件")
        self.log(f"处理目录: {directories}")
        
        # 递归遍历每个资源目录及其子目录中的所有文件
        for directory in directories:
            if not os.path.exists(directory):
                self.log(f"目录不存在: {directory}")
                continue
            
            self.log(f"正在处理目录: {directory}")
            for root, dirs, files in os.walk(directory):
                if os.path.basename(root).startswith(fileType):
                    self.log(f"开始重命名目录: {root}")
                    
                    xml_files = [f for f in files if (f.endswith('.xml') | f.endswith('.png') | f.endswith('.jpg') | f.endswith('.jpeg'))]
                    for filename in xml_files:
                        base_name = os.path.splitext(filename)[0]
                        # 修改这里：使用目录名而不是完整路径
                        dir_name = os.path.basename(directory)
                        if self.first_letter_mode.get():
                            abbr = '_'.join([w[0] for w in base_name.split('_') if w])
                            new_name = self.prefix_var.get() + "_" + abbr
                        else:
                            new_name = self.prefix_var.get() + "_" + base_name

                        # 如果该文件名已经在映射关系中，直接使用已有的映射
                        if base_name in rename_map:
                            new_name = rename_map[base_name]
                            self.log(f"使用已有映射: {base_name} -> {new_name}")
                        else:
                            # 只有新文件名才需要检查唯一性
                            new_name = self.generate_unique_name(new_name, rename_map.values())
                            rename_map[base_name] = new_name
                            self.log(f"创建新映射: {base_name} -> {new_name}")

                        new_filename = new_name + os.path.splitext(filename)[1]
                        old_file_path = os.path.join(root, filename)
                        new_file_path = os.path.join(root, new_filename)

                        self.log(f"重命名文件: {old_file_path} -> {new_file_path}")
                        try:
                            os.rename(old_file_path, new_file_path)
                        except Exception as e:
                            self.log(f"重命名失败: {str(e)}")
        
        return rename_map

    # 传入文件夹路径，遍历后重命名以strings 开头的 XML 文件
    def rename_string_resources(self, directories):
        rename_map = {}
        # 第一步：收集所有字符串资源名称，建立统一的映射关系
        all_string_names = set()
        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.startswith('strings') and file.endswith('.xml'):
                        file_path = os.path.join(root, file)
                        tree = ET.parse(file_path)
                        root_element = tree.getroot()
                        for string_element in root_element.findall('string'):
                            name = string_element.get('name')
                            if name:
                                all_string_names.add(name)
        
        # 第二步：为所有字符串资源生成统一的映射关系
        for name in sorted(all_string_names):
            # 优先使用app目录的名称作为前缀，如果没有app目录则使用第一个目录
            prefix_dir = None
            for directory in directories:
                if 'app' in directory:
                    prefix_dir = directory
                    break
            if not prefix_dir:
                prefix_dir = directories[0]
                
            dir_name = os.path.basename(prefix_dir)
            if self.first_letter_mode.get():
                abbr = '_'.join([w[0] for w in name.split('_') if w])
                new_name = self.prefix_var.get() + "_" + abbr
            else:
                new_name = self.prefix_var.get() + "_" + name
            
            # 检查唯一性，避免与已生成的名称冲突
            new_name = self.generate_unique_name(new_name, rename_map.values())
            rename_map[name] = new_name
            
            # 如果是 app 包下的 app_name，则存储其新名称
            if name == 'app_name':
                rename_map[name] = 'app_name'
        
        # 第三步：应用映射关系到所有文件
        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.startswith('strings') and file.endswith('.xml'):
                        file_path = os.path.join(root, file)
                        tree = ET.parse(file_path)
                        root_element = tree.getroot()
                        
                        for string_element in root_element.findall('string'):
                            name = string_element.get('name')
                            if name and name in rename_map:
                                new_name = rename_map[name]
                                string_element.set('name', new_name)
                                self.log(f'Renaming {name} to {new_name} in {file_path}')
                        
                        tree.write(file_path, encoding='utf-8', xml_declaration=True)

        return rename_map

    # 专门处理Binding类名替换的函数
    def update_binding_classes(self, src_directory, layout_rename_map):
        """专门处理Binding类名的替换，避免重复替换"""
        for root, dirs, files in os.walk(src_directory):
            for file in files:
                if file.endswith('.java') or file.endswith('.kt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    updated_content = content
                    
                    # 按原始名称排序，确保替换顺序一致
                    for old_name, new_name in sorted(layout_rename_map.items()):
                        old_binding_class = ''.join(word.capitalize() for word in old_name.split('_')) + 'Binding'
                        new_binding_class = ''.join(word.capitalize() for word in new_name.split('_')) + 'Binding'
                        
                        # 使用单词边界确保精确匹配
                        updated_content = re.sub(r'\b' + re.escape(old_binding_class) + r'\b', new_binding_class, updated_content)

                    if updated_content != content:
                        self.log(f'Updating Binding classes in {file_path}')
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated_content)

    # 更新引用，遍历指定的源代码目录， 找到所有 .java、.kt 和 .xml 文件，并将其中对旧资源文件名的引用替换为新的文件名。
    # src_directory: 源代码目录的路径。代码会遍历该目录及其子目录， 找到所有 .java、.kt 和 .xml 文件。
    # rename_map: 一个字典，包含旧文件名和新文件名的映射关系。 代码会使用该字典来更新代码中对资源文件的引用。
    # refType: 资源类型，例如 "string" 或 "layout"。代码会根据该参数来确定要更新哪些类型的资源引用。 例如， 如果 refType 为 "string"，则代码会更新对字符串资源的引用；如果 refType 为 "layout"，则代码会更新对布局资源的引用，并更新 Data Binding 类名的引用。
    def update_references(self, src_directory, rename_map, refType):
        for root, dirs, files in os.walk(src_directory):
            for file in files:
                if file.endswith('.java') or file.endswith('.kt') or file.endswith('.xml'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    updated_content = content
                    
                    for old_name, new_name in rename_map.items():
                        # 始终使用 app 包下 app_name 的新名称进行替换
                        if old_name == 'app_name':
                            updated_content = re.sub(r'(@' + refType + r'/)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)
                            updated_content = re.sub(r'(R\.' + refType + r'\.)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)
                        else:
                            # 更新 @string 和 R.string 的引用
                            updated_content = re.sub(r'(@' + refType + r'/)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)
                            updated_content = re.sub(r'(R\.' + refType + r'\.)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)

                        # 更新 @layout 和 R.layout 的引用
                        # updated_content = re.sub(r'(@'+fileType+'/)' + old_name, r'\1' + new_name, updated_content)
                        # updated_content = re.sub(r'(R\.'+fileType+'\.)' + old_name, r'\1' + new_name, updated_content)
                        if (refType == "layout"):
                            # 移除Binding类名替换逻辑，避免重复替换
                            updated_content = re.sub(r'(@drawable/)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)

                    if updated_content != content:
                        self.log(f'Updating references in {file_path}')
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(updated_content)
                    
    def update_manifest(self, file_path, rename_map, refType):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content = content
                    
        for old_name, new_name in rename_map.items():

                updated_content = re.sub(r'(@' + refType + r'/)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)
                updated_content = re.sub(r'(R\.' + refType + r'\.)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)
                
                if (refType == "layout"):
                    # 更新 Binding 类名
                    old_binding_class = ''.join(word.capitalize() for word in old_name.split('_')) + 'Binding'
                    new_binding_class = ''.join(word.capitalize() for word in new_name.split('_')) + 'Binding'
                    updated_content = re.sub(old_binding_class, new_binding_class, updated_content)
                    updated_content = re.sub(r'(@drawable/)' + re.escape(old_name) + r'\b', r'\1' + new_name, updated_content)


        if updated_content != content:
            self.log(f'Updating references in {file_path}')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                    
    def get_related_values_dirs(self, selected_values_dirs):
        """获取与选中的values目录同源的多语言文件夹"""
        related_dirs = []
        root_dir = self.root_dir_var.get()
        
        for values_dir in selected_values_dirs:
            # 将相对路径转换为绝对路径
            abs_values_dir = os.path.join(root_dir, values_dir)
            if not os.path.exists(abs_values_dir):
                continue
                
            # 获取values目录的父目录（res目录）
            res_dir = os.path.dirname(abs_values_dir)
            if not os.path.exists(res_dir):
                continue
                
            # 查找同源的多语言文件夹
            for item in os.listdir(res_dir):
                item_path = os.path.join(res_dir, item)
                if os.path.isdir(item_path) and item.startswith("values-"):
                    # 生成相对路径
                    rel_path = os.path.relpath(item_path, root_dir)
                    related_dirs.append(rel_path)
                    self.log(f"找到同源多语言文件夹: {rel_path}")
        
        return related_dirs

    def get_selected_mother_dirs(self, res_type):
        # 返回所选的母本目录绝对路径列表
        listbox = self.mapping_listboxes[res_type]
        return [listbox.get(i) for i in listbox.curselection()]

    def scan_package_dirs(self, root_dir):
        """扫描根目录下所有含有/src/main/AndroidManifest.xml的包体文件夹"""
        package_dirs = []
        for name in os.listdir(root_dir):
            abs_path = os.path.join(root_dir, name)
            if os.path.isdir(abs_path):
                manifest = os.path.join(abs_path, "src", "main", "AndroidManifest.xml")
                if os.path.exists(manifest):
                    package_dirs.append(name)
        return package_dirs

    # 开始重命名
    def start_rename(self):
        self.rename_btn.config(state=tk.DISABLED)
        self.win.update_idletasks()
        threading.Thread(target=self.do_rename, daemon=True).start()

    def do_rename(self):
        try:
            root_dir = self.root_dir_var.get()
            if not os.path.isdir(root_dir):
                self.safe_log("项目根目录不存在")
                self.safe_messagebox("提示", "项目根目录不存在")
                return

            selected_packages = self.get_selected_packages()
            if not selected_packages:
                self.safe_log("请至少选择一个包体")
                self.safe_messagebox("提示", "请至少选择一个包体")
                return

            self.safe_log(f"本次处理包体: {selected_packages}")

            for pkg in selected_packages:
                pkg_path = os.path.join(root_dir, pkg)
                self.safe_log(f"处理包体: {pkg_path}")
                self.process_package(pkg_path)

            self.safe_messagebox("提示", f"本次处理包体: {selected_packages}，重命名处理完成！")
        finally:
            self.win.after(0, lambda: self.rename_btn.config(state=tk.NORMAL))

    def safe_log(self, msg):
        self.win.after(0, lambda: self.log(msg))

    def safe_messagebox(self, title, msg):
        self.win.after(0, lambda: messagebox.showinfo(title, msg))

    def process_package(self, package_path):
        self.log(f"开始处理包体: {package_path}")
        if not os.path.isdir(package_path):
            self.log(f"包体不存在: {package_path}")
            return

        src_dir = os.path.join(package_path, 'src')
        if not os.path.isdir(src_dir):
            self.log(f"src目录不存在: {src_dir}")
            return

        # 1. 收集所有渠道目录（main、gp、cn、huawei...）
        channel_dirs = []
        for d in os.listdir(src_dir):
            abs_path = os.path.join(src_dir, d)
            if os.path.isdir(abs_path):
                channel_dirs.append(abs_path)
        channel_dirs.sort(key=lambda x: (x != os.path.join(src_dir, 'main'), x))  # main优先

        # 2. 收集所有资源母本目录
        all_string_dirs, all_drawable_dirs, all_layout_dirs = [], [], []
        for channel_dir in channel_dirs:
            res_root = os.path.join(channel_dir, 'res')
            if not os.path.isdir(res_root):
                continue
            # values/values-xx
            for d in os.listdir(res_root):
                if d == 'values' or d.startswith('values-'):
                    all_string_dirs.append(os.path.join(res_root, d))
                if d == 'drawable' or d == 'drawable-xxhdpi' or (d.startswith('drawable-') and d != 'drawable-xxhdpi'):
                    all_drawable_dirs.append(os.path.join(res_root, d))
                if d.startswith('layout'):
                    all_layout_dirs.append(os.path.join(res_root, d))

        self.log(f"所有string母本目录: {all_string_dirs}")
        self.log(f"所有drawable母本目录: {all_drawable_dirs}")
        self.log(f"所有layout母本目录: {all_layout_dirs}")

        # 3. 先处理main，建立映射，再处理其他渠道，遇到同名直接用已有映射
        # 你可以仿照rename_string_resources的逻辑，先遍历main的strings，建立rename_map，再遍历其他渠道的strings，遇到新名字才新建映射

        # 4. 资源文件重命名
        rename_draw_map = self.rename_files(all_drawable_dirs, 'drawable')
        rename_layout_map = self.rename_files(all_layout_dirs, 'layout')
        rename_string_map = self.rename_string_resources(all_string_dirs)

        # 5. 更新引用（仅处理当前包体下的java/kt/xml/AndroidManifest.xml）
        update_dirs = []
        for dirpath, dirnames, filenames in os.walk(package_path):
            if any(d in dirpath for d in ['/java/', '/res/', '/AndroidManifest.xml']):
                update_dirs.append(dirpath)
        self.log(f"需要更新的目录：{update_dirs}")
        for dir_path in update_dirs:
            if os.path.basename(dir_path) == 'AndroidManifest.xml':
                self.log(f"更新 AndroidManifest.xml: {dir_path}")
                self.update_manifest(dir_path, rename_draw_map, "drawable")
                self.update_manifest(dir_path, rename_string_map, "string")
                self.update_manifest(dir_path, rename_layout_map, "layout")
                continue
            if os.path.isdir(dir_path):
                self.log(f"更新目录: {dir_path}")
                self.update_references(dir_path, rename_draw_map, "drawable")
                self.update_references(dir_path, rename_string_map, "string")
                self.update_references(dir_path, rename_layout_map, "layout")
        # 6. Binding类名替换
        self.log("开始处理Binding类名替换...")
        for dir_path in update_dirs:
            if os.path.isdir(dir_path):
                self.update_binding_classes(dir_path, rename_layout_map)
        self.log(f"包体处理完成: {package_path}")

    def setup_log_console(self):
        log_frame = ttk.LabelFrame(self.main_frame, text="日志输出", padding="5")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.log_text = tk.Text(log_frame, height=12, state="disabled")
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.win.update_idletasks()

if __name__ == "__main__":
    app = RenameToolGUI()
    app.run()