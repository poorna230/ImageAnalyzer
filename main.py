import streamlit as st
import google.generativeai as genai
from PIL import Image, UnidentifiedImageError

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyDpuFnENGEafI_3XkrGMKPJ9Yp8m3FtktM")  # Replace with your actual key

# --- Extract text/content from image using Gemini ---
def extract_text_from_image(image_file):
    model = genai.GenerativeModel("gemini-1.5-flash")
    image_bytes = image_file.getvalue()

    try:
        response = model.generate_content([
            "Extract all visible content from this image (text, formulas, notes, etc.) as clearly as possible.",
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Validate the extracted content ---
def validate_information(extracted_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are an expert tutor.

Review the following extracted content from a handwritten image:

\"\"\"{extracted_text}\"\"\"

Your task:
- Identify any incorrect facts or formulas.
- Correct them.
- Explain the correct concept clearly as a tutor would to a student.

Use a friendly tone, and keep your explanations simple and clear.
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Let user ask follow-up questions ---
def answer_followup_question(image_text, question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
Based on this content extracted from an image:

\"\"\"{image_text}\"\"\"

Answer this follow-up question in a helpful, clear way:

\"{question}\"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="AI Tutor from Image 📸🧠", layout="centered")
st.title("📚 AI Tutor from Handwritten Images")
st.write("Upload an image with handwritten formulas, definitions, or notes. The AI will validate, correct, and teach you — just like a real tutor!")

# Upload section
uploaded_image = st.file_uploader("📤 Upload your handwritten or printed note image...", type=["jpg", "jpeg", "png"])

if uploaded_image:
    try:
        # Try to open the image and display it
        image = Image.open(uploaded_image)
        st.image(image, caption="🖼 Uploaded Image", use_container_width=True)

        with st.spinner("🧠 Extracting and understanding content..."):
            extracted = extract_text_from_image(uploaded_image)
            validation = validate_information(extracted)

        st.subheader("📝 Extracted Content:")
        st.code(extracted)

        st.subheader("✅ Validation & Tutor Explanation:")
        st.markdown(validation)

        # Follow-up question box
        st.subheader("💬 Ask a Follow-Up Question:")
        user_question = st.text_input("Type your question here (e.g., 'Why is the original formula wrong?')")

        if user_question:
            with st.spinner("🤔 Thinking..."):
                followup_response = answer_followup_question(extracted, user_question)
            st.markdown("🧠 Tutor Answer:")
            st.write(followup_response)

    except UnidentifiedImageError:
        st.error("❌ Unable to identify the image. Please upload a valid JPG, JPEG, or PNG file.")
    except Exception as e:
        st.error(f"❌ Error processing the image: {e}")