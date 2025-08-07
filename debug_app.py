import streamlit as st

st.set_page_config(page_title="Debug - Wildfire Analysis", layout="wide")

st.title("🔍 Debug: Secrets Check")

# Debug section
st.header("Debug Information")

# Check if secrets are available
st.write("### 1. Checking if st.secrets exists:")
try:
    st.write(f"st.secrets type: {type(st.secrets)}")
    st.write(f"st.secrets content: {st.secrets}")
    st.success("✅ st.secrets is available")
except Exception as e:
    st.error(f"❌ Error accessing st.secrets: {e}")

# Check individual keys
st.write("### 2. Checking individual secret keys:")

keys_to_check = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY", 
    "AWS_DEFAULT_REGION",
    "S3_BUCKET_NAME",
    "S3_OBJECT_KEY"
]

for key in keys_to_check:
    try:
        if key in st.secrets:
            st.success(f"✅ {key}: Found")
            # Don't show the actual value for security
            st.write(f"   Value: {'*' * len(str(st.secrets[key]))}")
        else:
            st.error(f"❌ {key}: Not found")
    except Exception as e:
        st.error(f"❌ {key}: Error checking - {e}")

# Show all available keys
st.write("### 3. All available secret keys:")
try:
    if hasattr(st.secrets, '_to_dict'):
        all_keys = list(st.secrets._to_dict().keys())
    else:
        all_keys = list(st.secrets.keys())
    st.write(f"Available keys: {all_keys}")
except Exception as e:
    st.error(f"Error listing keys: {e}")

# Test data loading
st.write("### 4. Testing data loading:")
try:
    import boto3
    import geopandas as gpd
    from io import BytesIO
    
    # Try to get secrets
    aws_access_key_id = st.secrets.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = st.secrets.get("AWS_SECRET_ACCESS_KEY")
    bucket_name = st.secrets.get("S3_BUCKET_NAME")
    file_path = st.secrets.get("S3_OBJECT_KEY")
    
    if all([aws_access_key_id, aws_secret_access_key, bucket_name, file_path]):
        st.success("✅ All required secrets are available")
        
        # Try to connect to S3
        try:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            st.success("✅ S3 client created successfully")
            
            # Try to get object info
            try:
                obj = s3.head_object(Bucket=bucket_name, Key=file_path)
                st.success(f"✅ File exists in S3: {obj['ContentLength']} bytes")
            except Exception as e:
                st.error(f"❌ Error accessing S3 file: {e}")
                
        except Exception as e:
            st.error(f"❌ Error creating S3 client: {e}")
    else:
        st.error("❌ Missing required secrets")
        st.write(f"AWS_ACCESS_KEY_ID: {'✅' if aws_access_key_id else '❌'}")
        st.write(f"AWS_SECRET_ACCESS_KEY: {'✅' if aws_secret_access_key else '❌'}")
        st.write(f"S3_BUCKET_NAME: {'✅' if bucket_name else '❌'}")
        st.write(f"S3_OBJECT_KEY: {'✅' if file_path else '❌'}")
        
except Exception as e:
    st.error(f"❌ Error in data loading test: {e}")

st.write("---")
st.write("### Instructions:")
st.write("1. If you see 'Not found' for any keys, add them to Streamlit Cloud secrets")
st.write("2. If S3 connection fails, check your AWS credentials")
st.write("3. If file access fails, check your S3 bucket and file path") 