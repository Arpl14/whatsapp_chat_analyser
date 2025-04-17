
# 📊 WhatsApp Chat Analyzer 

![Untitled design](https://github.com/user-attachments/assets/0052aeab-b0c5-4ad6-9224-f31bab6725b3)

An interactive web app that performs **data-driven analysis** on exported WhatsApp group chats using **NLP**, **Network Analysis**, **Sentiment analysis** and  **Topic Modeling**. It generates insightful statistics, sentiment trends, activity heatmaps, and network visualizations of group dynamics.
Use the app : https://whatsappchatanalyser-5jh9gvrmmkcmjqkdpbuvql.streamlit.app/
---

## 🚀 Project Overview

This project enables users to upload a `.txt` WhatsApp group chat file and receive comprehensive analytics about:
- **User engagement**
- **Sentiment trends**
- **Message activity patterns**
- **Topic clusters**
- **User interaction networks**

The goal is to convert raw WhatsApp chat logs into **visual, interpretable insights** using cutting-edge data science techniques.

---
## 🏆 Key Features & Achievements

-  Group and individual-level message statistics  
-  Topic modeling using **LDA** with dynamic word clouds to uncover latent themes  
-  Sentiment analysis over time & by user using **TextBlob/VADER**  
-  User segmentation & engagement detection with responsive UI  
-  Visualized **user responsiveness** using directional **network graphs** via NetworkX  
-  Temporal trends: Message frequency by month-year and day of the week  
-  Handles noisy, unstructured WhatsApp data with regex and preprocessing  
-  Supports multi-user chats, emojis, hyperlinks, media tags, and system messages  
-  Built a fully functional **end-to-end Streamlit app** using a modular architecture (`preprocess.py`, `stats.py`)  
-  Enabled **interactive exploratory analysis** with minimal user input and maximum insight
---

## ⚙️ Technical Implementation

**Languages & Frameworks:**
- Python
- Streamlit for frontend
- Pandas, NumPy for data wrangling
- Matplotlib, Seaborn for visualizations

**Key Libraries & Techniques:**
- **NLTK / spaCy** – for text preprocessing and stopword removal  
- **Scikit-learn / Gensim** – for LDA-based topic modeling  
- **TextBlob / VADER** – for sentiment analysis  
- **NetworkX** – for user interaction graph  
- **Regex** – for parsing WhatsApp message patterns  
- **PyLDAVis** – for topic visualization (optional)  
- **WordCloud** – for visual word distributions

---

## ▶️ Project Run-through

1. Download your own whatsapp group chat by navigating to : group -> group info -> export chat -> without media -> unzip and save as .txt file
2. Upload a WhatsApp `.txt` chat file in the sidebar.
3. Select a specific user or 'Overall' for group insights.
4. The app generates:
   - General & user-specific stats
   - Word clouds
   - Monthly message frequency
   - Weekday activity plots
   - Sentiment timeline
   - Topic clusters
   - Interaction network (for group analysis)

---

## 🛠️ How to Use

1. Use the project live by visiting : https://whatsappchatanalyser-5jh9gvrmmkcmjqkdpbuvql.streamlit.app/

   
### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer 

