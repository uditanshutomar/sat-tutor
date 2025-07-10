# SAT Tutor - AI-Powered SAT Preparation System

An intelligent SAT preparation system that combines knowledge graphs, semantic augmentation, and Large Language Models (LLMs) to provide personalized SAT tutoring with GPU acceleration support.

## 🚀 Features

- **Knowledge Graph Integration**: Builds and queries semantic knowledge graphs from educational content
- **Semantic Augmentation**: Enhances questions and explanations using AI models
- **GPU Acceleration**: Optimized for AMD GPUs using DirectML on Windows
- **Multi-Model Support**: Works with both local models and cloud APIs (Groq)
- **Interactive Learning**: Provides detailed explanations and concept extraction
- **Cross-Platform**: Supports Windows, macOS, and Linux

## 🏗️ Architecture

The system consists of several key components:

- **Knowledge Graph Module** (`knowledge_graph.py`): Manages semantic relationships and entity extraction
- **Semantic Augmenter** (`semantic_augmenter.py`): Enhances content using LLMs with GPU acceleration
- **Graph RAG** (`graph_rag.py`): Retrieval-Augmented Generation using knowledge graphs
- **Main Application** (`sat_tutor.py`): Orchestrates all components for SAT tutoring

## 🛠️ Installation

### Prerequisites

- Python 3.10 or higher
- AMD GPU (for DirectML acceleration) or NVIDIA GPU (for CUDA)
- Windows 10/11 (for DirectML support)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sat-tutor.git
   cd sat-tutor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv sat-tutor-env
   ```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     sat-tutor-env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source sat-tutor-env/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### GPU Acceleration Setup

#### For AMD GPUs (DirectML - Windows)

1. **Install DirectML**:
   ```bash
   pip install torch-directml
   ```

2. **Verify installation**:
   ```bash
   python -c "import torch_directml; print('DirectML available:', torch_directml.is_available())"
   ```

#### For NVIDIA GPUs (CUDA)

1. **Install PyTorch with CUDA**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Verify installation**:
   ```bash
   python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
   ```

## 🚀 Usage

### Basic Usage

```python
from sat_tutor import SATTutor

# Initialize the tutor
tutor = SATTutor()

# Ask a question
question = "What is the quadratic formula?"
answer = tutor.ask_question(question)
print(answer)
```

### Advanced Usage

```python
from semantic_augmenter import SemanticAugmenter
from knowledge_graph import KnowledgeGraph

# Initialize components
augmenter = SemanticAugmenter(use_groq=False, model_name="gpt2")
knowledge_graph = KnowledgeGraph()

# Extract concepts from text
text = "The American Revolution was a political and military conflict..."
concepts = augmenter.extract_concepts(text)

# Build knowledge graph
knowledge_graph.add_concepts(concepts)

# Generate explanations
explanation = augmenter.generate_explanation(
    question="What caused the American Revolution?",
    correct_answer="Taxation without representation",
    wrong_answers=["British military weakness", "French intervention"]
)
```

## 📁 Project Structure

```
sat-tutor/
├── sat_tutor.py              # Main application
├── knowledge_graph.py        # Knowledge graph management
├── semantic_augmenter.py     # AI model integration
├── graph_rag.py             # Graph-based RAG system
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── .gitignore              # Git ignore rules
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Groq API (optional)
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration
DEFAULT_MODEL=gpt2
USE_GPU=true
```

### Model Configuration

The system supports various models:

- **Local Models**: GPT-2, OPT, Llama-2 (requires sufficient RAM/VRAM)
- **Cloud APIs**: Groq (requires API key)

## 🧪 Testing

Run the GPU acceleration test:

```bash
python test_gpu.py
```

Test DirectML functionality:

```bash
python test_directml.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Microsoft DirectML for AMD GPU support
- Groq for cloud inference API
- The SAT community for educational content

## 📞 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/yourusername/sat-tutor/issues) page
2. Create a new issue with detailed information
3. Include your system specifications and error messages

## 🔄 Updates

Stay updated with the latest features and improvements:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Note**: This project is designed for educational purposes. Always verify AI-generated content and explanations for accuracy. 