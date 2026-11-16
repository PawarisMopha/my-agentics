"""
Test Python Agentic components and environment utilities.
"""
import sys

def main():
    print("=== [2] Testing Python Agentic Stack ===")
    print(f"Python Runtime: {sys.version.split()[0]}")

    # 1. Test python-dotenv
    import dotenv
    dotenv.load_dotenv()
    print("✓ python-dotenv loaded successfully")

    # 2. Test httpx
    import httpx
    print(f"✓ httpx ready (version {httpx.__version__})")

    # 3. Test rich
    import rich
    from rich.console import Console
    console = Console()
    console.print("[green]✓ rich terminal output ready[/green]")

    print("\nPython core agentic components PASSED! ✨")

if __name__ == "__main__":
    main()
