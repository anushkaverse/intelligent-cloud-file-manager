
# ☁ Intelligent Cloud File Management System

![Banner](https://img.shields.io/badge/Streamlit-App-blue)
![Python](https://img.shields.io/badge/Python-3.10-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Project Overview

The **Intelligent Cloud File Management System** is a **smart desktop and cloud file organizer** that uses lightweight AI heuristics to automatically classify files into categories and helps you manage them efficiently.  

It allows you to:  
- Automatically organize files into folders like **Financial, Work, Travel, Photos**, etc.  
- Save files locally in **organized folders**.  
- Upload files securely to **your own AWS S3 bucket**.  
- Delete unwanted files effortlessly.  

No more messy desktops or folder chaos — everything is structured and accessible at a glance!  

---

## 🧠 How it Works

1️⃣ **Upload your files** – documents, spreadsheets, presentations, images, anything!  

2️⃣ **AI Classification** – the system scans your file names and content to categorize them:  
   - 📊 Financial  
   - 🖼️ Photos  
   - 📝 Work & Notes  
   - 🍳 Food & Recipes  
   - ✈️ Travel  
   - …and more!
     
3️⃣ **File Management** – effortlessly manage your files:  
   - 🖥️ **Save to Desktop** in organized folders automatically  
   - 🗑️ **Delete** files with one click  
   - ☁️ **Upload to your own S3 bucket** securely  

---

## ⚡ Features

- ✅ **AI-driven classification** for documents, spreadsheets, presentations, and images  
- ✅ **Organized desktop storage** by category  
- ✅ **Cloud integration** via user-provided AWS S3 credentials  
- ✅ **Easy deletion** of unwanted files  
- ✅ Fully built using **Python and Streamlit**  

---

## 🛠 Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/anushkaverse/intelligent-cloud-file-manager.git
cd intelligent-cloud-file-manager
````

2. **Create a virtual environment (optional but recommended):**

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the app:**

```bash
streamlit run app.py
```

---

## ☁ AWS S3 Integration

* To upload files to S3, **you must enter your own AWS credentials** in the sidebar:

  * **Bucket Name**
  * **Access Key ID**
  * **Secret Access Key**
  * **Region**

> ⚠️ **Security Tip:** Never share your credentials or include them in the code. Users must provide their own.

---

## 🗂 Folder Organization

When you save files to Desktop, the system automatically creates folders matching the **AI-assigned category**, for example:

```
Desktop/
└── Financial/
    └── invoice.xlsx
└── Travel/
    └── vacation_photo.jpg
```

---

## 💡 Demo Tips

* For demos, you can temporarily use your own S3 credentials to showcase cloud integration.
* All features can be demonstrated **without exposing your keys** to users.

---

## 📦 Dependencies

* [Python 3.x](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [boto3](https://boto3.amazonaws.com/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [Pillow](https://pypi.org/project/Pillow/)
* [transformers](https://huggingface.co/transformers/) (optional for zero-shot classification)
* [python-docx](https://pypi.org/project/python-docx/)
* [PyMuPDF](https://pypi.org/project/PyMuPDF/)

Install via:

```bash
pip install -r requirements.txt
```

---

## 📂 Project Structure

```
intelligent-cloud-file-manager/
│
├─ app.py               # Main Streamlit app
├─ classifier.py        # AI classification logic
├─ requirements.txt     # Python dependencies
├─ uploads/             # Temporary upload folder (ignored in git)
├─ organized/           # AI-organized folders (ignored in git)
└─ README.md            # Project documentation
```

## 📣 Future Improvements

* Add more **AI-powered categorization** for specialized document types
* Enable **bulk S3 uploads** and folder sync
* Add **user authentication** for multiple users

---

## 📜 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.

---

## 👋 Author

Developed by Anushka Sharma – happy file organizing!








