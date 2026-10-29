
import os
import base64
import streamlit as st
import fal_client

st.set_page_config(
    page_title="مولد الفيديوهات بالذكاء الاصطناعي",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    direction: rtl;
    text-align: right;
}
h1 {
    text-align: center;
    color: #4A90E2;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 تحويل الصور إلى فيديو")
st.write("ارفع صورة واكتب وصف الحركة التي تريدها.")

api_key = st.text_input(
    "مفتاح Fal.ai API",
    type="password"
).strip()

uploaded_file = st.file_uploader(
    "اختر صورة",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file, caption="الصورة الأصلية", width=300)

prompt = st.text_area(
    "وصف الفيديو بالإنجليزية",
    placeholder="Describe the motion you want..."
)

model = st.selectbox(
    "نموذج توليد الفيديو",
    ["fal-ai/luma-dream-machine"]
)

if st.button("🚀 ابدأ توليد الفيديو", type="primary"):

    if not api_key:
        st.warning("أدخل مفتاح API أولاً.")

    elif not prompt.strip():
        st.warning("اكتب وصف الفيديو أولاً.")

    elif uploaded_file is None:
        st.warning("ارفع صورة أولاً.")

    else:
        os.environ["FAL_KEY"] = api_key

        try:
            file_data = uploaded_file.getvalue()
            mime_type = uploaded_file.type

            encoded = base64.b64encode(
                file_data
            ).decode("utf-8")

            image_url = (
                f"data:{mime_type};base64,{encoded}"
            )

            arguments = {
                "prompt": prompt.strip(),
                "image_url": image_url
            }

            with st.spinner("جارٍ إرسال طلب توليد الفيديو..."):
                result = fal_client.subscribe(
                    model,
                    arguments=arguments
                )

            video = result.get("video", {})
            video_url = (
                video.get("url")
                if isinstance(video, dict)
                else None
            )

            if video_url:
                st.success("تم توليد الفيديو!")
                st.video(video_url)
                st.markdown(
                    f"[📥 فتح الفيديو]({video_url})"
                )
            else:
                st.error(
                    "لم يُعثر على رابط الفيديو في النتيجة."
                )
                st.json(result)

        except Exception as e:
            error = str(e)

            st.error("تعذر إنشاء الفيديو.")
            st.code(error[:2000])

            if "403" in error or "Forbidden" in error:
                st.warning(
                    "الخادم رفض الطلب. قد تكون المشكلة "
                    "في صلاحيات الحساب أو التخزين أو النموذج."
                )

            elif "401" in error or "Unauthorized" in error:
                st.warning(
                    "تعذرت المصادقة. تحقق من مفتاح API."
                )


