# Car Showroom Chatbot

**Car Showroom** is an intelligent chatbot integrated with a web application built using Django. The chatbot is designed to assist users with various functionalities related to car showroom management. It supports advanced features like classification of queries, live transcription, and seamless interaction with backend services.

---

## **Features**

### **1. Intelligent Chatbot**
- The chatbot leverages **guard agents** and a **classification agent** to handle diverse queries effectively.
- It can classify queries into categories such as:
  - **Appointment Scheduler**
  - **Shop Information**
  - **New Cars**
  - **Used Cars**

### **2. Pinecone Vector Database**
- Data is stored and retrieved efficiently using **Pinecone**, a powerful vector database.
- This enables fast and accurate query processing for the chatbot.

### **3. Django Web Integration**
- The chatbot is seamlessly integrated with a Django web application.
- The front-end template includes a **Clear Message** option that allows users to:
  - Clear chat history.
  - Reset conversations with the chatbot.
- **Django sessions** are used to manage chat history at the backend, ensuring smooth and secure interactions.

### **4. Live Transcription and Response**
- **Speak to Send**: Users can speak their queries, and the chatbot transcribes the speech to text in real-time.
- **Audio Responses**: The chatbot's replies can be read **and heard**, enhancing accessibility and user experience.
  - This feature makes it easier for users who prefer auditory interactions.

### **5. User-Friendly Interface**
- A clean and intuitive UI ensures that users can interact with the chatbot effortlessly.
- Designed to improve customer engagement and provide instant assistance.

---

## **How It Works**
1. **Query Classification**: The chatbot identifies the intent behind the user's query and routes it to the appropriate agent.
2. **Data Storage and Retrieval**: Pinecone stores the data in vector format, allowing the chatbot to process queries efficiently.
3. **Session Management**: Django sessions handle chat history and user interactions.
4. **Live Transcription**: Users can interact with the chatbot using voice commands and receive audio responses, making the experience highly interactive and accessible.


