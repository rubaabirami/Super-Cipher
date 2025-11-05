from flask import Flask, render_template, request, redirect, url_for, session

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Secret key for session management

# Dummy credentials for login
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

# Helper functions for Vigenère Cipher
def vigenere_encrypt(text, key):
    encrypted = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            if char.isupper():
                encrypted += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            key_index = (key_index + 1) % len(key)
        else:
            encrypted += char
    return encrypted

def vigenere_decrypt(ciphertext, key):
    decrypted = ""
    key = key.upper()
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index]) - ord('A')
            if char.isupper():
                decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            key_index = (key_index + 1) % len(key)
        else:
            decrypted += char
    return decrypted

# Helper functions for Polybius Cipher
polybius_square = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'K'],
    ['L', 'M', 'N', 'O', 'P'],
    ['Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z']
]

def polybius_encrypt(text):
    text = text.upper().replace("J", "I")
    encrypted = ""
    for char in text:
        if char.isalpha():
            for i, row in enumerate(polybius_square):
                if char in row:
                    encrypted += str(i + 1) + str(row.index(char) + 1)
        else:
            encrypted += char
    return encrypted

def polybius_decrypt(ciphertext):
    decrypted = ""
    i = 0
    while i < len(ciphertext):
        if ciphertext[i].isdigit() and i + 1 < len(ciphertext) and ciphertext[i + 1].isdigit():
            row = int(ciphertext[i]) - 1
            col = int(ciphertext[i + 1]) - 1
            decrypted += polybius_square[row][col]
            i += 2
        else:
            decrypted += ciphertext[i]
            i += 1
    return decrypted

# Login route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("homepage"))
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")
    return render_template("login.html")

# Homepage route
@app.route("/homepage")
def homepage():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html")

# Cipher page route
@app.route("/cipher", methods=["GET", "POST"])
def cipher():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    result = ""
    if request.method == "POST":
        mode = request.form["mode"]
        text = request.form["text"]
        key = request.form.get("key", "")

        if mode == "encode":
            # First Vigenere, then Polybius
            intermediate = vigenere_encrypt(text, key)
            result = polybius_encrypt(intermediate)
        elif mode == "decode":
            # First Polybius, then Vigenere
            intermediate = polybius_decrypt(text)
            result = vigenere_decrypt(intermediate, key)

    return render_template("cipher.html", result=result)

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
