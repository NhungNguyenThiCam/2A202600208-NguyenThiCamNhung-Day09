"""
build_index.py — Build ChromaDB index từ documents
Chạy script này trước khi test pipeline.

Usage:
    python build_index.py
"""

import os
import chromadb
from sentence_transformers import SentenceTransformer

def build_index():
    """Build ChromaDB index từ data/docs/"""
    print("=" * 60)
    print("Building ChromaDB Index")
    print("=" * 60)
    
    # Initialize ChromaDB
    client = chromadb.PersistentClient(path='./chroma_db')
    
    # Delete existing collection if any
    try:
        client.delete_collection('day09_docs')
        print("✓ Deleted existing collection")
    except:
        pass
    
    # Create new collection
    collection = client.create_collection(
        'day09_docs',
        metadata={"hnsw:space": "cosine"}
    )
    print("✓ Created collection 'day09_docs'")
    
    # Load embedding model
    print("\n📦 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Model loaded")
    
    # Read and index documents
    docs_dir = './data/docs'
    documents = []
    metadatas = []
    ids = []
    
    print(f"\n📄 Reading documents from {docs_dir}...")
    for fname in os.listdir(docs_dir):
        if not fname.endswith('.txt'):
            continue
            
        fpath = os.path.join(docs_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks (simple split by paragraphs)
        chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
        
        for i, chunk in enumerate(chunks):
            if len(chunk) < 20:  # Skip very short chunks
                continue
            documents.append(chunk)
            metadatas.append({
                "source": fname,
                "chunk_id": i,
            })
            ids.append(f"{fname}_{i}")
        
        print(f"  ✓ {fname}: {len(chunks)} chunks")
    
    # Generate embeddings and add to collection
    print(f"\n🔢 Generating embeddings for {len(documents)} chunks...")
    embeddings = model.encode(documents, show_progress_bar=True)
    
    print("\n💾 Adding to ChromaDB...")
    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"\n✅ Index built successfully!")
    print(f"   Total chunks: {len(documents)}")
    print(f"   Collection: day09_docs")
    print(f"   Path: ./chroma_db")
    
    # Test query
    print("\n🔍 Testing index with sample query...")
    test_query = "SLA ticket P1"
    test_embedding = model.encode([test_query])[0].tolist()
    results = collection.query(
        query_embeddings=[test_embedding],
        n_results=2
    )
    
    print(f"   Query: '{test_query}'")
    print(f"   Top result: {results['documents'][0][0][:100]}...")
    print(f"   Source: {results['metadatas'][0][0]['source']}")
    
    print("\n" + "=" * 60)
    print("✅ Setup complete! You can now run: python graph.py")
    print("=" * 60)

if __name__ == "__main__":
    build_index()
