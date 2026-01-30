# Ankit's Minimalist Blog

A custom, minimalist, text-first blog built with Hugo.
No theme dependencies. Just clean HTML and CSS.

## 🚀 Quick Start

### Prerequisites
- Hugo Extended (latest version)
- Git

### Run Locally

```bash
# Clone the repository
git clone https://github.com/ankitmodi/ankit-site.git
cd ankit-site

# Start the server (with drafts enabled)
hugo server -D
```

Visit `http://localhost:1313`.

## ✍️ Writing a New Post

Run the following command to create a new post:

```bash
hugo new content posts/my-new-post.md
```

This will create a file in `content/posts/my-new-post.md`.
Edit the file using Markdown. Set `draft: false` when ready to publish.

## 🚢 Publishing

The site is automatically deployed to GitHub Pages via GitHub Actions when you push to the `main` branch.

```bash
git add .
git commit -m "New post: My New Post"
git push origin main
```

## 🛠 Project Structure

- `content/`: Markdown content.
- `layouts/`: HTML templates (no theme folder!).
- `assets/css/`: Main CSS file.
- `hugo.toml`: Site configuration.
- `.github/workflows/`: Deployment automation.

## 🎨 Customization

- **Styles**: Edit `assets/css/main.css`.
- **Layouts**: Edit files in `layouts/`.
- **Config**: Edit `hugo.toml`.
