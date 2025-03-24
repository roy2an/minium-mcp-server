from . import server
import asyncio
import argparse

def main():
    """Main entry point for the package."""
    parser = argparse.ArgumentParser(description='Minium MCP Server')
    parser.add_argument('--path', 
                       default="./MiniProgram",
                       help='Path to WeChat MiniProgram project')
    
    args = parser.parse_args()
    asyncio.run(server.main(args.path))


# Optionally expose other important items at package level
__all__ = ["main", "server"]