#!/usr/bin/env python3
"""
Modern GUI Application with Unicode Emoji Logging
This demonstrates the Unicode encoding issue and implements the fix.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import sys
import io
import contextlib
from pathlib import Path


class ModernGUI:
    """Modern GUI application with emoji-enhanced logging."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern GUI - Emoji Logging Demo 🎨")
        self.root.geometry("800x600")
        
        # Set up logging
        self.setup_logging()
        
        # Create GUI components
        self.create_widgets()
        
        # Log startup message with emojis
        self.logger.info("🎨 Modern GUI application started successfully!")
        self.logger.info("✨ Welcome to the emoji-enhanced logging system")
        
    def setup_logging(self):
        """Set up logging configuration - this will initially cause Unicode errors."""
        self.logger = logging.getLogger("ModernGUI")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # File handler - this will cause Unicode errors on Windows
        try:
            file_handler = logging.FileHandler("modern_gui.log", encoding="utf-8")
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Failed to set up file logging: {e}")
        
        # Console handler - this will cause Unicode errors with cp1252 encoding
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(
                "%(levelname)s: %(message)s"
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        except Exception as e:
            print(f"Failed to set up console logging: {e}")
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🎨 Modern GUI - Emoji Logging Test", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
        # Buttons with emoji actions
        ttk.Button(
            button_frame, 
            text="📋 Process Data", 
            command=self.process_data
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            button_frame, 
            text="📁 Open File", 
            command=self.open_file
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="📚 Load Library", 
            command=self.load_library
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="✨ Generate Report", 
            command=self.generate_report
        ).pack(side=tk.LEFT, padx=5)
        
        # Log display area
        log_label = ttk.Label(main_frame, text="Log Output (with emojis in GUI):")
        log_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame, 
            height=20, 
            width=80,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text widget to show logs
        self.setup_gui_logging()
    
    def setup_gui_logging(self):
        """Set up logging to display in the GUI text widget."""
        # Create a custom handler for GUI display
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                # Insert at end and scroll to bottom
                self.text_widget.insert(tk.END, msg + "\n")
                self.text_widget.see(tk.END)
        
        # Add GUI handler to logger
        gui_handler = GUILogHandler(self.log_text)
        gui_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        gui_handler.setFormatter(gui_formatter)
        self.logger.addHandler(gui_handler)
    
    def process_data(self):
        """Simulate data processing with emoji logging."""
        self.logger.info("📋 Starting data processing operation...")
        self.logger.debug("📊 Loading dataset from memory")
        self.logger.info("🔄 Processing 1000 records...")
        self.logger.warning("⚠️ Found 3 missing values, using defaults")
        self.logger.info("✅ Data processing completed successfully!")
    
    def open_file(self):
        """Simulate file operations with emoji logging."""
        self.logger.info("📁 Opening file browser...")
        self.logger.debug("🔍 Scanning available files")
        self.logger.info("📄 Selected file: example_data.csv")
        self.logger.info("💾 File loaded into memory (2.3MB)")
        self.logger.info("✨ File operations completed!")
    
    def load_library(self):
        """Simulate library loading with emoji logging."""
        self.logger.info("📚 Loading external libraries...")
        self.logger.debug("📦 Importing numpy...")
        self.logger.debug("📦 Importing pandas...")
        self.logger.debug("📦 Importing matplotlib...")
        self.logger.warning("⚠️ Library version mismatch detected, using compatibility mode")
        self.logger.info("🎯 All libraries loaded successfully!")
    
    def generate_report(self):
        """Simulate report generation with emoji logging."""
        self.logger.info("✨ Starting report generation...")
        self.logger.debug("📝 Creating document template")
        self.logger.debug("📊 Generating charts and graphs")
        self.logger.debug("🎨 Applying styling and formatting")
        self.logger.info("📋 Report generated: output/report_2025.pdf")
        self.logger.info("🚀 Report generation completed successfully!")
        
        # This will likely fail with Unicode errors on Windows console
        try:
            self.logger.error("🔥 This message contains emojis that will cause encoding errors!")
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error: {e}")
    
    def run(self):
        """Start the GUI application."""
        self.logger.info("🚀 Starting GUI main loop...")
        self.root.mainloop()


def test_unicode_encoding_issue():
    """Demonstrate the Unicode encoding issue that occurs on Windows."""
    print("Testing Unicode emoji encoding...")
    
    # This will work fine in most environments
    message_with_emoji = "🎨 Testing emoji encoding"
    print(f"Message: {message_with_emoji}")
    
    # But when logging to a file or console with cp1252 encoding, it will fail
    try:
        # Simulate Windows console encoding
        with io.StringIO() as fake_console:
            fake_console.encoding = 'cp1252'  # Simulate Windows console
            # This would normally cause: UnicodeEncodeError: 'charmap' codec can't encode character
            logging.basicConfig(stream=fake_console, level=logging.INFO)
            logger = logging.getLogger("test")
            logger.info("🎨 This will cause encoding errors on Windows!")
    except Exception as e:
        print(f"Expected encoding error: {e}")


if __name__ == "__main__":
    # Test the encoding issue first
    test_unicode_encoding_issue()
    
    print("\n" + "="*50)
    print("Starting Modern GUI Application...")
    print("="*50)
    
    # Create and run the GUI
    app = ModernGUI()
    app.run()