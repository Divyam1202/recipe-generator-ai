# 🍳 ChefAI — LLM-Powered Recipe Generator

An intelligent recipe generation system that combines semantic recipe retrieval with a fine-tuned language model to generate structured, step-by-step cooking instructions from a list of ingredients.

---

## What It Does

ChefAI takes a list of ingredients, finds semantically similar recipes using embeddings, and synthesises a new structured recipe by combining relevant culinary patterns — powered by a locally hosted fine-tuned LLM served via FastAPI.

---

## Architecture

```
User Input (Ingredients)
        ↓
Embedding Model
(Semantic similarity search across recipe corpus)
        ↓
Top-K Similar Recipe Combinations Retrieved
        ↓
Fine-tuned LLM (Llama/Mistral — GGUF quantized)
(Generates new structured recipe from combinations)
        ↓
Structured Recipe Output (dish name + steps)
```

**Decoupled system design:**
- Embedding layer runs at inference time for semantic ingredient matching
- Fine-tuned LLM synthesises recipes from retrieved combinations — not direct retrieval
- Frontend and backend are independently deployable
- CORS-configured middleware for secure cross-service communication

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Custom CSS (Glass-morphism) |
| Backend | Python 3.x, FastAPI |
| Embeddings | Sentence Transformers (semantic recipe retrieval) |
| AI Engine | Fine-tuned Llama / Mistral (HuggingFace + Unsloth) |
| Quantization | GGUF (4-bit) for optimised local inference |
| Deployment | Vercel (Frontend), Render (Backend) |
| Assets | Unsplash API for dynamic food imagery |

---

## Model Details

- **Base model:** Llama 3 / Mistral
- **Fine-tuning:** Custom culinary dataset in `.jsonl` format
- **Embeddings:** Pre-computed recipe corpus embeddings for semantic similarity
- **Optimisation:** GGUF quantization for faster inference and reduced memory footprint
- **Training framework:** Unsloth + HuggingFace Transformers

---

## API

### `POST /generate`

**Request:**
```json
{
  "ingredients": ["chicken", "garlic", "lemon", "olive oil", "rosemary"]
}
```

**Response:**
```json
{
  "dish_name": "Lemon Herb Roasted Chicken",
  "ingredients": [
    "2 chicken breasts",
    "3 cloves garlic, minced",
    "1 lemon, juiced",
    "2 tbsp olive oil",
    "1 tsp fresh rosemary"
  ],
  "steps": [
    "Preheat oven to 200°C.",
    "Mix olive oil, garlic, lemon juice, and rosemary.",
    "Coat chicken and marinate for 20 minutes.",
    "Roast for 25-30 minutes until golden."
  ]
}
```

---

## Local Setup

```bash
# Clone the repo
git clone https://github.com/Divyam1202/recipe-generator-ai
cd recipe-generator-ai

# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Full setup guide: [setup.md](./setup.md)

---

## Live Demo

Frontend: [recipe-generator-ai-phi.vercel.app](https://recipe-generator-ai-phi.vercel.app)

---

## License

MIT License

This project is available under the MIT License.
