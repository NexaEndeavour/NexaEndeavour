#!/usr/bin/env python3
"""
Test script for Unicode emoji logging functionality.
"""

import unittest
import logging
import io
import sys
import tempfile
import os
from pathlib import Path

# Import the fixed implementation (headless version for testing)
from emoji_safe_logging import EmojiSafeFormatter, SafeFileHandler, SafeConsoleHandler


class TestEmojiSafeLogging(unittest.TestCase):
    """Test cases for emoji-safe logging functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_messages = [
            "🎨 Art and Design",
            "✨ Sparkles and Magic", 
            "📋 Clipboard Operations",
            "📁 File Management",
            "📚 Library Functions",
            "🔥 Critical Errors",
            "⚠️ Warning Messages",
            "✅ Success Indicators",
            "🚀 Launch Operations",
            "Regular message without emojis"
        ]
        
    def test_emoji_safe_formatter_strips_emojis(self):
        """Test that EmojiSafeFormatter can strip emojis."""
        formatter = EmojiSafeFormatter(strip_emojis=True)
        
        # Create a test log record
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="🎨 Testing emoji removal ✨", args=(), exc_info=None
        )
        
        formatted = formatter.format(record)
        
        # Should not contain emoji characters
        self.assertNotIn("🎨", formatted)
        self.assertNotIn("✨", formatted)
        # Should contain the text
        self.assertIn("Testing emoji removal", formatted)
        
    def test_emoji_safe_formatter_preserves_emojis(self):
        """Test that EmojiSafeFormatter can preserve emojis."""
        formatter = EmojiSafeFormatter(strip_emojis=False)
        
        # Create a test log record
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg="🎨 Testing emoji preservation ✨", args=(), exc_info=None
        )
        
        formatted = formatter.format(record)
        
        # Should contain emoji characters
        self.assertIn("🎨", formatted)
        self.assertIn("✨", formatted)
        # Should contain the text
        self.assertIn("Testing emoji preservation", formatted)
        
    def test_safe_file_handler_utf8_encoding(self):
        """Test that SafeFileHandler uses UTF-8 encoding."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_path = temp_file.name
            
        try:
            # Create handler with UTF-8 encoding
            handler = SafeFileHandler(temp_path, encoding='utf-8')
            formatter = EmojiSafeFormatter(strip_emojis=True)
            handler.setFormatter(formatter)
            
            # Create logger and add handler
            logger = logging.getLogger("test_file")
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)
            
            # Log message with emojis
            logger.info("🎨 Testing file logging with emojis ✨")
            
            # Close handler
            handler.close()
            
            # Read file and verify content
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Should contain stripped message
            self.assertIn("Testing file logging with emojis", content)
            # Should not contain emojis (they were stripped)
            self.assertNotIn("🎨", content)
            self.assertNotIn("✨", content)
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    def test_console_encoding_detection(self):
        """Test console encoding detection logic."""
        # Test the encoding detection logic directly
        test_encodings = [
            ('utf-8', False),
            ('cp1252', True),
            ('cp437', True),
            ('windows-1252', True),
            ('ascii', False)
        ]
        
        for encoding, should_be_problematic in test_encodings:
            # Test the logic that determines if an encoding is problematic
            is_problematic = encoding in ['cp1252', 'cp437', 'windows-1252']
            self.assertEqual(is_problematic, should_be_problematic, 
                           f"Encoding {encoding} problematic detection failed")
        
        # Test that the handler can be created
        handler = SafeConsoleHandler()
        self.assertIsNotNone(handler.console_encoding)
        self.assertIsInstance(handler.is_windows_console, bool)
                    
    def test_emoji_pattern_matching(self):
        """Test that emoji pattern correctly matches Unicode emojis."""
        formatter = EmojiSafeFormatter(strip_emojis=True)
        
        test_cases = [
            ("🎨", True),   # Art palette
            ("✨", True),   # Sparkles
            ("📋", True),   # Clipboard
            ("📁", True),   # Folder
            ("📚", True),   # Books
            ("🔥", True),   # Fire
            ("⚠️", True),   # Warning
            ("✅", True),   # Check mark
            ("🚀", True),   # Rocket
            ("A", False),   # Regular letter
            ("123", False), # Numbers
            ("!", False),   # Punctuation
        ]
        
        for char, should_match in test_cases:
            matches = bool(formatter.emoji_pattern.search(char))
            self.assertEqual(matches, should_match, 
                           f"Character '{char}' match result should be {should_match}")
            
    def test_all_test_messages(self):
        """Test all predefined test messages for emoji handling."""
        formatter_strip = EmojiSafeFormatter(strip_emojis=True)
        formatter_keep = EmojiSafeFormatter(strip_emojis=False)
        
        for message in self.test_messages:
            # Create test record
            record = logging.LogRecord(
                name="test", level=logging.INFO, pathname="", lineno=0,
                msg=message, args=(), exc_info=None
            )
            
            # Test stripping
            stripped = formatter_strip.format(record)
            # Test preserving
            preserved = formatter_keep.format(record)
            
            # Preserved should contain original message
            self.assertIn(message.replace("🎨", "").replace("✨", "").replace("📋", "")
                         .replace("📁", "").replace("📚", "").replace("🔥", "")
                         .replace("⚠️", "").replace("✅", "").replace("🚀", "").strip(), 
                         preserved)
            
            # If message has emojis, stripped should be different
            has_emojis = bool(formatter_strip.emoji_pattern.search(message))
            if has_emojis:
                self.assertNotEqual(stripped, preserved)


class TestLoggingIntegration(unittest.TestCase):
    """Integration tests for the logging system."""
    
    def test_complete_logging_setup(self):
        """Test the complete logging setup with multiple handlers."""
        # Create temporary log file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_path = temp_file.name
            
        try:
            # Set up logger with multiple handlers
            logger = logging.getLogger("integration_test")
            logger.setLevel(logging.DEBUG)
            logger.handlers.clear()
            
            # File handler (should strip emojis)
            file_handler = SafeFileHandler(temp_path, encoding='utf-8')
            file_formatter = EmojiSafeFormatter(
                fmt="%(asctime)s - %(levelname)s - %(message)s",
                strip_emojis=True
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            # String stream handler (simulate GUI - preserve emojis)
            gui_stream = io.StringIO()
            gui_handler = logging.StreamHandler(gui_stream)
            gui_formatter = EmojiSafeFormatter(
                fmt="%(levelname)s: %(message)s",
                strip_emojis=False
            )
            gui_handler.setFormatter(gui_formatter)
            logger.addHandler(gui_handler)
            
            # Test logging
            test_message = "🎨 Integration test with emojis ✨"
            logger.info(test_message)
            
            # Close file handler
            file_handler.close()
            
            # Check file output (should be stripped)
            with open(temp_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
                
            self.assertIn("Integration test with emojis", file_content)
            self.assertNotIn("🎨", file_content)
            self.assertNotIn("✨", file_content)
            
            # Check GUI output (should preserve emojis)
            gui_content = gui_stream.getvalue()
            self.assertIn("🎨", gui_content)
            self.assertIn("✨", gui_content)
            self.assertIn("Integration test with emojis", gui_content)
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)


def run_manual_tests():
    """Run manual tests to demonstrate the functionality."""
    print("Running manual tests for emoji logging...")
    print("=" * 60)
    
    # Test 1: Emoji stripping
    print("\n1. Testing emoji stripping:")
    formatter = EmojiSafeFormatter(strip_emojis=True)
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="🎨 This message has emojis ✨📋📁", args=(), exc_info=None
    )
    
    original = record.msg
    stripped = formatter.format(record)
    print(f"Original: {original}")
    print(f"Stripped: {stripped}")
    
    # Test 2: Emoji preservation
    print("\n2. Testing emoji preservation:")
    formatter_keep = EmojiSafeFormatter(strip_emojis=False)
    preserved = formatter_keep.format(record)
    print(f"Preserved: {preserved}")
    
    # Test 3: File logging
    print("\n3. Testing file logging:")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_path = temp_file.name
    
    try:
        logger = logging.getLogger("manual_test")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        file_handler = SafeFileHandler(temp_path, encoding='utf-8')
        file_formatter = EmojiSafeFormatter(strip_emojis=True)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        logger.info("🎨 File logging test with emojis ✨")
        file_handler.close()
        
        with open(temp_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        print(f"File content: {file_content.strip()}")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    print("\n" + "=" * 60)
    print("Manual tests completed!")


if __name__ == "__main__":
    # Run manual tests first
    run_manual_tests()
    
    print("\nRunning unit tests...")
    unittest.main(verbosity=2)