import streamlit as st
import google.generativeai as genai
import docx
import os

# Lấy API Key từ mục Environment Variables của Vercel
api_key = os.environ.get("GEMINI_API_KEY")

def run_app():
    st.title("📄 Trợ Lý Văn Bản Giàng Chu Phìn")
    st.info("Ứng dụng hỗ trợ giáo viên soạn thảo và soát lỗi")

    if not api_key:
        st.error("Lỗi: Chưa tìm thấy API Key. Hãy cấu hình GEMINI_API_KEY trong phần Environment Variables trên Vercel.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    uploaded_file = st.file_uploader("Tải lên file Word (.docx)", type="docx")

    if uploaded_file:
        try:
            doc = docx.Document(uploaded_file)
            full_text = [para.text for para in doc.paragraphs]
            content = "\n".join(full_text)
            
            st.subheader("Nội dung văn bản:")
            st.text_area("", content, height=200)

            option = st.selectbox("Chọn chế độ xử lý:", 
                ["Soát lỗi chính tả & văn phong", "Tóm tắt nội dung chính", "Tạo câu hỏi ôn tập"])

            if st.button("Bắt đầu xử lý"):
                with st.spinner("AI đang làm việc..."):
                    prompt = f"Với vai trò là một trợ lý giáo dục, hãy {option} cho văn bản sau: \n\n {content}"
                    response = model.generate_content(prompt)
                    st.subheader("Kết quả:")
                    st.write(response.text)
        except Exception as e:
            st.error(f"Có lỗi xảy ra khi đọc file: {e}")

if __name__ == "__main__":
    run_app()
