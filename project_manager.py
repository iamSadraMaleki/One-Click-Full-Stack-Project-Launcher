# project_manager.py
import subprocess
import os
import threading
import webbrowser
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime
import json
import re

class ProjectManager:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 TODO Project Manager - Ultimate Control Panel")
        self.root.geometry("1300x750")
        self.root.configure(bg='#1e1e2e')
        self.root.minsize(1200, 700)
        
        self.backend_process = None
        self.frontend_process = None
        self.backend_running = False
        self.frontend_running = False
        
        # Config file path
        self.config_file = "project_config.json"
        
        # Default values
        self.backend_bat = ""
        self.frontend_bat = ""
        self.stop_bat = ""
        self.backend_port = ""
        self.frontend_port = ""
        self.backend_path = ""
        self.frontend_path = ""
        
        # Registered status
        self.backend_registered = False
        self.frontend_registered = False
        
        # Load existing config
        self.load_config()
        
        self.setup_ui()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.backend_bat = config.get('backend_bat', '')
                    self.frontend_bat = config.get('frontend_bat', '')
                    self.stop_bat = config.get('stop_bat', '')
                    self.backend_port = config.get('backend_port', '')
                    self.frontend_port = config.get('frontend_port', '')
                    self.backend_path = config.get('backend_path', '')
                    self.frontend_path = config.get('frontend_path', '')
                    self.backend_registered = config.get('backend_registered', False)
                    self.frontend_registered = config.get('frontend_registered', False)
            except:
                pass
    
    def save_config(self):
        config = {
            'backend_bat': self.backend_bat,
            'frontend_bat': self.frontend_bat,
            'stop_bat': self.stop_bat,
            'backend_port': self.backend_port,
            'frontend_port': self.frontend_port,
            'backend_path': self.backend_path,
            'frontend_path': self.frontend_path,
            'backend_registered': self.backend_registered,
            'frontend_registered': self.frontend_registered
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2d2d3f', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🎯 TODO Project Manager", 
                font=('Arial', 18, 'bold'), bg='#2d2d3f', fg='#ffffff').pack(pady=12)
        tk.Label(header_frame, text="Batch File Registration & Service Control", 
                font=('Arial', 9), bg='#2d2d3f', fg='#a0a0c0').pack()
        
        # Main horizontal layout: Left panel (Registration) + Right panel (Log)
        main_pan = tk.Frame(self.root, bg='#1e1e2e')
        main_pan.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # ===== LEFT PANEL (Registration & Controls) =====
        left_panel = tk.Frame(main_pan, bg='#1e1e2e', width=550)
        left_panel.pack(side='left', fill='both', expand=False, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # BACKEND CARD
        backend_frame = tk.LabelFrame(left_panel, text="⚙️ BACKEND SERVICE", 
                                      bg='#2d2d3f', fg='#61afef', font=('Arial', 11, 'bold'),
                                      relief='groove', bd=2)
        backend_frame.pack(fill='x', pady=(0, 12))
        
        # Batch file row
        row1 = tk.Frame(backend_frame, bg='#2d2d3f')
        row1.pack(fill='x', padx=15, pady=(12, 5))
        tk.Label(row1, text="📁 Bat File:", bg='#2d2d3f', fg='#e5c07b', width=10, anchor='w').pack(side='left')
        self.backend_bat_entry = tk.Entry(row1, bg='#0a0a0f', fg='#abb2bf', relief='flat', width=45)
        self.backend_bat_entry.pack(side='left', padx=5)
        self.backend_bat_entry.insert(0, self.backend_bat)
        self.backend_browse_btn = tk.Button(row1, text="📂", command=self.browse_backend_bat,
                                           bg='#3d3d4f', fg='white', relief='flat', width=3)
        self.backend_browse_btn.pack(side='left')
        
        if self.backend_registered:
            self.backend_bat_entry.config(state='readonly')
            self.backend_browse_btn.config(state='disabled')
        
        # Port row
        row2 = tk.Frame(backend_frame, bg='#2d2d3f')
        row2.pack(fill='x', padx=15, pady=5)
        tk.Label(row2, text="🔌 Port:", bg='#2d2d3f', fg='#e5c07b', width=10, anchor='w').pack(side='left')
        self.backend_port_entry = tk.Entry(row2, bg='#0a0a0f', fg='#abb2bf', relief='flat', width=20)
        self.backend_port_entry.pack(side='left', padx=5)
        self.backend_port_entry.insert(0, self.backend_port)
        
        if self.backend_registered:
            self.backend_port_entry.config(state='readonly')
        
        # Path row
        row3 = tk.Frame(backend_frame, bg='#2d2d3f')
        row3.pack(fill='x', padx=15, pady=5)
        tk.Label(row3, text="📂 Path:", bg='#2d2d3f', fg='#98c379', width=10, anchor='w').pack(side='left')
        self.backend_path_label = tk.Label(row3, text=self.backend_path or "Not set", 
                                          bg='#2d2d3f', fg='#888', anchor='w')
        self.backend_path_label.pack(side='left', padx=5, fill='x', expand=True)
        
        # Register button
        self.backend_register_btn = tk.Button(backend_frame, text="✅ REGISTER & VERIFY" if not self.backend_registered else "✅ REGISTERED",
                                              command=self.register_backend,
                                              bg='#4caf50' if not self.backend_registered else '#555', 
                                              fg='white', font=('Arial', 10, 'bold'), relief='flat',
                                              state='normal' if not self.backend_registered else 'disabled')
        self.backend_register_btn.pack(pady=(8, 10))
        
        # Status indicator
        self.backend_reg_status = tk.Label(backend_frame, 
                                          text="🔴 NOT REGISTERED" if not self.backend_registered else "🟢 REGISTERED",
                                          bg='#2d2d3f', fg='#f44336' if not self.backend_registered else '#4caf50',
                                          font=('Arial', 9, 'bold'))
        self.backend_reg_status.pack(pady=(0, 10))
        
        # FRONTEND CARD
        frontend_frame = tk.LabelFrame(left_panel, text="🎨 FRONTEND SERVICE", 
                                       bg='#2d2d3f', fg='#61afef', font=('Arial', 11, 'bold'),
                                       relief='groove', bd=2)
        frontend_frame.pack(fill='x', pady=(0, 12))
        
        # Batch file row
        row1f = tk.Frame(frontend_frame, bg='#2d2d3f')
        row1f.pack(fill='x', padx=15, pady=(12, 5))
        tk.Label(row1f, text="📁 Bat File:", bg='#2d2d3f', fg='#e5c07b', width=10, anchor='w').pack(side='left')
        self.frontend_bat_entry = tk.Entry(row1f, bg='#0a0a0f', fg='#abb2bf', relief='flat', width=45)
        self.frontend_bat_entry.pack(side='left', padx=5)
        self.frontend_bat_entry.insert(0, self.frontend_bat)
        self.frontend_browse_btn = tk.Button(row1f, text="📂", command=self.browse_frontend_bat,
                                            bg='#3d3d4f', fg='white', relief='flat', width=3)
        self.frontend_browse_btn.pack(side='left')
        
        if self.frontend_registered:
            self.frontend_bat_entry.config(state='readonly')
            self.frontend_browse_btn.config(state='disabled')
        
        # Port row
        row2f = tk.Frame(frontend_frame, bg='#2d2d3f')
        row2f.pack(fill='x', padx=15, pady=5)
        tk.Label(row2f, text="🔌 Port:", bg='#2d2d3f', fg='#e5c07b', width=10, anchor='w').pack(side='left')
        self.frontend_port_entry = tk.Entry(row2f, bg='#0a0a0f', fg='#abb2bf', relief='flat', width=20)
        self.frontend_port_entry.pack(side='left', padx=5)
        self.frontend_port_entry.insert(0, self.frontend_port)
        
        if self.frontend_registered:
            self.frontend_port_entry.config(state='readonly')
        
        # Path row
        row3f = tk.Frame(frontend_frame, bg='#2d2d3f')
        row3f.pack(fill='x', padx=15, pady=5)
        tk.Label(row3f, text="📂 Path:", bg='#2d2d3f', fg='#98c379', width=10, anchor='w').pack(side='left')
        self.frontend_path_label = tk.Label(row3f, text=self.frontend_path or "Not set", 
                                           bg='#2d2d3f', fg='#888', anchor='w')
        self.frontend_path_label.pack(side='left', padx=5, fill='x', expand=True)
        
        # Register button
        self.frontend_register_btn = tk.Button(frontend_frame, text="✅ REGISTER & VERIFY" if not self.frontend_registered else "✅ REGISTERED",
                                               command=self.register_frontend,
                                               bg='#4caf50' if not self.frontend_registered else '#555', 
                                               fg='white', font=('Arial', 10, 'bold'), relief='flat',
                                               state='normal' if not self.frontend_registered else 'disabled')
        self.frontend_register_btn.pack(pady=(8, 10))
        
        # Status indicator
        self.frontend_reg_status = tk.Label(frontend_frame, 
                                           text="🔴 NOT REGISTERED" if not self.frontend_registered else "🟢 REGISTERED",
                                           bg='#2d2d3f', fg='#f44336' if not self.frontend_registered else '#4caf50',
                                           font=('Arial', 9, 'bold'))
        self.frontend_reg_status.pack(pady=(0, 10))
        
        # STOP SCRIPT CARD
        stop_frame = tk.LabelFrame(left_panel, text="🛑 STOP SCRIPT", 
                                   bg='#2d2d3f', fg='#e5c07b', font=('Arial', 10, 'bold'),
                                   relief='groove', bd=2)
        stop_frame.pack(fill='x', pady=(0, 12))
        
        stop_row = tk.Frame(stop_frame, bg='#2d2d3f')
        stop_row.pack(fill='x', padx=15, pady=10)
        tk.Label(stop_row, text="📁 Stop Bat:", bg='#2d2d3f', fg='#e5c07b', width=10, anchor='w').pack(side='left')
        self.stop_bat_entry = tk.Entry(stop_row, bg='#0a0a0f', fg='#abb2bf', relief='flat', width=40)
        self.stop_bat_entry.pack(side='left', padx=5)
        self.stop_bat_entry.insert(0, self.stop_bat)
        self.stop_browse_btn = tk.Button(stop_row, text="📂", command=self.browse_stop_bat,
                                        bg='#3d3d4f', fg='white', relief='flat', width=3)
        self.stop_browse_btn.pack(side='left')
        
        self.save_stop_btn = tk.Button(stop_frame, text="💾 SAVE STOP SCRIPT", 
                                       command=self.save_stop_script,
                                       bg='#ff9800', fg='white', relief='flat')
        self.save_stop_btn.pack(pady=(5, 10))
        
        # CONTROL BUTTONS
        ctrl_frame = tk.Frame(left_panel, bg='#1e1e2e')
        ctrl_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(ctrl_frame, text="▶ START SERVICES", 
                                   command=self.start_all,
                                   bg='#4caf50', fg='white', font=('Arial', 10, 'bold'),
                                   width=14, relief='flat',
                                   state='normal' if (self.backend_registered and self.frontend_registered) else 'disabled')
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = tk.Button(ctrl_frame, text="⏹ STOP SERVICES", 
                                  command=self.stop_all,
                                  bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
                                  width=14, relief='flat', state='disabled')
        self.stop_btn.pack(side='left', padx=5)
        
        self.open_browser_btn = tk.Button(ctrl_frame, text="🌐 OPEN BROWSER", 
                                          command=self.open_browser,
                                          bg='#ff9800', fg='white', font=('Arial', 10, 'bold'),
                                          width=14, relief='flat', state='disabled')
        self.open_browser_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(ctrl_frame, text="🔄 RESET", 
                                   command=self.reset_registration,
                                   bg='#9c27b0', fg='white', font=('Arial', 10, 'bold'),
                                   width=10, relief='flat')
        self.reset_btn.pack(side='left', padx=5)
        
        # STATUS INDICATORS (compact)
        status_frame = tk.Frame(left_panel, bg='#2d2d3f')
        status_frame.pack(fill='x', pady=10)
        
        # Backend live status
        self.backend_led = tk.Label(status_frame, text="●", font=('Arial', 14), fg='#555', bg='#2d2d3f')
        self.backend_led.pack(side='left', padx=15)
        self.backend_status = tk.Label(status_frame, text="BACKEND: STOPPED", 
                                       font=('Arial', 9, 'bold'), fg='#888', bg='#2d2d3f')
        self.backend_status.pack(side='left', padx=5)
        self.backend_port_label = tk.Label(status_frame, text="", font=('Arial', 9), fg='#666', bg='#2d2d3f')
        self.backend_port_label.pack(side='left', padx=10)
        
        # Frontend live status
        self.frontend_led = tk.Label(status_frame, text="●", font=('Arial', 14), fg='#555', bg='#2d2d3f')
        self.frontend_led.pack(side='left', padx=15)
        self.frontend_status = tk.Label(status_frame, text="FRONTEND: STOPPED", 
                                        font=('Arial', 9, 'bold'), fg='#888', bg='#2d2d3f')
        self.frontend_status.pack(side='left', padx=5)
        self.frontend_port_label = tk.Label(status_frame, text="", font=('Arial', 9), fg='#666', bg='#2d2d3f')
        self.frontend_port_label.pack(side='left', padx=10)
        
        # ===== RIGHT PANEL (LOG) =====
        right_panel = tk.Frame(main_pan, bg='#1e1e2e')
        right_panel.pack(side='right', fill='both', expand=True)
        
        log_header = tk.Frame(right_panel, bg='#2d2d3f')
        log_header.pack(fill='x')
        
        tk.Label(log_header, text="📋 CONSOLE LOG", 
                font=('Arial', 10, 'bold'), bg='#2d2d3f', fg='#61afef').pack(side='left', padx=10, pady=8)
        
        clear_btn = tk.Button(log_header, text="🗑 CLEAR", command=self.clear_log,
                             bg='#3d3d4f', fg='#ccc', font=('Arial', 9), relief='flat')
        clear_btn.pack(side='right', padx=10)
        
        self.log_area = scrolledtext.ScrolledText(right_panel, 
                                                  font=('Consolas', 9),
                                                  bg='#0a0a0f', fg='#abb2bf',
                                                  insertbackground='#abb2bf',
                                                  relief='flat', wrap='word')
        self.log_area.pack(fill='both', expand=True)
        
        # Configure log tags
        self.log_area.tag_config('success', foreground='#98c379')
        self.log_area.tag_config('error', foreground='#e06c75')
        self.log_area.tag_config('warning', foreground='#e5c07b')
        self.log_area.tag_config('info', foreground='#61afef')
        
        self.add_log("═══════════════════════════════════════════════════════════", 'info')
        self.add_log("🚀 PROJECT MANAGER INITIALIZED", 'success')
        self.add_log("═══════════════════════════════════════════════════════════", 'info')
        
        if self.backend_registered:
            self.add_log(f"✅ Backend already registered", 'success')
            self.backend_port_label.config(text=f"Port: {self.backend_port}")
        if self.frontend_registered:
            self.add_log(f"✅ Frontend already registered", 'success')
            self.frontend_port_label.config(text=f"Port: {self.frontend_port}")
            
        if not self.backend_registered or not self.frontend_registered:
            self.add_log("📝 Please register your batch files and ports first", 'warning')
        
        self.update_status()
        
    def browse_backend_bat(self):
        filename = filedialog.askopenfilename(title="Select Backend Batch File", 
                                               filetypes=[("Batch files", "*.bat")])
        if filename:
            self.backend_bat_entry.delete(0, tk.END)
            self.backend_bat_entry.insert(0, filename)
            self.extract_path_from_bat(filename, 'backend')
            
    def browse_frontend_bat(self):
        filename = filedialog.askopenfilename(title="Select Frontend Batch File", 
                                               filetypes=[("Batch files", "*.bat")])
        if filename:
            self.frontend_bat_entry.delete(0, tk.END)
            self.frontend_bat_entry.insert(0, filename)
            self.extract_path_from_bat(filename, 'frontend')
            
    def browse_stop_bat(self):
        filename = filedialog.askopenfilename(title="Select Stop Script", 
                                               filetypes=[("Batch files", "*.bat")])
        if filename:
            self.stop_bat_entry.delete(0, tk.END)
            self.stop_bat_entry.insert(0, filename)
            
    def save_stop_script(self):
        stop_bat = self.stop_bat_entry.get().strip()
        if stop_bat and os.path.exists(stop_bat):
            self.stop_bat = stop_bat
            self.save_config()
            self.add_log(f"✅ Stop script saved: {stop_bat}", 'success')
        elif stop_bat:
            self.add_log(f"❌ Stop script not found", 'error')
        else:
            self.add_log("ℹ️ No stop script selected (optional)", 'info')
            
    def extract_path_from_bat(self, bat_file, service):
        try:
            with open(bat_file, 'r', encoding='utf-8') as f:
                content = f.read()
                cd_match = re.search(r'cd /d "([^"]+)"', content)
                if cd_match:
                    path = cd_match.group(1)
                    if service == 'backend':
                        self.backend_path = path
                        self.backend_path_label.config(text=path, fg='#98c379')
                    else:
                        self.frontend_path = path
                        self.frontend_path_label.config(text=path, fg='#98c379')
                    self.add_log(f"📂 Extracted {service} path: {path}", 'info')
        except Exception as e:
            self.add_log(f"⚠️ Could not extract path: {str(e)}", 'warning')
            
    def register_backend(self):
        bat_file = self.backend_bat_entry.get().strip()
        port = self.backend_port_entry.get().strip()
        
        if not bat_file or not port:
            messagebox.showerror("Error", "Please select batch file and enter port")
            return
        if not os.path.exists(bat_file):
            messagebox.showerror("Error", f"Batch file not found")
            return
            
        try:
            with open(bat_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.add_log(f"✅ Batch file verified ({len(content)} bytes)", 'success')
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read batch file: {str(e)}")
            return
            
        self.backend_bat = bat_file
        self.backend_port = port
        self.backend_registered = True
        self.save_config()
        
        self.backend_bat_entry.config(state='readonly')
        self.backend_port_entry.config(state='readonly')
        self.backend_browse_btn.config(state='disabled')
        self.backend_register_btn.config(text="✅ REGISTERED", bg='#555', state='disabled')
        self.backend_reg_status.config(text="🟢 REGISTERED", fg='#4caf50')
        self.backend_port_label.config(text=f"Port: {port}")
        
        if self.frontend_registered:
            self.start_btn.config(state='normal')
            
        self.add_log(f"✅ Backend registered | Port: {port}", 'success')
        messagebox.showinfo("Success", f"Backend registered!\nPort: {port}")
        
    def register_frontend(self):
        bat_file = self.frontend_bat_entry.get().strip()
        port = self.frontend_port_entry.get().strip()
        
        if not bat_file or not port:
            messagebox.showerror("Error", "Please select batch file and enter port")
            return
        if not os.path.exists(bat_file):
            messagebox.showerror("Error", f"Batch file not found")
            return
            
        try:
            with open(bat_file, 'r', encoding='utf-8') as f:
                content = f.read()
                self.add_log(f"✅ Batch file verified ({len(content)} bytes)", 'success')
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read batch file: {str(e)}")
            return
            
        self.frontend_bat = bat_file
        self.frontend_port = port
        self.frontend_registered = True
        self.save_config()
        
        self.frontend_bat_entry.config(state='readonly')
        self.frontend_port_entry.config(state='readonly')
        self.frontend_browse_btn.config(state='disabled')
        self.frontend_register_btn.config(text="✅ REGISTERED", bg='#555', state='disabled')
        self.frontend_reg_status.config(text="🟢 REGISTERED", fg='#4caf50')
        self.frontend_port_label.config(text=f"Port: {port}")
        
        if self.backend_registered:
            self.start_btn.config(state='normal')
            
        self.add_log(f"✅ Frontend registered | Port: {port}", 'success')
        messagebox.showinfo("Success", f"Frontend registered!\nPort: {port}")
        
    def reset_registration(self):
        if messagebox.askyesno("Reset", "Clear all registered batch files and ports?"):
            self.backend_registered = False
            self.frontend_registered = False
            self.backend_bat = ""
            self.frontend_bat = ""
            self.backend_port = ""
            self.frontend_port = ""
            self.backend_path = ""
            self.frontend_path = ""
            self.save_config()
            
            # Reset UI
            self.backend_bat_entry.config(state='normal')
            self.backend_bat_entry.delete(0, tk.END)
            self.backend_port_entry.config(state='normal')
            self.backend_port_entry.delete(0, tk.END)
            self.backend_path_label.config(text="Not set", fg='#888')
            self.backend_browse_btn.config(state='normal')
            self.backend_register_btn.config(text="✅ REGISTER & VERIFY", bg='#4caf50', state='normal')
            self.backend_reg_status.config(text="🔴 NOT REGISTERED", fg='#f44336')
            self.backend_port_label.config(text="")
            
            self.frontend_bat_entry.config(state='normal')
            self.frontend_bat_entry.delete(0, tk.END)
            self.frontend_port_entry.config(state='normal')
            self.frontend_port_entry.delete(0, tk.END)
            self.frontend_path_label.config(text="Not set", fg='#888')
            self.frontend_browse_btn.config(state='normal')
            self.frontend_register_btn.config(text="✅ REGISTER & VERIFY", bg='#4caf50', state='normal')
            self.frontend_reg_status.config(text="🔴 NOT REGISTERED", fg='#f44336')
            self.frontend_port_label.config(text="")
            
            self.start_btn.config(state='disabled')
            self.add_log("🔄 All registrations have been reset", 'warning')
            
    def add_log(self, message, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        if tag:
            self.log_area.insert(tk.END, log_message, tag)
        else:
            if '✅' in message or 'SUCCESS' in message:
                self.log_area.insert(tk.END, log_message, 'success')
            elif '❌' in message or 'ERROR' in message:
                self.log_area.insert(tk.END, log_message, 'error')
            elif '⚠️' in message or 'WARNING' in message:
                self.log_area.insert(tk.END, log_message, 'warning')
            else:
                self.log_area.insert(tk.END, log_message, 'info')
        self.log_area.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        self.log_area.delete(1.0, tk.END)
        self.add_log("📋 Console cleared", 'info')
        
    def update_status(self):
        self.backend_led.config(fg='#4caf50' if self.backend_running else '#555')
        self.backend_status.config(text="BACKEND: RUNNING" if self.backend_running else "BACKEND: STOPPED",
                                   fg='#4caf50' if self.backend_running else '#888')
        self.frontend_led.config(fg='#4caf50' if self.frontend_running else '#555')
        self.frontend_status.config(text="FRONTEND: RUNNING" if self.frontend_running else "FRONTEND: STOPPED",
                                    fg='#4caf50' if self.frontend_running else '#888')
        
    def open_browser(self):
        if not self.frontend_running:
            messagebox.showwarning("Warning", "Frontend is not running!")
            return
        url = f"http://localhost:{self.frontend_port}/"
        self.add_log(f"🌐 Opening: {url}", 'info')
        try:
            os.system(f'start {url}')
            self.add_log("✅ Browser opened", 'success')
        except:
            webbrowser.open(url)
        
    def start_all(self):
        if not self.backend_registered or not self.frontend_registered:
            messagebox.showerror("Error", "Please register both services first!")
            return
            
        self.add_log("══════════════════════════════════════════════", 'info')
        self.add_log("🚀 Starting services...", 'success')
        
        try:
            self.backend_process = subprocess.Popen(
                ["cmd", "/c", self.backend_bat],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            threading.Thread(target=self.read_output, args=(self.backend_process, "BACKEND"), daemon=True).start()
            self.backend_running = True
            self.update_status()
            self.add_log("✅ Backend started", 'success')
        except Exception as e:
            self.add_log(f"❌ Backend failed: {str(e)}", 'error')
            return
        
        self.add_log("⏳ Waiting 5s for backend...", 'warning')
        self.root.after(5000, self.start_frontend)
        
    def start_frontend(self):
        try:
            self.frontend_process = subprocess.Popen(
                ["cmd", "/c", self.frontend_bat],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            threading.Thread(target=self.read_output, args=(self.frontend_process, "FRONTEND"), daemon=True).start()
            self.frontend_running = True
            self.update_status()
            self.add_log("✅ Frontend started", 'success')
            
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.open_browser_btn.config(state="normal")
            
            self.add_log(f"🌐 Frontend: http://localhost:{self.frontend_port}", 'info')
            self.add_log(f"🔙 Backend API: http://localhost:{self.backend_port}", 'info')
            self.add_log("🎉 ALL SERVICES STARTED!", 'success')
            
            self.root.after(2000, self.auto_open_browser)
        except Exception as e:
            self.add_log(f"❌ Frontend failed: {str(e)}", 'error')
    
    def auto_open_browser(self):
        if self.frontend_running:
            self.open_browser()
        
    def read_output(self, process, name):
        for line in iter(process.stdout.readline, ''):
            if line:
                self.root.after(0, self.add_log, f"[{name}] {line.strip()}")
            if (name == "BACKEND" and not self.backend_running) or (name == "FRONTEND" and not self.frontend_running):
                break
                
    def stop_all(self):
        self.add_log("══════════════════════════════════════════════", 'warning')
        self.add_log("🛑 Stopping services...", 'warning')
        
        if self.stop_bat and os.path.exists(self.stop_bat):
            try:
                subprocess.run(["cmd", "/c", self.stop_bat], capture_output=True, timeout=10)
                self.add_log("✅ Stop script executed", 'success')
            except:
                pass
        
        os.system("taskkill /F /IM java.exe 2>nul")
        os.system("taskkill /F /IM node.exe 2>nul")
        
        self.backend_running = False
        self.frontend_running = False
        self.update_status()
        self.start_btn.config(state="normal" if (self.backend_registered and self.frontend_registered) else "disabled")
        self.stop_btn.config(state="disabled")
        self.open_browser_btn.config(state="disabled")
        
        self.add_log("✅ All services stopped", 'success')
        
    def on_closing(self):
        if self.backend_running or self.frontend_running:
            if messagebox.askyesno("Exit", "Services are running! Stop them?"):
                self.stop_all()
                self.root.after(500, self.root.destroy)
            else:
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManager(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()