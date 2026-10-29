import streamlit as st
import fal_client
import os

# إعدادات الصفحة الأساسية للتطبيق
st.set_page_config(page_title="مُولد الفيديوهات بالذكاء الاصطناعي", page_icon="🎬", layout="centered")

# تغيير اتجاه الصفحة للعربية (من اليمين إلى اليسار) وعنوان جذاب
st.markdown("""
    <style>
    .reportview-container .main .block-container { direction: RTL; text-align: right; }
    h1 { text-align: center; color: #4A90E2; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 تحويل الصور والنصوص إلى فيديو")
st.write("ارفع صورتك واكتب الوصف (البرومت) لتحويلها إلى فيديو رائع خلال ثوانٍ معدودة!")

# صندوق إدخال الـ API Key الخاص بالمستخدم لحماية خصوصيتك
api_key = st.text_input("أدخل مفتاح Fal.ai API الخاص بك أولاً:", type="password")

if api_key:
    # تفعيل المفتاح في خلفية النظام
    os.environ["FAL_KEY"] = api_key

    # نموذج رفع الصورة
    uploaded_file = st.file_uploader("اختر صورة للبدء (اختياري):", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="الصورة المرفوعة", width=300)

    # صندوق كتابة البرومت (النص الوصفي)
    prompt = st.text_area("اكتب الوصف (مثال: طائر يطير في الغابة وقت الغروب، حركة واقعية سينمائية):")

    # زر توليد الفيديو
    if st.button("🚀 ابدأ توليد الفيديو الآن"):
        if not prompt:
            st.warning("الرجاء كتابة وصف (برومت) للفيديو أولاً!")
        else:
            with st.spinner("⏳ جارٍ توليد الفيديو على السيرفرات السحابية... قد يستغرق الأمر دقيقة."):
                try:
                    # رفع الصورة مؤقتاً لسيرفر fal إذا كانت موجودة
                    image_url = None
                    if uploaded_file:
                        image_url = fal_client.upload_file(uploaded_file)

                    # إعداد المدخلات لنموذج لونا (Luma Dream Machine) القوي بالفيديو
                    arguments = {
                        "prompt": prompt,
                    }
                    if image_url:
                        arguments["image_url"] = image_url

                    # إرسال الطلب للسيرفر وتوليد الفيديو
                    # نستخدم هنا نموذج Luma الشهير والمتوفر على fal
                    handler = fal_client.submit("fal-ai/luma-dream-machine", arguments=arguments)
                    result = handler.get()

                    # استخراج رابط الفيديو الناتج
                    video_url = result['video']['url']

                    # عرض الفيديو بنجاح للمستخدم
                    st.success("🎉 تم توليد الفيديو بنجاح!")
                    st.video(video_url)
                    st.markdown(f"[📥 اضغط هنا لتحميل الفيديو مباشرة]({video_url})")

                except Exception as e:
                    st.error(f"عذراً، حدث خطأ أثناء التوليد: {str(e)}")
else:
    st.info("الرجاء إدخال الـ API Key في الصندوق أعلاه لتتمكن من استخدام التطبيق.")
