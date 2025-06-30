import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QFormLayout, QLineEdit, QTextEdit, 
                            QPushButton, QMenuBar, QAction, QStackedWidget,
                            QScrollArea, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class FormWidget(QWidget):
    def __init__(self, fields, parent=None):
        super().__init__(parent)
        self.fields = fields
        self.field_widgets = {}
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll_widget = QWidget()
        form_layout = QFormLayout()
        
        for field in self.fields:
            if field in ['Beschreibung', 'Features', 'Installation', 'Verwendung', 
                        'Tests', 'Build', 'Deployment', 'Projektstruktur',
                        'Export / Import / API-Info', 'Sicherheit / Datenschutz',
                        'Abhängigkeiten / Datenschutz', 'Changelog']:
                widget = QTextEdit()
                widget.setMaximumHeight(100)
            else:
                widget = QLineEdit()
            
            default_value = ""
            if field == 'Autor' or field == 'Autor / Kontakt':
                default_value = "**Kai ([@chefkoch0312](https://github.com/chefkoch0312))**\n[https://kado-ber.de](https://kado-ber.de)" # hier bitte anpassen
            elif field == 'Lizenz':
                default_value = "MIT License" # hier bitte anpassen
            elif field == 'Screenshots':
                default_value = "![Screenshot](./images/screenshot.png)" # hier bitte anpassen
            
            if default_value:
                if isinstance(widget, QTextEdit):
                    widget.setPlainText(default_value)
                else:
                    widget.setText(default_value)
            
            self.field_widgets[field] = widget
            
            label = QLabel(field + ":")
            font = QFont()
            font.setBold(True)
            label.setFont(font)
            
            form_layout.addRow(label, widget)
        
        scroll_widget.setLayout(form_layout)
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        self.setLayout(layout)
    
    def get_form_data(self):
        """Sammelt alle Formulardaten"""
        data = {}
        for field, widget in self.field_widgets.items():
            if isinstance(widget, QTextEdit):
                data[field] = widget.toPlainText()
            else:
                data[field] = widget.text()
        return data
    
    def clear_form(self):
        """Leert alle Formularelder"""
        for widget in self.field_widgets.values():
            if isinstance(widget, QTextEdit):
                widget.clear()
            else:
                widget.clear()


class READMEGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("README.md-Generator")
        self.setGeometry(100, 100, 1000, 700)
        
        self.minimal_fields = [
            'Projektname', 'Beschreibung', 'Features', 'Screenshots',
            'Installation', 'Verwendung', 'Lizenz', 'Autor'
        ]
        
        self.full_fields = [
            'Projektname', 'Beschreibung', 'Features', 'Screenshots',
            'Tech Stack', 'Projektstruktur', 'Installation', 'Verwendung',
            'Tests', 'Build', 'Deployment', 'Export / Import / API-Info',
            'Sicherheit / Datenschutz', 'Abhängigkeiten / Datenschutz',
            'Lizenz', 'Autor / Kontakt', 'Projektstatus', 'Changelog',
            'Weiterführende Links'
        ]
        
        self.setup_ui()
        self.setup_menu()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        
        left_layout = QVBoxLayout()
        
        self.form_stack = QStackedWidget()
        
        self.minimal_form = FormWidget(self.minimal_fields)
        self.form_stack.addWidget(self.minimal_form)
        
        self.full_form = FormWidget(self.full_fields)
        self.form_stack.addWidget(self.full_form)
        
        left_layout.addWidget(self.form_stack)
        
        button_layout = QHBoxLayout()
        
        self.generate_btn = QPushButton("Dokumentation generieren")
        self.generate_btn.clicked.connect(self.generate_documentation)
        
        self.clear_btn = QPushButton("Formular leeren")
        self.clear_btn.clicked.connect(self.clear_current_form)
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        left_layout.addLayout(button_layout)
        
        right_layout = QVBoxLayout()
        
        output_label = QLabel("Generierte Dokumentation:")
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        output_label.setFont(font)
        
        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Courier", 10))
        
        self.copy_btn = QPushButton("Text kopieren")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        
        right_layout.addWidget(output_label)
        right_layout.addWidget(self.output_text)
        right_layout.addWidget(self.copy_btn)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(500)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        
        central_widget.setLayout(main_layout)
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        form_menu = menubar.addMenu("Formular")
        
        minimal_action = QAction("Minimal", self)
        minimal_action.triggered.connect(lambda: self.switch_form(0))
        form_menu.addAction(minimal_action)
        
        full_action = QAction("Vollständig", self)
        full_action.triggered.connect(lambda: self.switch_form(1))
        form_menu.addAction(full_action)
        
        help_menu = menubar.addMenu("Hilfe")
        about_action = QAction("Über", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def switch_form(self, index):
        """Wechselt zwischen Minimal- und Full-Formular"""
        self.form_stack.setCurrentIndex(index)
        if index == 0:
            self.setWindowTitle("Documentation Generator - Minimal")
        else:
            self.setWindowTitle("Documentation Generator - Vollständig")
    
    def generate_documentation(self):
        """Generiert die Markdown-Dokumentation"""
        current_form = self.form_stack.currentWidget()
        data = current_form.get_form_data()
        
        markdown_text = ""
        
        for field, value in data.items():
            if not value.strip():  
                continue
                
            if field == 'Projektname':
                markdown_text += f"# **📦 {value}**\n\n"
            elif field == 'Beschreibung':
                markdown_text += f"{value}\n\n"
                markdown_text += "![Version](https://img.shields.io/badge/version-1.0.0-blue)\n"
                markdown_text += "![Sprache](https://img.shields.io/badge/Python-3.10%2B-blue)\n"
                markdown_text += "![License](https://img.shields.io/badge/license-MIT-green)\n"
                markdown_text += "![Plattform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)\n\n"
            elif field == 'Features':
                markdown_text += f"## **🚀 {field}**\n\n{value}\n\n"
            elif field == 'Screenshots':
                markdown_text += f"## **🖼️ {field}**\n\n{value}\n\n"
            elif field == 'Tech Stack':
                markdown_text += f"## **🛠️ {field}**\n\n{value}\n\n"
            elif field == 'Projektstruktur':
                markdown_text += f"## **📁 {field}**\n\n{value}\n\n"
            elif field == 'Installation':
                markdown_text += f"## **⚙️ {field}**\n\n{value}\n\n"
            elif field == 'Verwendung':
                markdown_text += f"## **▶️ {field}**\n\n{value}\n\n"
            elif field == 'Tests':
                markdown_text += f"## **🧪 {field}**\n\n{value}\n\n"
            elif field == 'Build':
                markdown_text += f"## **🧱 {field}**\n\n{value}\n\n"
            elif field == 'Deployment':
                markdown_text += f"## **🌐 {field}**\n\n{value}\n\n"
            elif field == 'Export / Import / API-Info':
                markdown_text += f"## **💾 {field}**\n\n{value}\n\n"
            elif field == 'Sicherheit / Datenschutz':
                markdown_text += f"## **🔒 {field}**\n\n{value}\n\n"
            elif field == 'Abhängigkeiten / Datenschutz':
                markdown_text += f"## **📦 {field}**\n\n{value}\n\n"
            elif field == 'Projektstatus':
                markdown_text += f"## **🗃️ {field}**\n\n{value}\n\n"
            elif field == 'Changelog':
                markdown_text += f"## **📋 {field}**\n\n{value}\n\n"
            elif field == 'Weiterführende Links':
                markdown_text += f"## **📚 {field}**\n\n{value}\n\n"
            elif field == 'Lizenz':
                markdown_text += f"## **🧾 {field}**\n\n{value}\n\n"
            elif field == 'Autor' or field == 'Autor / Kontakt':
                markdown_text += f"## **👤 {field}**\n\n{value}\n\n"
            else:
                markdown_text += f"## {field}\n\n{value}\n\n"
        
        self.output_text.setPlainText(markdown_text)
    
    def clear_current_form(self):
        """Leert das aktuelle Formular"""
        current_form = self.form_stack.currentWidget()
        current_form.clear_form()
        self.output_text.clear()
    
    def copy_to_clipboard(self):
        """Kopiert den generierten Text in die Zwischenablage"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
    
    def show_about(self):
        """Zeigt Über-Dialog"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "Über README.md-Generator",
                         "README.md-Generator v1.0\n\n"
                         "Erstellt Markdown-Dokumentation aus Formulardaten.\n"
                         "Wählen Sie zwischen Minimal- und Vollständigem Formular.")


def main():
    app = QApplication(sys.argv)
    
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f0f0f0;
        }
        QWidget {
            font-family: Arial, sans-serif;
        }
        QPushButton {
            background-color: #007acc;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005a9e;
        }
        QPushButton:pressed {
            background-color: #004578;
        }
        QLineEdit, QTextEdit {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px;
            background-color: white;
        }
        QLineEdit:focus, QTextEdit:focus {
            border: 2px solid #007acc;
        }
        QLabel {
            color: #333;
        }
        QMenuBar {
            background-color: #e0e0e0;
            border-bottom: 1px solid #ccc;
        }
        QMenuBar::item {
            padding: 4px 8px;
        }
        QMenuBar::item:selected {
            background-color: #007acc;
            color: white;
        }
    """)
    
    window = READMEGenerator()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()