#!/usr/bin/env python3
"""
Demonstration script showing the Unicode emoji logging fix.
This script compares the problematic approach with the fixed implementation.
"""

import logging
import sys
import platform
import tempfile
import os
from pathlib import Path
import traceback

# Import the fixed implementation (headless version)
from emoji_safe_logging import EmojiSafeFormatter, SafeFileHandler, SafeConsoleHandler


def demonstrate_problem():
    """Demonstrate the Unicode encoding problem."""
    print("🔥 DEMONSTRATING THE PROBLEM")
    print("=" * 50)
    
    # Try to set up logging that would fail on Windows with cp1252
    try:
        # Create a logger that might fail with Unicode
        logger = logging.getLogger("problematic")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()
        
        # Add a basic console handler
        console_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        print(f"Console encoding: {getattr(sys.stdout, 'encoding', 'unknown')}")
        print(f"Platform: {platform.system()}")
        
        # Test messages that would cause problems on Windows
        problematic_messages = [
            "🎨 Art palette emoji",
            "✨ Sparkles emoji", 
            "📋 Clipboard emoji",
            "📁 Folder emoji",
            "📚 Books emoji"
        ]
        
        print("\nTrying to log messages with emojis...")
        for msg in problematic_messages:
            try:
                logger.info(msg)
                print(f"✅ Successfully logged: {msg}")
            except UnicodeEncodeError as e:
                print(f"❌ Failed to log: {msg}")
                print(f"   Error: {e}")
                break
                
    except Exception as e:
        print(f"Setup failed: {e}")
        traceback.print_exc()


def demonstrate_solution():
    """Demonstrate the fixed Unicode-safe logging solution."""
    print("\n\n🎯 DEMONSTRATING THE SOLUTION")
    print("=" * 50)
    
    # Set up the fixed logging system
    logger = logging.getLogger("fixed_solution")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    # Create temporary log file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
        temp_path = temp_file.name
    
    try:
        # 1. File handler with emoji stripping
        print("1. Setting up file logging (UTF-8, emojis stripped)...")
        file_handler = SafeFileHandler(temp_path, encoding='utf-8')
        file_formatter = EmojiSafeFormatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s",
            strip_emojis=True
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # 2. Console handler with encoding detection
        print("2. Setting up console logging (encoding-safe)...")
        console_handler = SafeConsoleHandler()
        
        # Determine if we need to strip emojis for console
        console_encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        should_strip = console_encoding in ['cp1252', 'cp437', 'windows-1252']
        
        console_formatter = EmojiSafeFormatter(
            fmt="CONSOLE: %(message)s",
            strip_emojis=should_strip
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        print(f"Console encoding: {console_encoding}")
        print(f"Will strip emojis for console: {should_strip}")
        
        # 3. Test the fixed logging
        print("\n3. Testing fixed logging with emoji messages:")
        test_messages = [
            "🎨 Art and Design operations",
            "✨ Sparkle effects processing", 
            "📋 Clipboard data management",
            "📁 File system operations",
            "📚 Library loading sequence",
            "🔥 Critical error handling",
            "⚠️ Warning notifications",
            "✅ Success confirmations",
            "🚀 Launch procedures"
        ]
        
        for i, msg in enumerate(test_messages, 1):
            try:
                logger.info(f"Test {i}: {msg}")
                print(f"✅ Successfully processed message {i}")
            except Exception as e:
                print(f"❌ Error processing message {i}: {e}")
        
        # Close file handler
        file_handler.close()
        
        # 4. Show file contents
        print("\n4. File log contents (emojis should be stripped):")
        print("-" * 30)
        try:
            with open(temp_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            print(file_content)
        except Exception as e:
            print(f"Error reading file: {e}")
        print("-" * 30)
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def show_formatter_comparison():
    """Show side-by-side comparison of formatters."""
    print("\n\n📊 FORMATTER COMPARISON")
    print("=" * 50)
    
    test_messages = [
        "🎨 Art palette operations",
        "✨ Magic sparkle effects", 
        "📋 Clipboard management",
        "Regular message without emojis",
        "Mixed: Regular text with 🚀 emojis ✨ included"
    ]
    
    # Create formatters
    strip_formatter = EmojiSafeFormatter(
        fmt="%(message)s", 
        strip_emojis=True
    )
    
    preserve_formatter = EmojiSafeFormatter(
        fmt="%(message)s", 
        strip_emojis=False
    )
    
    print("| Original Message | Emojis Stripped | Emojis Preserved |")
    print("|" + "-" * 18 + "|" + "-" * 17 + "|" + "-" * 18 + "|")
    
    for msg in test_messages:
        # Create log record
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="", lineno=0,
            msg=msg, args=(), exc_info=None
        )
        
        stripped = strip_formatter.format(record)
        preserved = preserve_formatter.format(record)
        
        # Truncate for display
        orig_display = msg[:16] + "..." if len(msg) > 16 else msg
        strip_display = stripped[:15] + "..." if len(stripped) > 15 else stripped
        preserve_display = preserved[:16] + "..." if len(preserved) > 16 else preserved
        
        print(f"| {orig_display:<16} | {strip_display:<15} | {preserve_display:<16} |")


def demonstrate_platform_compatibility():
    """Demonstrate platform compatibility features."""
    print("\n\n🖥️ PLATFORM COMPATIBILITY")
    print("=" * 50)
    
    print(f"Platform: {platform.system()}")
    print(f"Platform Version: {platform.version()}")
    print(f"Python Version: {sys.version}")
    print(f"Console Encoding: {getattr(sys.stdout, 'encoding', 'unknown')}")
    print(f"File System Encoding: {sys.getfilesystemencoding()}")
    print(f"Default Locale Encoding: {sys.getdefaultencoding()}")
    
    # Test encoding detection logic
    console_encoding = getattr(sys.stdout, 'encoding', 'utf-8')
    is_windows = platform.system() == 'Windows'
    is_problematic_encoding = console_encoding in ['cp1252', 'cp437', 'windows-1252']
    
    print(f"\nEncoding Analysis:")
    print(f"- Is Windows: {is_windows}")
    print(f"- Problematic encoding: {is_problematic_encoding}")
    print(f"- Should strip emojis for console: {is_windows and is_problematic_encoding}")
    
    # Show which characters would be problematic
    print(f"\nEmoji Support Test:")
    test_emojis = ["🎨", "✨", "📋", "📁", "📚"]
    
    for emoji in test_emojis:
        try:
            # Try to encode with console encoding
            emoji.encode(console_encoding)
            print(f"✅ {emoji} - Supported")
        except UnicodeEncodeError:
            print(f"❌ {emoji} - Would cause encoding error")


def main():
    """Main demonstration function."""
    print("UNICODE EMOJI LOGGING FIX DEMONSTRATION")
    print("=" * 60)
    print(f"Running on {platform.system()} with Python {sys.version_info.major}.{sys.version_info.minor}")
    print("=" * 60)
    
    # Run all demonstrations
    try:
        demonstrate_problem()
        demonstrate_solution()
        show_formatter_comparison()
        demonstrate_platform_compatibility()
        
        print("\n\n🎉 DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Key Benefits of the Fixed Implementation:")
        print("✅ Handles Unicode emoji encoding errors gracefully")
        print("✅ Separates GUI logging (with emojis) from file/console logging")
        print("✅ Uses UTF-8 encoding for file output")
        print("✅ Automatically detects problematic console encodings")
        print("✅ Maintains backward compatibility")
        print("✅ Preserves emoji functionality in GUI while ensuring robust logging")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()