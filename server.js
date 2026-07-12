// Import modules
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const fs = require("fs");

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Dummy database file
const DB_FILE = "users.json";

// Ensure file exists
if (!fs.existsSync(DB_FILE)) {
    fs.writeFileSync(DB_FILE, JSON.stringify([]));
}

// 🔹 SIGNUP API
app.post("/signup", (req, res) => {
    const { name, email, password } = req.body;

    let users = JSON.parse(fs.readFileSync(DB_FILE));

    // Check if user exists
    const userExists = users.find(u => u.email === email);
    if (userExists) {
        return res.json({ message: "User already exists!" });
    }

    // Add new user
    users.push({ name, email, password });

    fs.writeFileSync(DB_FILE, JSON.stringify(users));

    res.json({ message: "Signup successful!" });
});

// 🔹 LOGIN API
app.post("/login", (req, res) => {
    const { email, password } = req.body;

    let users = JSON.parse(fs.readFileSync(DB_FILE));

    const user = users.find(
        u => u.email === email && u.password === password
    );

    if (user) {
        res.json({ message: "Login successful", user });
    } else {
        res.json({ message: "Invalid credentials" });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});