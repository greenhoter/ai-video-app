
import os
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
st.write("ارفع صورة، واكتب وصف الحركة التي تريدها.")

api_key = st.text_input(
    "أدخل مفتاح Fal.ai API:",
    type="password"
).strip()

uploaded_file = st.file_uploader(
    "اختر صورة (اختياري)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(uploaded_file, caption="الصورة الأصلية", width=300)

prompt = st.text_area(
    "اكتب وصف الفيديو بالإنجليزية:",
    placeholder="Describe the motion you want..."
)

if st.button("🚀 ابدأ توليد الفيديو", type="primary"):

    if not api_key:
        st.warning("أدخل مفتاح API صالحاً أولاً.")

    elif not prompt.strip():
        st.warning("اكتب وصف الفيديو أولاً.")

    else:
        try:
            # تعيين المفتاح قبل الاتصال بخدمة Fal.ai
            os.environ["FAL_KEY"] = api_key

            arguments = {
                "prompt": prompt.strip()
            }

            with st.spinner("جارٍ تجهيز الطلب..."):

                if uploaded_file is not None:
                    file_data = uploaded_file.getvalue()

                    image_url = fal_client.upload(
                        file_data,
                        uploaded_file.type,
                        file_name=uploaded_file.name
                    )

                    arguments["image_url"] = image_url

            with st.spinner(
                "جارٍ توليد الفيديو... قد يستغرق الأمر بعض الوقت."
            ):
                result = fal_client.subscribe(
                    "fal-ai/luma-dream-machine",
                    arguments=arguments
                )

            video_data = result.get("video", {})
            video_url = (
                video_data.get("url")
                if isinstance(video_data, dict)
                else None
            )

            if video_url:
                st.success("تم إنشاء الفيديو بنجاح!")
                st.video(video_url)
                st.markdown(
                    f"[📥 فتح الفيديو وتحميله]({video_url})"
                )
            else:
                st.error(
                    "انتهى الطلب، لكن لم يُعثر على رابط الفيديو "
                    "في النتيجة."
                )
                st.json(result)

        except Exception as e:
            error_text = str(e)
            st.error("تعذر إكمال عملية توليد الفيديو.")

            if "403" in error_text or "Forbidden" in error_text:
                st.warning(
                    "رفضت Fal.ai الطلب. تحقق من صلاحية مفتاح API "
                    "ومن إمكانية الوصول إلى خدمة رفع الملفات."
                )
            elif "401" in error_text or "Unauthorized" in error_text:
                st.warning(
                    "فشل التحقق من الهوية. تحقق من صحة مفتاح API."
                )
            else:
                st.code(error_text[:1500])

else:
    st.info("أدخل مفتاح API، ثم اكتب وصف الفيديو.")




