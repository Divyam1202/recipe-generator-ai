# Recipe Generator AI - Complete Documentation

## Table of Contents
1. [How It Works](#how-it-works)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Model Details](#model-details)
5. [Performance](#performance)
6. [File Descriptions](#file-descriptions)
7. [Output Format](#output-format)
8. [Examples](#examples)
9. [Customization](#customization)
10. [Troubleshooting](#troubleshooting)
11. [Future Improvements](#future-improvements)
12. [Contributing](#contributing)

---

## How It Works

### 1. PDF Extraction
- Reads PDF files from `book/` directory
- Extracts text from each page
- Cleans and normalizes whitespace
- Saves extracted text to `txt_output/`

### 2. Data Preparation
- Splits extracted text into individual recipe chunks
- Converts to JSONL format with metadata (book name, recipe ID, text)
- Transforms recipes into instruction-response pairs for training

### 3. Model Fine-tuning
- **Base Model:** mistralai/Mistral-7B-Instruct-v0.2
- **Quantization:** 4-bit (NF4) for memory efficiency
- **LoRA Configuration:**
  - Rank (r): 8
  - Alpha: 16
  - Target modules: Q and V projections
  - Training: 1 epoch with gradient accumulation

### 4. Recipe Generation
- Accepts user ingredient input in natural language
- Normalizes ingredients (handles "and", "with", etc.)
- Generates comprehensive recipes including:
  - Ingredient lists with quantities
  - Step-by-step instructions
  - Good ingredient combination explanations
  - Bad ingredient combination warnings
  - Suggested variations and improvements

---

## Installation

### Requirements
- Python 3.8+
- GPU with CUDA support (recommended for training)
- ~20GB disk space for model and data

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Divyam1202/recipe-generator-ai.git
   cd recipe-generator-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **For frontend setup:**
   ```bash
   cd frontend
   npm install
   ```

4. **For backend setup:**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r ../requirements.txt
   ```

### Dependencies

**Core Libraries:**
- `transformers`: HuggingFace model loading and inference
- `peft`: LoRA (Parameter-Efficient Fine-Tuning) implementation
- `bitsandbytes`: 4-bit quantization
- `torch`: Deep learning framework
- `datasets`: Dataset loading and processing
- `pdfplumber`: PDF text extraction
- `accelerate`: Multi-GPU training support
- `fastapi`: Backend API framework
- `react`: Frontend framework (Vite)

See `requirements.txt` for complete dependency list with versions.

---

## Usage

### Backend Setup

1. **Activate Python environment:**
   ```bash
   cd backend
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Start the backend server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your backend URL
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

### API Endpoints

**Generate Recipe:**
```bash
POST /generate
Content-Type: application/json

{
  "ingredients": "tomatoes, basil, garlic, pasta"
}
```

**Get History:**
```bash
GET /history
```

**Save Conversation:**
```bash
POST /save-conversation
Content-Type: application/json

{
  "id": "conversation_id",
  "title": "Recipe Title",
  "messages": [...]
}
```

**Delete Conversation:**
```bash
POST /delete-conversation
Content-Type: application/json

{
  "id": "conversation_id"
}
```

**Clear History:**
```bash
POST /clear-history
```

### Training Pipeline (in Jupyter)

```python
# 1. Extract PDFs to text
extract_pdfs_to_separate_txt(PDF_DIR, TXT_DIR)

# 2. Build recipes JSONL
build_jsonl_from_txt(TXT_DIR, RECIPES_JSONL)

# 3. Convert to training format
convert_to_instruction_format(RECIPES_JSONL, TRAIN_JSONL)

# 4. Load dataset
dataset = load_dataset("json", data_files=TRAIN_JSONL)["train"]

# 5. Fine-tune model (see notebook for full training code)
```

---

## Model Details

| Property | Value |
|----------|-------|
| Base Model | Mistral-7B-Instruct-v0.2 (7.3B parameters) |
| Quantization | 4-bit NF4 |
| Fine-tuning Method | LoRA with ~3.3M trainable parameters |
| Max Sequence Length | 512 tokens |
| Model Size (quantized) | ~8GB |
| VRAM for Training | ~16GB |
| VRAM for Inference | ~8GB |

---

## Performance

| Metric | Value |
|--------|-------|
| Inference Speed | ~5-10 sec per recipe (GPU), slower on CPU |
| Model Size | ~8GB (quantized) |
| Training Time | ~2-4 hours (varies by dataset size) |
| Output Quality | Detailed, multi-section recipes |

---

## File Descriptions

| File | Purpose |
|------|---------|
| `reciepe_bot.ipynb` | Complete pipeline from PDF extraction to inference |
| `recipes.jsonl` | Raw extracted recipes with metadata |
| `train_data.jsonl` | Instruction-response pairs for fine-tuning |
| `book/` | Input PDF recipe books |
| `txt_output/` | Extracted text files from PDFs |
| `finalmodel/` | Fine-tuned LoRA adapter and tokenizer |
| `frontend/src/App.jsx` | Main React component |
| `backend/app/routes.py` | API endpoints |
| `backend/app/recipe_engine.py` | Recipe generation logic |
| `backend/app/history.py` | Conversation history management |

---

## Output Format

Generated recipes follow a structured format:

```
Recipe Title:
------------------------------

### Ingredients:
- item 1 with quantity
- item 2 with quantity

### Instructions:
1. First step
2. Second step
...

### Good Ingredient Combinations:
Explanation of why these ingredients work well together

### Bad Ingredient Combinations and Why:
Explanation of problematic pairings

### Suggestions:
Variations and improvements to the recipe
```

---

## Examples

### Example 1: Tomato Basil Pasta

**Input:**
```
📝 Ingredients: tomatoes, basil, garlic, pasta
```

**Output:**
```
Recipe Title:
Creamy Tomato Basil Pasta
------------------------------

### Ingredients:
- 400g pasta (penne or spaghetti)
- 500g fresh tomatoes (or 400g canned)
- 4 cloves garlic, minced
- Fresh basil leaves (about 20-25 leaves)
- 2 tbsp olive oil
- Salt and pepper to taste
- 100ml heavy cream (optional)
- Parmesan cheese for garnish

### Instructions:
1. Heat olive oil in a large pan over medium heat
2. Sauté minced garlic for 1-2 minutes until fragrant
3. Add chopped tomatoes and simmer for 15-20 minutes
4. Tear fresh basil leaves and add to the sauce in the last 2 minutes
5. Cook pasta according to package instructions
6. Drain pasta and mix with the tomato-basil sauce
7. Add cream if desired for a smoother texture
8. Season with salt and pepper
9. Serve topped with Parmesan cheese and fresh basil

### Good Ingredient Combinations:
Tomatoes, basil, and garlic are a classic Italian trio that complement each other perfectly. The acidity of tomatoes balances the sweetness, while basil adds a fresh, aromatic quality. Garlic ties all flavors together with its pungent depth.

### Suggestions:
- Add fresh mozzarella or ricotta for creaminess
- Include red pepper flakes for a spicy kick
- Top with toasted breadcrumbs for texture
- Use fresh cherry tomatoes for sweeter results
```

### Example 2: Mediterranean Lemon Herb Chicken

**Input:**
```
📝 Ingredients: chicken, lemon, olive oil, herbs
```

**Output:**
```
Recipe Title:
Mediterranean Lemon Herb Chicken
------------------------------

### Ingredients:
- 4 chicken breasts or thighs (about 800g)
- Juice and zest of 2 lemons
- 60ml olive oil
- 4 cloves garlic, minced
- 2 tsp dried oregano (or 1 tbsp fresh)
- 1 tsp thyme
- Salt and pepper to taste
- 250ml chicken broth
- Fresh herbs for garnish (rosemary, parsley)

### Instructions:
1. In a bowl, combine olive oil, lemon juice, lemon zest, garlic, oregano, and thyme
2. Season chicken with salt and pepper
3. Marinate chicken in herb mixture for at least 30 minutes (up to 4 hours)
4. Heat a large skillet over medium-high heat
5. Cook marinated chicken until golden, about 6-7 minutes per side
6. Add chicken broth to the pan
7. Reduce heat and simmer for 15-20 minutes until internal temperature reaches 165°F
8. Finish with fresh herbs and serve

### Good Ingredient Combinations:
Lemon and herbs are the perfect match for chicken. The acidity of lemon brightens the meat, while Mediterranean herbs add earthy, aromatic depth.

### Suggestions:
- Serve with roasted vegetables (zucchini, bell peppers, tomatoes)
- Add capers or Kalamata olives for briny notes
- Reduce the sauce after cooking for more intensity
```

---

## Customization

### Add Your Own Recipe Books
1. Place PDF files in `book/` directory
2. Run the PDF extraction cell in the notebook
3. Run the JSONL conversion cells
4. Re-train the model with new data

### Adjust Generation Parameters
Modify in `backend/app/recipe_engine.py`:

```python
max_new_tokens=2500        # Recipe length
temperature=0.4            # Creativity (0-1)
top_p=0.9                  # Diversity
repetition_penalty=1.2     # Reduce repetition
```

### Fine-tune with Different Base Model
Change in `backend/app/model_loader.py`:

```python
MODEL_NAME = "mistralai/Mistral-7B-v0.2"  # or another model
```

### Configure Environment Variables
Edit `.env.local` for frontend:

```env
VITE_API_URL=http://127.0.0.1:8000
```

---

## Troubleshooting

### CUDA Out of Memory
- Reduce `max_new_tokens` in recipe generation
- Use CPU for inference only
- Reduce batch size during training

### Slow Inference
- Use GPU if available
- Reduce `max_new_tokens` for shorter recipes
- Check that quantization is enabled

### Model Not Loading
- Ensure `finalmodel/` contains all required files
- Verify model files aren't corrupted
- Check compatible `transformers` version

### Backend Connection Issues
- Verify backend is running: `python -m uvicorn app.main:app --reload`
- Check API URL in `.env.local`
- Clear browser cache and retry
- Check CORS settings in `backend/app/main.py`

### Frontend Build Issues
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version compatibility (14+)

---

## Requirements for Running Locally

| Resource | Requirement |
|----------|-------------|
| GPU Memory | 16GB+ for training, 8GB+ for inference |
| CPU | Any modern processor |
| Storage | ~30GB for full setup (models + data) |
| OS | Linux, macOS, or Windows |
| Python | 3.8+ |
| Node.js | 14+ (for frontend) |

### CPU-only Inference (Slower)
Install CPU-compatible torch version:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

## Training on Google Colab

The notebook is optimized for Google Colab:
- Uses `/content/drive/` paths for Google Drive integration
- Includes GPU acceleration
- Handles memory efficiently with 4-bit quantization

### Steps:
1. Upload `reciepe_bot.ipynb` to Google Colab
2. Mount Google Drive: `from google.colab import drive`
3. Run cells in order
4. Download trained model when complete

---

## Future Improvements

- 🌐 Web interface with Streamlit/FastAPI
- 🔗 REST API for third-party integration
- 🎯 Support for dietary restrictions/allergies
- 🌍 Multi-language recipe support
- ⭐ Recipe difficulty ranking
- 📊 Nutritional information estimation
- 🔄 Ingredient substitution suggestions
- 📱 Mobile app version
- 🎨 Enhanced UI/UX
- 🧪 Recipe testing and validation

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## License

This project is open source and available under the **MIT License**. See `LICENSE` file for details.

---

## Author

**Divyam Chandak**
- GitHub: [@Divyam1202](https://github.com/Divyam1202)
- Project: [recipe-generator-ai](https://github.com/Divyam1202/recipe-generator-ai)

---

## Acknowledgments

- 🤖 **Mistral AI** for the excellent Mistral-7B model
- 🤗 **HuggingFace** for transformers, datasets, and PEFT libraries
- ⚡ **BitsandBytes** for efficient quantization
- 📚 Recipe data from various open-source cookbooks

---

## References

- [Mistral 7B Documentation](https://docs.mistral.ai/)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [HuggingFace PEFT](https://huggingface.co/docs/peft/)
- [BitsandBytes](https://github.com/TimDettmers/bitsandbytes)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

**Last Updated:** March 26, 2026
**Version:** 1.0.0
