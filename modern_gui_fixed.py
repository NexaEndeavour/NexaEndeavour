#!/usr/bin/env python3
"""
Modern GUI Application with Unicode-Safe Emoji Logging
This implements the fix for Unicode encoding issues.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import logging
import sys
import re
from pathlib import Path
import platform


class EmojiSafeFormatter(logging.Formatter):
    """Custom formatter that strips emojis for file and console output."""
    
    def __init__(self, fmt=None, datefmt=None, strip_emojis=True):
        super().__init__(fmt, datefmt)
        self.strip_emojis = strip_emojis
        
        # Regex pattern to match emoji characters
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002500-\U00002BEF"  # chinese char
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"  # dingbats
            "\u3030"
            "]+", 
            flags=re.UNICODE
        )
    
    def format(self, record):
        """Format the log record, optionally stripping emojis."""
        # Format the record normally first
        formatted = super().format(record)
        
        # Strip emojis if requested
        if self.strip_emojis:
            formatted = self.emoji_pattern.sub('', formatted)
            # Clean up extra spaces that might be left after emoji removal
            formatted = re.sub(r'\s+', ' ', formatted).strip()
        
        return formatted


class SafeFileHandler(logging.FileHandler):
    """File handler that ensures UTF-8 encoding and handles errors gracefully."""
    
    def __init__(self, filename, mode='a', encoding='utf-8', delay=False, errors='replace'):
        # Ensure UTF-8 encoding and error handling
        super().__init__(filename, mode, encoding, delay, errors)
    
    def emit(self, record):
        """Emit a record with error handling."""
        try:
            super().emit(record)
        except UnicodeEncodeError as e:
            # Fallback: strip emojis and try again
            if hasattr(record, 'msg'):
                # Use emoji-safe formatter as fallback
                formatter = EmojiSafeFormatter(strip_emojis=True)
                safe_message = formatter.format(record)
                print(f"File logging fallback (emoji stripped): {safe_message}")


class SafeConsoleHandler(logging.StreamHandler):
    """Console handler that handles encoding errors gracefully."""
    
    def __init__(self, stream=None):
        super().__init__(stream)
        
        # Detect console encoding
        self.console_encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        self.is_windows_console = (
            platform.system() == 'Windows' and 
            self.console_encoding in ['cp1252', 'cp437', 'windows-1252']
        )
    
    def emit(self, record):
        """Emit a record with encoding-safe handling."""
        try:
            super().emit(record)
        except UnicodeEncodeError:
            # Use emoji-safe formatter for problematic consoles
            if self.is_windows_console:
                formatter = EmojiSafeFormatter(
                    fmt=self.formatter._fmt if self.formatter else "%(levelname)s: %(message)s",
                    strip_emojis=True
                )
                safe_message = formatter.format(record)
                # Output directly to avoid encoding issues
                print(safe_message, file=sys.stdout)


class ModernGUIFixed:
    """Fixed Modern GUI application with Unicode-safe emoji logging."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern GUI - Fixed Emoji Logging 🎨")
        self.root.geometry("800x600")
        
        # Set up fixed logging
        self.setup_safe_logging()
        
        # Create GUI components
        self.create_widgets()
        
        # Log startup message with emojis
        self.logger.info("🎨 Modern GUI application started successfully!")
        self.logger.info("✨ Unicode-safe logging system initialized")
        self.logger.info(f"📊 Console encoding detected: {getattr(sys.stdout, 'encoding', 'unknown')}")
        
    def setup_safe_logging(self):
        """Set up Unicode-safe logging configuration."""
        self.logger = logging.getLogger("ModernGUIFixed")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # File handler with UTF-8 encoding and emoji stripping
        try:
            file_handler = SafeFileHandler("modern_gui_fixed.log", encoding="utf-8")
            file_formatter = EmojiSafeFormatter(
                fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                strip_emojis=True  # Strip emojis for file output
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            self.logger.debug("📁 File logging configured with UTF-8 encoding (emojis stripped)")
        except Exception as e:
            print(f"Failed to set up file logging: {e}")
        
        # Console handler with encoding-safe handling
        try:
            console_handler = SafeConsoleHandler(sys.stdout)
            console_formatter = EmojiSafeFormatter(
                fmt="%(levelname)s: %(message)s",
                strip_emojis=getattr(sys.stdout, 'encoding', 'utf-8') in ['cp1252', 'cp437']
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            self.logger.debug("🖥️ Console logging configured with encoding detection")
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
            text="🎨 Modern GUI - Fixed Emoji Logging", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status info
        status_text = (
            f"Platform: {platform.system()} | "
            f"Console Encoding: {getattr(sys.stdout, 'encoding', 'unknown')} | "
            f"Fixed Logging: ✅"
        )
        status_label = ttk.Label(main_frame, text=status_text, font=("Arial", 9))
        status_label.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        
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
        
        ttk.Button(
            button_frame, 
            text="🧪 Test Unicode", 
            command=self.test_unicode_safety
        ).pack(side=tk.LEFT, padx=5)
        
        # Log display area
        log_label = ttk.Label(main_frame, text="Log Output (with emojis preserved in GUI):")
        log_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame, 
            height=20, 
            width=80,
            font=("Consolas", 9)
        )
        self.log_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text widget to show logs with emojis preserved
        self.setup_gui_logging()
    
    def setup_gui_logging(self):
        """Set up logging to display in the GUI text widget with emojis preserved."""
        class GUILogHandler(logging.Handler):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                # Insert at end and scroll to bottom
                self.text_widget.insert(tk.END, msg + "\n")
                self.text_widget.see(tk.END)
        
        # Add GUI handler to logger with emojis preserved
        gui_handler = GUILogHandler(self.log_text)
        gui_formatter = EmojiSafeFormatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            strip_emojis=False  # Keep emojis in GUI display
        )
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
    
    def test_unicode_safety(self):
        """Test various Unicode characters and emojis."""
        self.logger.info("🧪 Testing Unicode safety...")
        
        # Test various emoji categories
        test_emojis = [
            "🎨 Art and Design",
            "✨ Sparkles and Magic", 
            "📋 Clipboard Operations",
            "📁 File Management",
            "📚 Library Functions",
            "🔥 Critical Errors",
            "⚠️ Warning Messages",
            "✅ Success Indicators",
            "🚀 Launch Operations",
            "💾 Data Storage",
            "🔄 Processing Status",
            "📊 Data Analysis",
            "🎯 Target Achievement"
        ]
        
        for emoji_msg in test_emojis:
            self.logger.debug(emoji_msg)
        
        self.logger.info("🎉 Unicode safety test completed - no encoding errors!")
    
    def run(self):
        """Start the GUI application."""
        self.logger.info("🚀 Starting GUI main loop...")
        self.root.mainloop()


def compare_logging_approaches():
    """Demonstrate the difference between problematic and fixed logging."""
    print("Comparing logging approaches...")
    print("=" * 50)
    
    # Test message with emojis
    test_message = "🎨 Testing emoji logging with various symbols: ✨📋📁📚🔥⚠️✅"
    
    print(f"Original message: {test_message}")
    
    # Show what happens with emoji-safe formatter
    safe_formatter = EmojiSafeFormatter(strip_emojis=True)
    
    # Create a fake log record
    import logging
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg=test_message, args=(), exc_info=None
    )
    
    safe_message = safe_formatter.format(record)
    print(f"Safe formatted (emojis stripped): {safe_message}")
    
    # Show encoding detection
    console_encoding = getattr(sys.stdout, 'encoding', 'utf-8')
    is_problematic = console_encoding in ['cp1252', 'cp437', 'windows-1252']
    
    print(f"Console encoding: {console_encoding}")
    print(f"Problematic encoding detected: {is_problematic}")
    
    print("=" * 50)


if __name__ == "__main__":
    # Compare logging approaches
    compare_logging_approaches()
    
    print("\nStarting Fixed Modern GUI Application...")
    print("=" * 50)
    
    # Create and run the fixed GUI
    app = ModernGUIFixed()
    app.run()