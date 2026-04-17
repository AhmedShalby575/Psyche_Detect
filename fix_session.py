import streamlit as st

# Clear all session state
for key in list(st.session_state.keys()):
    del st.session_state[key]

st.success("✅ تم مسح كل البيانات القديمة بنجاح!")
st.write("اغلق هذا التطبيق الآن، ثم شغل التطبيق الأصلي تاني")