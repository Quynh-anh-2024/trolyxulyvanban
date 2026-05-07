import streamlit as st
import google.generativeai as genai
import docx
import os

# Lấy API Key từ Environment Variables của Vercel
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("📄 Trợ Lý Văn Bản Giàng Chu Phìn")
    
    uploaded_file = st.file_uploader("Tải lên file Word (.docx)", type="docx")

    if uploaded_file:
        doc = docx.Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])
        
        option = st.selectbox("Chế độ:", ["Soát lỗi", "Tóm tắt", "Tạo trắc nghiệm"])
        
        if st.button("Bắt đầu"):
            with st.spinner("Đang xử lý..."):
                prompt = f"Hãy {option}: \n\n {content}"
                response = model.generate_content(prompt)
                st.write(response.text)
else:
    st.error("Chưa cấu hình API Key trên Vercel!")
