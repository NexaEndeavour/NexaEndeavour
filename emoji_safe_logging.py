#!/usr/bin/env python3
"""
Core Unicode-Safe Emoji Logging Implementation (Headless)
This contains the core logging functionality without GUI dependencies.
"""

import logging
import sys
import re
import platform
from pathlib import Path


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


class EmojiSafeLogger:
    """A logger class that handles emoji encoding safely."""
    
    def __init__(self, name="EmojiSafeLogger", log_file=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()
        
        # Set up file logging if requested
        if log_file:
            self.setup_file_logging(log_file)
        
        # Set up console logging
        self.setup_console_logging()
        
    def setup_file_logging(self, log_file):
        """Set up file logging with UTF-8 encoding and emoji stripping."""
        file_handler = SafeFileHandler(log_file, encoding="utf-8")
        file_formatter = EmojiSafeFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            strip_emojis=True  # Strip emojis for file output
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
    def setup_console_logging(self):
        """Set up console logging with encoding detection."""
        console_handler = SafeConsoleHandler(sys.stdout)
        
        # Detect if we need to strip emojis for console
        console_encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        should_strip_emojis = console_encoding in ['cp1252', 'cp437', 'windows-1252']
        
        console_formatter = EmojiSafeFormatter(
            fmt="%(levelname)s: %(message)s",
            strip_emojis=should_strip_emojis
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
    def info(self, message):
        """Log an info message."""
        self.logger.info(message)
        
    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)
        
    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)
        
    def error(self, message):
        """Log an error message."""
        self.logger.error(message)
        
    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)


def demonstrate_emoji_safe_logging():
    """Demonstrate the emoji-safe logging functionality."""
    print("🧪 Testing Emoji-Safe Logging System")
    print("=" * 50)
    
    # Create logger with file output
    logger = EmojiSafeLogger("demo", "emoji_safe_demo.log")
    
    # Test messages with various emojis
    test_messages = [
        ("info", "🎨 Art and Design operations starting"),
        ("debug", "✨ Sparkle effects processing initialized"),
        ("info", "📋 Clipboard data management active"),
        ("warning", "⚠️ Warning: File size exceeds recommended limit"),
        ("error", "🔥 Critical error in data processing pipeline"),
        ("info", "📁 File system operations completed"),
        ("debug", "📚 Library loading sequence finished"),
        ("info", "✅ All operations completed successfully"),
        ("info", "🚀 System ready for production deployment")
    ]
    
    print(f"Console encoding: {getattr(sys.stdout, 'encoding', 'unknown')}")
    print(f"Platform: {platform.system()}")
    print(f"Will strip emojis for console: {getattr(sys.stdout, 'encoding', 'utf-8') in ['cp1252', 'cp437', 'windows-1252']}")
    print("\nLogging test messages:")
    
    for level, message in test_messages:
        try:
            getattr(logger, level)(message)
            print(f"✅ {level.upper()}: Logged successfully")
        except Exception as e:
            print(f"❌ {level.upper()}: Failed - {e}")
    
    # Show file contents
    print("\nFile log contents (emojis should be stripped):")
    print("-" * 40)
    try:
        with open("emoji_safe_demo.log", 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
    except Exception as e:
        print(f"Error reading log file: {e}")
    print("-" * 40)
    
    return logger


if __name__ == "__main__":
    demonstrate_emoji_safe_logging()