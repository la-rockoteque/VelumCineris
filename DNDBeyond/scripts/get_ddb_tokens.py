#!/usr/bin/env python3
"""
D&D Beyond Token Extractor

Automates the process of extracting cookies and security tokens from D&D Beyond
using Playwright to avoid manual browser DevTools extraction.

Usage:
    poetry run python DNDBeyond/scripts/get_ddb_tokens.py

Requirements:
    - Playwright installed: poetry run playwright install
    - DDB credentials in environment or prompted at runtime
"""

import os
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup


class DDBTokenExtractor:
    """Extracts authentication tokens from D&D Beyond"""

    BASE_URL = "https://www.dndbeyond.com"
    LOGIN_URL = f"{BASE_URL}/sign-in"
    CREATE_SPELL_URL = f"{BASE_URL}/homebrew/creations/create-spell/create"

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.cookies = None
        self.security_token = None
        self.authenticity_token = None
        self.verification_token = None
        self.user_id = None
        self.username = None

    def extract_tokens(self, email: str = None, password: str = None) -> dict:
        """
        Extract all necessary tokens from D&D Beyond

        Args:
            email: D&D Beyond account email (or set DDB_EMAIL env var)
            password: D&D Beyond account password (or set DDB_PASSWORD env var)

        Returns:
            Dict with cookies and tokens
        """
        # Get credentials
        email = email or os.getenv("DDB_EMAIL")
        password = password or os.getenv("DDB_PASSWORD")

        if not email or not password:
            print("❌ Error: Email and password required")
            print("\nOptions:")
            print("  1. Set DDB_EMAIL and DDB_PASSWORD environment variables")
            print("  2. Pass email/password as arguments")
            print("\nFor security, consider using environment variables:")
            print("  export DDB_EMAIL='your-email@example.com'")
            print("  export DDB_PASSWORD='your-password'")
            sys.exit(1)

        print("🌐 Starting browser automation...")
        print(f"   Headless mode: {'ON' if self.headless else 'OFF (you can watch the browser)'}")

        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            page = context.new_page()

            try:
                # Step 1: Login
                print("\n1️⃣  Logging in to D&D Beyond...")
                self._login(page, email, password)

                # Step 2: Extract cookies
                print("\n2️⃣  Extracting cookies...")
                self._extract_cookies(context)

                # Step 3: Extract user info
                print("\n3️⃣  Extracting user information...")
                self._extract_user_info(page)

                # Step 4: Navigate to create spell page
                print("\n4️⃣  Navigating to spell creation page...")
                self._navigate_to_create_page(page)

                # Step 5: Extract security tokens
                print("\n5️⃣  Extracting security tokens...")
                self._extract_security_tokens(page)

                print("\n✅ Successfully extracted all tokens!")

                return self._build_result()

            except Exception as e:
                print(f"\n❌ Error during token extraction: {e}")
                if not self.headless:
                    input("\nPress Enter to close browser...")
                raise
            finally:
                browser.close()

    def _login(self, page, email: str, password: str):
        """Login to D&D Beyond"""
        try:
            page.goto(self.LOGIN_URL, wait_until="networkidle", timeout=30000)

            # Fill login form
            page.fill('input[type="email"]', email)
            page.fill('input[type="password"]', password)

            # Click login button
            page.click('button[type="submit"]')

            # Wait for redirect after login
            page.wait_for_url("**/characters", timeout=30000)
            print("   ✓ Login successful")

        except PlaywrightTimeout:
            print("   ⚠️  Login timeout - checking if already logged in...")
            # Check if we're already on a logged-in page
            if "/characters" in page.url or "/profile" in page.url:
                print("   ✓ Already logged in")
            else:
                raise Exception("Login failed - credentials may be incorrect")

    def _extract_cookies(self, context):
        """Extract cookies from browser context"""
        cookies = context.cookies()

        # Format cookies as string for requests
        cookie_strings = [f"{c['name']}={c['value']}" for c in cookies]
        self.cookies = "; ".join(cookie_strings)

        print(f"   ✓ Extracted {len(cookies)} cookies")

    def _extract_user_info(self, page):
        """Extract user ID and username"""
        try:
            # Look for user info in the page
            page.goto(f"{self.BASE_URL}/my-account", wait_until="networkidle", timeout=15000)

            # Try to extract from page content
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')

            # Find user ID and username
            # These are often in meta tags or data attributes
            user_link = soup.find('a', href=re.compile(r'/profile/[\w-]+/\d+'))
            if user_link:
                match = re.search(r'/profile/([\w-]+)/(\d+)', user_link['href'])
                if match:
                    self.username = match.group(1)
                    self.user_id = match.group(2)

            # Alternative: check for data in page
            if not self.user_id:
                # Try to find user ID in page data
                script_tags = soup.find_all('script', string=re.compile(r'userId'))
                for script in script_tags:
                    match = re.search(r'"userId["\']?\s*:\s*["\']?(\d+)', script.string)
                    if match:
                        self.user_id = match.group(1)
                        break

            if self.user_id:
                print(f"   ✓ Found user ID: {self.user_id}")
            if self.username:
                print(f"   ✓ Found username: {self.username}")
            else:
                print("   ⚠️  Could not extract username (not critical)")

        except Exception as e:
            print(f"   ⚠️  Could not extract user info: {e} (not critical)")

    def _navigate_to_create_page(self, page):
        """Navigate to the spell creation page"""
        page.goto(self.CREATE_SPELL_URL, wait_until="networkidle", timeout=30000)
        print("   ✓ Reached spell creation page")

    def _extract_security_tokens(self, page):
        """Extract security tokens from the create spell page"""
        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Find security token
        security_input = soup.find('input', {'name': 'security-token'})
        if security_input:
            self.security_token = security_input.get('value')
            print(f"   ✓ Security token: {self.security_token[:16]}...")
        else:
            print("   ⚠️  Security token not found")

        # Find authenticity token
        auth_input = soup.find('input', {'name': 'authenticity-token'})
        if auth_input:
            self.authenticity_token = auth_input.get('value')
            print(f"   ✓ Authenticity token: {self.authenticity_token[:16]}...")
        else:
            print("   ⚠️  Authenticity token not found")

        # Find request verification token
        verify_input = soup.find('input', {'name': 'request-verification-token'})
        if verify_input:
            self.verification_token = verify_input.get('value')
            print(f"   ✓ Verification token: {self.verification_token[:16]}...")
        else:
            print("   ⚠️  Verification token not found")

    def _build_result(self) -> dict:
        """Build result dictionary"""
        return {
            "DDB_BASE_URL": self.BASE_URL,
            "DDB_COOKIES": self.cookies,
            "DDB_SECURITY_TOKEN": self.security_token,
            "DDB_AUTHENTICITY_TOKEN": self.authenticity_token,
            "REQUEST_VERIFICATION_TOKEN": self.verification_token,
            "DDB_USER_ID": self.user_id or "unknown",
            "DDB_USERNAME": self.username or "unknown",
        }

    def save_to_env_file(self, env_path: str = None):
        """
        Save extracted tokens to .env file

        Args:
            env_path: Path to .env file (default: DNDBeyond/.env)
        """
        if not env_path:
            env_path = Path(__file__).parent.parent / ".env"
        else:
            env_path = Path(env_path)

        result = self._build_result()

        # Read existing .env if it exists
        existing_lines = []
        token_keys = set(result.keys())

        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Keep lines that don't start with our token keys
                    if not any(line.startswith(f"{key}=") for key in token_keys):
                        existing_lines.append(line)

        # Write new .env
        with open(env_path, 'w') as f:
            # Write existing non-token lines
            for line in existing_lines:
                if line:  # Skip empty lines
                    f.write(f"{line}\n")

            # Add separator if there were existing lines
            if existing_lines:
                f.write("\n")

            # Write new tokens
            f.write("# D&D Beyond Authentication Tokens\n")
            f.write(f"# Generated: {__import__('datetime').datetime.now().isoformat()}\n")
            f.write("# Note: These tokens expire periodically and need to be refreshed\n\n")

            for key, value in result.items():
                if value:  # Only write non-empty values
                    f.write(f'{key}="{value}"\n')

        print(f"\n💾 Saved tokens to: {env_path}")
        print("\n⚠️  Security reminder:")
        print("   - The .env file contains sensitive credentials")
        print("   - Make sure it's listed in .gitignore")
        print("   - Never commit this file to version control")
        print("   - Tokens expire periodically - re-run this script when they do")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract D&D Beyond authentication tokens",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (safest - credentials not in shell history)
  poetry run python DNDBeyond/scripts/get_ddb_tokens.py

  # Using environment variables (recommended)
  export DDB_EMAIL='your-email@example.com'
  export DDB_PASSWORD='your-password'
  poetry run python DNDBeyond/scripts/get_ddb_tokens.py

  # With arguments (not recommended - stays in shell history)
  poetry run python DNDBeyond/scripts/get_ddb_tokens.py \\
      --email your-email@example.com \\
      --password your-password

  # Headless mode (no browser window)
  poetry run python DNDBeyond/scripts/get_ddb_tokens.py --headless
        """
    )

    parser.add_argument("--email", help="D&D Beyond account email")
    parser.add_argument("--password", help="D&D Beyond account password")
    parser.add_argument("--headless", action="store_true",
                       help="Run browser in headless mode (no visible window)")
    parser.add_argument("--output", help="Path to save .env file (default: DNDBeyond/.env)")
    parser.add_argument("--print-only", action="store_true",
                       help="Print tokens to stdout instead of saving to file")

    args = parser.parse_args()

    # Get credentials
    email = args.email or os.getenv("DDB_EMAIL")
    password = args.password or os.getenv("DDB_PASSWORD")

    # Prompt for credentials if not provided
    if not email:
        email = input("D&D Beyond email: ").strip()
    if not password:
        import getpass
        password = getpass.getpass("D&D Beyond password: ")

    # Extract tokens
    extractor = DDBTokenExtractor(headless=args.headless)

    try:
        result = extractor.extract_tokens(email, password)

        if args.print_only:
            # Print to stdout
            print("\n" + "=" * 60)
            print("EXTRACTED TOKENS")
            print("=" * 60)
            for key, value in result.items():
                if value:
                    print(f"{key}={value}")
            print("=" * 60)
        else:
            # Save to .env file
            extractor.save_to_env_file(args.output)

            print("\n✅ All done! You can now use the D&D Beyond sync notebooks.")
            print("\n💡 Next steps:")
            print("   1. Open DNDBeyond/dnd_beyond_spells.ipynb")
            print("   2. Run the cells - credentials will be loaded from .env")
            print("   3. Sync your spells to D&D Beyond!")

        return 0

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
