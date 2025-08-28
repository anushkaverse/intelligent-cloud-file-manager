import streamlit as st
from pathlib import Path
import shutil
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from classifier import classify_file

# --- Load env/secrets (hidden, never exposed to users) ---
load_dotenv()
AWS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
# S3_BUCKET not used for users; they must input their own
# --- Configuration ---
BASE_UPLOAD = Path("uploads")
ORG = Path("organized")
BASE_UPLOAD.mkdir(exist_ok=True)
ORG.mkdir(exist_ok=True)

st.set_page_config(page_title="Intelligent Cloud File Management System", layout="wide")
st.title("☁ Intelligent Cloud File Management System")
st.write("Upload files and let AI classify & organize them into folders.")

# --- Sidebar: S3 settings (user must input their own) ---
st.sidebar.header("AWS S3 (for sending files to S3 storage buckets)")
use_s3 = st.sidebar.checkbox("Enable S3 actions", value=False)

s3_bucket = ""
aws_key = ""
aws_secret = ""
aws_region = ""

if use_s3:
    st.sidebar.warning("Enter your own S3 credentials.")
    s3_bucket = st.sidebar.text_input("S3 bucket name", value="")
    aws_key = st.sidebar.text_input("AWS Access Key", type="password", value="")
    aws_secret = st.sidebar.text_input("AWS Secret Key", type="password", value="")
    aws_region = st.sidebar.text_input("AWS Region (optional)", value="")

def get_s3_client():
    if not aws_key or not aws_secret or not s3_bucket:
        return None
    return boto3.client(
        "s3",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region or None
    )

# Initialize session state for deleted file tracking
if "deleted_file" not in st.session_state:
    st.session_state.deleted_file = None

# --- Upload Area ---
st.subheader("Upload files")
uploaded = st.file_uploader("Choose files (multiple allowed)", accept_multiple_files=True)

if st.button("Upload and Organize"):
    if not uploaded:
        st.info("Please choose files to upload.")
    else:
        results = []
        with st.spinner("Saving and organizing..."):
            for up in uploaded:
                tmp_path = BASE_UPLOAD / up.name
                with open(tmp_path, "wb") as f:
                    f.write(up.getbuffer())

                category, tags = classify_file(str(tmp_path), up.name)
                dest_dir = ORG / category
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_path = dest_dir / up.name

                if dest_path.exists():
                    stem = dest_path.stem
                    suf = dest_path.suffix
                    i = 1
                    while (dest_dir / f"{stem}_{i}{suf}").exists():
                        i += 1
                    dest_path = dest_dir / f"{stem}_{i}{suf}"

                shutil.move(str(tmp_path), dest_path)
                results.append((up.name, category, tags))

        st.success(f"Organized {len(results)} file(s).")
        for name, cat, tags in results:
            st.write(f"• {name} → **{cat}** — tags: {tags}")

st.markdown("---")

# --- Dashboard ---
st.subheader("Organized folders")
cols = st.columns([2, 3])
folder_map = {}
for root, dirs, files in os.walk(ORG):
    rel = Path(root).relative_to(ORG)
    if str(rel) == ".":
        continue
    folder_map[str(rel)] = files

with cols[0]:
    st.write("Folders")
    folder_selected = st.selectbox("Choose a folder", options=sorted(folder_map.keys()) or ["(no files)"])
    if folder_selected and folder_selected != "(no files)":
        st.write(f"Files in {folder_selected}: {len(folder_map.get(folder_selected, []))}")

with cols[1]:
    if folder_map and folder_selected and folder_selected != "(no files)":
        files = folder_map.get(folder_selected, [])
        for fname in files:
            c1, c2, c3, c4 = st.columns([3,1,1,1])
            c1.write(fname)
            file_path = ORG / folder_selected / fname

            # Save to Desktop inside category folder
            if c2.button("Save to Desktop", key=f"local_{folder_selected}_{fname}"):
                local_dir = Path.home() / "Desktop" / folder_selected
                local_dir.mkdir(parents=True, exist_ok=True)
                local_path = local_dir / fname
                shutil.copy(file_path, local_path)
                st.success(f"Saved {fname} to {local_dir}")

            # Delete button
            if c3.button("Delete", key=f"del_{folder_selected}_{fname}"):
                try:
                    os.remove(file_path)
                    st.session_state.deleted_file = fname
                    st.success(f"Deleted {fname} locally.")
                except FileNotFoundError:
                    st.warning("File already deleted.")

            # S3 upload
            if use_s3 and c4.button("Send to S3", key=f"s3_{folder_selected}_{fname}"):
                try:
                    s3 = get_s3_client()
                    if not s3:
                        st.error("S3 client not configured properly. Enter your own credentials above.")
                    else:
                        s3.upload_file(str(file_path), s3_bucket, f"{folder_selected}/{fname}")
                        st.success(f"Uploaded {fname} to s3://{s3_bucket}/{folder_selected}/{fname}")
                except ClientError as e:
                    st.error("S3 upload failed: " + str(e))

# --- Trigger UI refresh after deletion ---
if st.session_state.deleted_file:
    st.session_state.deleted_file = None
    # Folder view updates automatically; no experimental_rerun needed

st.markdown("---")
st.markdown(
    """
    🧠 **How it works – The AI Magic Behind Your Files**  

    1️⃣ Upload your files – documents, spreadsheets, presentations, images, anything!  
    2️⃣ Our smart AI scans and classifies them into neat folders automatically:  
       - 📊 Financial  
       - 🖼️ Photos  
       - 📝 Work & Notes  
       - 🍳 Food & Recipes  
       - ✈️ Travel  
       - …and more!  
    3️⃣ Manage your files effortlessly:  
       - 💾 **Download** files instantly  
       - 🖥️ **Save to Desktop** in organized folders  
       - 🗑️ **Delete** with one click  
       - ☁️ **Upload to your own S3 bucket** securely  

    ⚡ **No more clutter, no more stress – just smart, organized storage!**
    """
)
