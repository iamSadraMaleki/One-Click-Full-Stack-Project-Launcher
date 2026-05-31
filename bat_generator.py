import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                             QLineEdit, QPushButton, QFileDialog, 
                             QMessageBox, QVBoxLayout, QHBoxLayout, QGroupBox)
from PyQt5.QtCore import Qt

class BatGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bat File Generator ")
        self.setFixedSize(700, 400)
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ========== بخش فرانت ==========
        frontend_group = QGroupBox("🚀 فرانت‌اند (Frontend)")
        frontend_layout = QVBoxLayout()
        
        frontend_path_layout = QHBoxLayout()
        self.frontend_input = QLineEdit()
        self.frontend_input.setPlaceholderText("مثال: T:/Project/TODO_V1/Source Code/Frontend/todo_app")
        frontend_path_layout.addWidget(QLabel("📁 آدرس پروژه فرانت:"))
        frontend_path_layout.addWidget(self.frontend_input)
        
        self.frontend_btn = QPushButton("🔨 ساخت start_frontend.bat")
        self.frontend_btn.clicked.connect(self.generate_frontend_bat)
        
        frontend_layout.addLayout(frontend_path_layout)
        frontend_layout.addWidget(self.frontend_btn)
        frontend_group.setLayout(frontend_layout)
        
        # ========== بخش بک‌اند ==========
        backend_group = QGroupBox("⚙️ بک‌اند (Backend - Spring Boot)")
        backend_layout = QVBoxLayout()
        
        backend_path_layout = QHBoxLayout()
        self.backend_input = QLineEdit()
        self.backend_input.setPlaceholderText("مثال: T:/Project/TODO_V1/Source Code/Backend/project")
        backend_path_layout.addWidget(QLabel("📁 آدرس پروژه بک‌اند:"))
        backend_path_layout.addWidget(self.backend_input)
        
        self.backend_btn = QPushButton("🔨 ساخت start_backend.bat")
        self.backend_btn.clicked.connect(self.generate_backend_bat)
        
        backend_layout.addLayout(backend_path_layout)
        backend_layout.addWidget(self.backend_btn)
        backend_group.setLayout(backend_layout)
        
        # ========== بخش ذخیره‌سازی ==========
        save_group = QGroupBox("💾 انتخاب مقصد ذخیره فایل‌های bat")
        save_layout = QHBoxLayout()
        
        self.save_path_input = QLineEdit()
        self.save_path_input.setPlaceholderText("مسیر ذخیره batها رو انتخاب کن...")
        self.browse_btn = QPushButton("📂 انتخاب مسیر")
        self.browse_btn.clicked.connect(self.browse_save_folder)
        
        save_layout.addWidget(self.save_path_input)
        save_layout.addWidget(self.browse_btn)
        save_group.setLayout(save_layout)
        
        # دکمه ساخت هر دو با هم
        self.both_btn = QPushButton("🔥 ساخت هر دو فایل با هم")
        self.both_btn.clicked.connect(self.generate_both)
        
        layout.addWidget(frontend_group)
        layout.addWidget(backend_group)
        layout.addWidget(save_group)
        layout.addWidget(self.both_btn)
        
        # استایل ساده
        self.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px 0 5px; }
            QPushButton { background-color: #4CAF50; color: white; border: none; padding: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #45a049; }
            QLineEdit { padding: 5px; border: 1px solid #ccc; border-radius: 4px; }
        """)
    
    def browse_save_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "انتخاب مسیر ذخیره batها")
        if folder:
            self.save_path_input.setText(folder)
    
    def generate_frontend_bat(self):
        frontend_path = self.frontend_input.text().strip()
        save_dir = self.save_path_input.text().strip()
        
        if not frontend_path:
            QMessageBox.warning(self, "خطا", "لطفاً آدرس پروژه فرانت رو وارد کن")
            return
        if not save_dir:
            QMessageBox.warning(self, "خطا", "لطفاً مقصد ذخیره فایل bat رو انتخاب کن")
            return
            
        content = f'''cd /d "{frontend_path}"
npm run dev
'''
        save_file = os.path.join(save_dir, "start_frontend.bat")
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(content)
        QMessageBox.information(self, "موفق", f"فایل start_frontend.bat در {save_dir} ساخته شد ✅")
    
    def generate_backend_bat(self):
        backend_path = self.backend_input.text().strip()
        save_dir = self.save_path_input.text().strip()
        
        if not backend_path:
            QMessageBox.warning(self, "خطا", "لطفاً آدرس پروژه بک‌اند رو وارد کن")
            return
        if not save_dir:
            QMessageBox.warning(self, "خطا", "لطفاً مقصد ذخیره فایل bat رو انتخاب کن")
            return
            
        content = f'''@echo off
cd /d "{backend_path}"

"C:\\Program Files\\Java\\jdk-21\\bin\\java.exe" -XX:TieredStopAtLevel=1 -Dspring.output.ansi.enabled=always -Dcom.sun.management.jmxremote -Dspring.jmx.enabled=true -Dspring.liveBeansView.mbeanDomain -Dspring.application.admin.enabled=true "-Dmanagement.endpoints.jmx.exposure.include=*" -Dfile.encoding=UTF-8 -Dsun.stdout.encoding=UTF-8 -Dsun.stderr.encoding=UTF-8 -classpath "target\\classes;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-web\\3.3.5\\spring-boot-starter-web-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-data-jpa\\3.3.5\\spring-boot-starter-data-jpa-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\xerial\\sqlite-jdbc\\3.44.1.0\\sqlite-jdbc-3.44.1.0.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\hibernate\\orm\\hibernate-community-dialects\\6.4.8.Final\\hibernate-community-dialects-6.4.8.Final.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-validation\\3.3.5\\spring-boot-starter-validation-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\projectlombok\\lombok\\1.18.34\\lombok-1.18.34.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\datatype\\jackson-datatype-jsr310\\2.17.2\\jackson-datatype-jsr310-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter\\3.3.5\\spring-boot-starter-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-json\\3.3.5\\spring-boot-starter-json-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-tomcat\\3.3.5\\spring-boot-starter-tomcat-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-web\\6.1.14\\spring-web-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-webmvc\\6.1.14\\spring-webmvc-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-aop\\3.3.5\\spring-boot-starter-aop-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-jdbc\\3.3.5\\spring-boot-starter-jdbc-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\hibernate\\orm\\hibernate-core\\6.5.3.Final\\hibernate-core-6.5.3.Final.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\data\\spring-data-jpa\\3.3.5\\spring-data-jpa-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-aspects\\6.1.14\\spring-aspects-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\apache\\tomcat\\embed\\tomcat-embed-el\\10.1.31\\tomcat-embed-el-10.1.31.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\hibernate\\validator\\hibernate-validator\\8.0.1.Final\\hibernate-validator-8.0.1.Final.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\xml\\bind\\jakarta.xml.bind-api\\4.0.2\\jakarta.xml.bind-api-4.0.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-core\\6.1.14\\spring-core-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\core\\jackson-annotations\\2.17.2\\jackson-annotations-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\core\\jackson-core\\2.17.2\\jackson-core-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\core\\jackson-databind\\2.17.2\\jackson-databind-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot\\3.3.5\\spring-boot-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-autoconfigure\\3.3.5\\spring-boot-autoconfigure-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\boot\\spring-boot-starter-logging\\3.3.5\\spring-boot-starter-logging-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\annotation\\jakarta.annotation-api\\2.1.1\\jakarta.annotation-api-2.1.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\yaml\\snakeyaml\\2.2\\snakeyaml-2.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\datatype\\jackson-datatype-jdk8\\2.17.2\\jackson-datatype-jdk8-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\jackson\\module\\jackson-module-parameter-names\\2.17.2\\jackson-module-parameter-names-2.17.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\apache\\tomcat\\embed\\tomcat-embed-core\\10.1.31\\tomcat-embed-core-10.1.31.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\apache\\tomcat\\embed\\tomcat-embed-websocket\\10.1.31\\tomcat-embed-websocket-10.1.31.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-beans\\6.1.14\\spring-beans-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\io\\micrometer\\micrometer-observation\\1.13.6\\micrometer-observation-1.13.6.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-aop\\6.1.14\\spring-aop-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-context\\6.1.14\\spring-context-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-expression\\6.1.14\\spring-expression-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\aspectj\\aspectjweaver\\1.9.22.1\\aspectjweaver-1.9.22.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\zaxxer\\HikariCP\\5.1.0\\HikariCP-5.1.0.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-jdbc\\6.1.14\\spring-jdbc-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\persistence\\jakarta.persistence-api\\3.1.0\\jakarta.persistence-api-3.1.0.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\transaction\\jakarta.transaction-api\\2.0.1\\jakarta.transaction-api-2.0.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\jboss\\logging\\jboss-logging\\3.5.3.Final\\jboss-logging-3.5.3.Final.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\hibernate\\common\\hibernate-commons-annotations\\6.0.6.Final\\hibernate-commons-annotations-6.0.6.Final.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\io\\smallrye\\jandex\\3.1.2\\jandex-3.1.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\fasterxml\\classmate\\1.7.0\\classmate-1.7.0.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\net\\bytebuddy\\byte-buddy\\1.14.19\\byte-buddy-1.14.19.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\glassfish\\jaxb\\jaxb-runtime\\4.0.5\\jaxb-runtime-4.0.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\inject\\jakarta.inject-api\\2.0.1\\jakarta.inject-api-2.0.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\antlr\\antlr4-runtime\\4.13.0\\antlr4-runtime-4.13.0.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\data\\spring-data-commons\\3.3.5\\spring-data-commons-3.3.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-orm\\6.1.14\\spring-orm-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-tx\\6.1.14\\spring-tx-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\slf4j\\slf4j-api\\2.0.16\\slf4j-api-2.0.16.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\validation\\jakarta.validation-api\\3.0.2\\jakarta.validation-api-3.0.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\jakarta\\activation\\jakarta.activation-api\\2.1.3\\jakarta.activation-api-2.1.3.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\springframework\\spring-jcl\\6.1.14\\spring-jcl-6.1.14.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\ch\\qos\\logback\\logback-classic\\1.5.11\\logback-classic-1.5.11.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\apache\\logging\\log4j\\log4j-to-slf4j\\2.23.1\\log4j-to-slf4j-2.23.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\slf4j\\jul-to-slf4j\\2.0.16\\jul-to-slf4j-2.0.16.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\io\\micrometer\\micrometer-commons\\1.13.6\\micrometer-commons-1.13.6.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\glassfish\\jaxb\\jaxb-core\\4.0.5\\jaxb-core-4.0.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\ch\\qos\\logback\\logback-core\\1.5.11\\logback-core-1.5.11.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\apache\\logging\\log4j\\log4j-api\\2.23.1\\log4j-api-2.23.1.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\eclipse\\angus\\angus-activation\\2.0.2\\angus-activation-2.0.2.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\org\\glassfish\\jaxb\\txw2\\4.0.5\\txw2-4.0.5.jar;C:\\Users\\sadra_maleki\\.m2\\repository\\com\\sun\\istack\\istack-commons-runtime\\4.1.2\\istack-commons-runtime-4.1.2.jar" com.example.project.ProjectApplication
'''
        save_file = os.path.join(save_dir, "start_backend.bat")
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(content)
        QMessageBox.information(self, "موفق", f"فایل start_backend.bat در {save_dir} ساخته شد ✅")
    
    def generate_both(self):
        self.generate_frontend_bat()
        self.generate_backend_bat()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BatGeneratorApp()
    window.show()
    sys.exit(app.exec_())