import streamlit as st

st.title("Secrets Debug Test")

# Try to access secrets
try:
    st.write("### Available secrets:")
    st.write(st.secrets)
    
    st.write("### Testing individual keys:")
    
    if "AWS_ACCESS_KEY_ID" in st.secrets:
        st.success("✅ AWS_ACCESS_KEY_ID found")
    else:
        st.error("❌ AWS_ACCESS_KEY_ID not found")
        
    if "S3_BUCKET_NAME" in st.secrets:
        st.success("✅ S3_BUCKET_NAME found")
    else:
        st.error("❌ S3_BUCKET_NAME not found")
        
    if "S3_OBJECT_KEY" in st.secrets:
        st.success("✅ S3_OBJECT_KEY found")
    else:
        st.error("❌ S3_OBJECT_KEY not found")
        
except Exception as e:
    st.error(f"Error accessing secrets: {e}") 