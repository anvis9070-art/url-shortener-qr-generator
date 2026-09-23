import pyshorteners
import qrcode
import re
from datetime import datetime

HISTORY_FILE = "url_history.txt"


# -----------------------------
# Validate URL
# -----------------------------
def is_valid_url(url):
    pattern = r"^(https?://)?([\w-]+\.)+[\w-]+(/[^\s]*)?$"
    return re.match(pattern, url) is not None


# -----------------------------
# Shorten URL
# -----------------------------
def shorten_url(url):
    try:
        shortener = pyshorteners.Shortener()
        short_url = shortener.tinyurl.short(url)
        return short_url

    except Exception as e:
        print("Error while shortening URL:", e)
        return None


# -----------------------------
# Generate QR Code
# -----------------------------
def generate_qr(url):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"qr_code_{timestamp}.png"

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )

        qr.add_data(url)
        qr.make(fit=True)

        qr_image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        qr_image.save(filename)

        print(f"\nQR Code generated successfully!")
        print(f"Saved as: {filename}")

    except Exception as e:
        print("Error while generating QR code:", e)


# -----------------------------
# Save URL History
# -----------------------------
def save_history(original_url, short_url):
    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(f"{original_url} -> {short_url}\n")

    except Exception as e:
        print("Error while saving history:", e)


# -----------------------------
# Show URL History
# -----------------------------
def show_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = file.read()

        if history.strip():
            print("\n----- URL HISTORY -----")
            print(history)
        else:
            print("\nNo URL history found.")

    except FileNotFoundError:
        print("\nNo URL history found.")


# -----------------------------
# Main Program
# -----------------------------
def main():

    while True:

        print("\n==============================")
        print("   URL SHORTENER & QR GENERATOR")
        print("==============================")
        print("1. Shorten URL")
        print("2. Generate QR Code")
        print("3. View URL History")
        print("4. Exit")
        print("==============================")

        choice = input("\nEnter your choice: ").strip()

        # -----------------------------
        # Option 1: Shorten URL
        # -----------------------------
        if choice == "1":

            url = input("\nEnter the URL: ").strip()

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            if not is_valid_url(url):
                print("\nInvalid URL. Please enter a valid URL.")
                continue

            print("\nShortening URL...")

            short_url = shorten_url(url)

            if short_url:
                print("\nOriginal URL:")
                print(url)

                print("\nShortened URL:")
                print(short_url)

                save_history(url, short_url)

                # Generate QR code for shortened URL
                generate_qr(short_url)

        # -----------------------------
        # Option 2: Generate QR Code
        # -----------------------------
        elif choice == "2":

            url = input("\nEnter URL for QR Code: ").strip()

            if not url:
                print("\nPlease enter a URL.")
                continue

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            if not is_valid_url(url):
                print("\nInvalid URL. Please enter a valid URL.")
                continue

            generate_qr(url)

        # -----------------------------
        # Option 3: View History
        # -----------------------------
        elif choice == "3":
            show_history()

        # -----------------------------
        # Option 4: Exit
        # -----------------------------
        elif choice == "4":
            print("\nThank you for using the URL Shortener!")
            print("Goodbye!")
            break

        # -----------------------------
        # Invalid option
        # -----------------------------
        else:
            print("\nInvalid choice. Please select 1, 2, 3, or 4.")


# -----------------------------
# Run Program
# -----------------------------
if __name__ == "__main__":
    main()