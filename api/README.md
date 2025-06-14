## Prerequisites

To run NumTales API locally, you will need:

- **Node.js** (v18 or newer) and **npm** for managing and running the Angular frontend.
- **Python** (3.11 recommended) for the Flask API backend.
- **Poetry** for Python dependency management.
- **MongoDB** (a local instance or MongoDB Atlas) to store stories, embeddings, and related data.
- (Optional) **Git** for version control.

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/numtales.git
   cd numtales
   ```

2. **Set up the Python backend:**
   ```sh
   cd api
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

   pip install poetry
   poetry install --no-root
   ```

3. **Set up the Angular frontend:**
   ```sh
   cd ../front-end
   npm install
   ```

4. **Start the applications:**
   - **Backend:**  
     ```sh
     cd ../api
     poetry run python search.py
     ```
   - **Frontend:**  
     ```sh
     cd ../front-end
     npm run start
     ```

5. **Access NumTales:**  
   Open your browser and go to [http://localhost:4200](http://localhost:4200)

## Vector Searching with MongoDB Atlas

MongoDB Atlas vector search lets you find documents based on the meaning of their content instead of just matching keywords. The basic idea is to convert unstructured data such as text, images, or audio into numerical vectors using machine learning models. These vectors are stored along with your documents in MongoDB. Then, when you make a search query, you convert that query into a vector in the same numeric space. The database finds the documents whose vectors most closely match the query vector.

Under the hood, this technology uses techniques like K-nearest neighbors (KNN) search combined with approximate algorithms. Similarity metrics like cosine similarity are used to measure how close two vectors are. In practice, if you have an image or a story turned into a vector, MongoDB Atlas can find similar items based on the overall context rather than relying on exact words or tags. This hybrid approach lets you mix traditional metadata filters with vector-based criteria, providing search results that are both broad in meaning and precise in context.

One of the great benefits of using MongoDB Atlas vector search in NumTales is that your operational data and the vector embeddings live together in one system. This integration simplifies your stack, making it easier to build intelligent applications such as recommendation engines, conversational agents, or retrieval-augmented generation systems. It paves the way for a search experience that truly understands user intent, matching mathematical narratives or artistic themes with rich contextual similarity.

## License

MIT License

Enjoy exploring numbers in a whole new way with NumTales!