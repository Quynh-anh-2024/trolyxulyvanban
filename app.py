import streamlit as st
import google.generativeai as genai
import docx
from io import BytesIO

# 1. Cấu hình trang web
st.set_page_config(page_title="Trợ lý Văn bản Giàng Chu Phìn", page_icon="📝")

# 2. Cấu hình API Gemini (Lấy từ biến môi trường hoặc nhập tay)
api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Bản này chạy ổn định nhất

    st.title("📄 Trợ Lý Soát Lỗi & Chuẩn Hóa AI")
    st.info("Ứng dụng dành riêng cho GV Trường PTDTBT Tiểu học Giàng Chu Phìn")

    # 3. Thành phần tải file
    uploaded_file = st.file_input("Tải lên file Word (.docx)", type="docx")

    if uploaded_file:
        # Đọc nội dung file Word
        doc = docx.Document(uploaded_file)
        full_text = [para.text for para in doc.paragraphs]
        content = "\n".join(full_text)

        st.subheader("Nội dung văn bản:")
        st.text_area("", content, height=200)

        # 4. Lựa chọn chế độ xử lý
        option = st.selectbox("Chọn chế độ xử lý:", 
            ["Soát lỗi chính tả & văn phong", "Tóm tắt văn bản", "Tạo 5 câu trắc nghiệm"])

        if st.button("Bắt đầu xử lý với AI"):
            with st.spinner("AI đang suy nghĩ..."):
                try:
                    # Tạo prompt dựa trên lựa chọn
                    prompt = f"Hãy {option} cho đoạn văn bản sau đây một cách chuyên nghiệp: \n\n {content}"
                    response = model.generate_content(prompt)
                    
                    st.subheader("Kết quả từ AI:")
                    st.write(response.text)
                    
                    # 5. Cho phép tải kết quả về (Dạng text đơn giản)
                    st.download_button("Tải kết quả về máy", response.text)
                except Exception as e:
                    st.error(f"Lỗi: {e}")
else:
    st.warning("Vui lòng nhập API Key ở thanh bên trái để bắt đầu.")