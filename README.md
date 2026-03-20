# 🍳 RecipeAI - AI-Powered Recipe Generator

An intelligent recipe generation application that creates delicious recipes from any ingredients you have on hand. Built with a modern AI-powered backend and a stunning ChatGPT-like frontend interface.

## ✨ Features

- 🤖 **AI-Powered Recipe Generation** - Uses advanced AI models to generate recipes based on ingredients
- 📸 **Beautiful Food Images** - Fetches food images from Unsplash API for visual inspiration
- 💬 **ChatGPT-like Interface** - Modern, intuitive chat-based UI with conversation history
- 🌙 **Dark/Light UI Theme** - Modern design with glass-morphism effects and smooth animations
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile devices
- 💾 **Conversation History** - Save and revisit previous recipe generations
- ⚡ **Fast & Instant Results** - Get recipe results in seconds

## 🏗️ Project Structure

```
reciepe_ai/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # App styles
│   │   ├── index.css        # Global styles
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Frontend dependencies
│   ├── vite.config.js       # Vite configuration
│   └── index.html           # HTML template
│
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── main.py          # FastAPI app initialization
│   │   ├── routes.py        # API routes
│   │   ├── generator.py     # Recipe generation logic
│   │   ├── model_loader.py  # AI model loading
│   │   ├── recipe_engine.py # Recipe engine
│   │   └── schemas.py       # Pydantic schemas
│   ├── requirements.txt     # Python dependencies
│   └── venv/               # Python virtual environment
│
├── models/                  # Pre-trained models
│   └── finalmodel/         # Fine-tuned recipe generation model
│
└── .gitignore              # Git ignore rules
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🔗 API Endpoints

### Generate Recipe
```
POST /generate
Content-Type: application/json

{
  "ingredients": "chicken, garlic, onions, tomatoes"
}

Response:
{
  "recipe": "Recipe text here..."
}
```

## 🎨 UI Features

- **Sidebar Navigation**: Easily manage conversation history
- **Message Bubbles**: ChatGPT-like message formatting with user and AI avatars
- **Image Display**: Beautiful recipe images with smooth animations
- **Quick Actions**: Copy recipes and start new conversations
- **Loading States**: Animated loading indicators
- **Responsive Design**: Adapts to all screen sizes

## 🛠️ Tech Stack

### Frontend
- React 18
- Vite
- Modern CSS with animations and glass-morphism effects

### Backend
- FastAPI
- Python 3.8+
- Transformers/Llama models
- CORS enabled for cross-origin requests

### External APIs
- Unsplash API for food images

## 📋 Configuration

### Environment Variables

Create `.env` file in backend directory:
```
API_KEY=your_api_key_here
MODEL_PATH=./models/finalmodel
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Unsplash API for beautiful food images
- OpenAI for AI capabilities
- The open-source community

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ by RecipeAI Team
