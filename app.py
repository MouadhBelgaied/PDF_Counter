import streamlit as st
import os
import gdown
import boto3
import webbrowser

st.title("PDF File Counter and S3 Uploader")

def count_pdf_files(dir_path):
    count = 0
    for filename in os.listdir(dir_path):
        if filename.lower().endswith(".pdf"):
            count += 1
    return count

def upload_to_s3(Bucket_name,aws_access_key_id,aws_secret_access_key,file_path,file_name):
    s3_client = boto3.client('s3', 
                      aws_access_key_id= aws_access_key_id, 
                      aws_secret_access_key= aws_secret_access_key)
    s3_client.upload_file(file_path, Bucket_name, file_name)

# Create two tabs
tabs = st.tabs(["PDF File Counter", "S3 Uploader"])

# PDF File Counter Tab
with tabs[0]:
    if st.button("Open Drive"):
        webbrowser.open_new_tab("https://drive.google.com")

    gdrive_dir_link = st.text_input("Enter the Google Drive Directory Link:")

    if st.button("Count"):
        if gdrive_dir_link:
            # Create a temporary directory to store the Google Drive directory
            temp_dir = "./temp_dir"
            os.makedirs(temp_dir, exist_ok=True)

            # Download the Google Drive directory to the temporary directory 
            # The Google Drive directory must have the required permissions
            gdown.download_folder(url= gdrive_dir_link,output= temp_dir)

            # Count PDF files in the downloaded directory
            pdf_count = count_pdf_files(temp_dir)

            # Write the count in a text file
            result = f"Number of PDF files in the given directory: {pdf_count}"
            with open(os.path.join(temp_dir, "result.txt"), "w") as f:
                f.write(result)

            # Display the count in the text box
            st.success(f"Number of PDF files: {pdf_count}")

# S3 Uploader Tab
with tabs[1]:
    if st.button("Open AWS"):
        webbrowser.open_new_tab("https://aws.amazon.com/")

    s3_bucket_name = st.text_input("Enter your S3 Bucket name:")
    aws_access_key_id= st.text_input("Enter your access key id:")
    aws_secret_access_key= st.text_input("Enter your secret access key:")

    if st.button("Upload"):
        if s3_bucket_name and aws_access_key_id and aws_secret_access_key and result:    
            # Upload the result to the specified S3 bucket
            upload_to_s3(s3_bucket_name,aws_access_key_id,aws_secret_access_key,os.path.join(temp_dir, "result.txt"),"result.txt")

            # Cleanup
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)

            st.success("Uploaded!")
