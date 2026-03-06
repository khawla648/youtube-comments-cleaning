import pandas as pd
import re
from langdetect import detect, DetectorFactory

# تثبيت نفس نتيجة كشف اللغة
DetectorFactory.seed = 0

# 1️⃣ قراءة dataset
df = pd.read_csv("all_comments.csv")

# التأكد أن العمود نصي
df["Comment"] = df["Comment"].astype(str)

# 2️⃣ حذف الروابط
url_pattern = r'http\S+|www\S+|https\S+'
df["no_url_comment"] = df["Comment"].apply(lambda x: re.sub(url_pattern, '', x))

# 3️⃣ استخراج الايموجي
emoji_pattern = re.compile(
"["
"\U0001F600-\U0001F64F"
"\U0001F300-\U0001F5FF"
"\U0001F680-\U0001F6FF"
"\U0001F1E0-\U0001F1FF"
"]+", flags=re.UNICODE)

df["emojis"] = df["no_url_comment"].apply(lambda x: " ".join(emoji_pattern.findall(x)))

# 4️⃣ حذف الايموجي من التعليق
df["clean_comment"] = df["no_url_comment"].apply(lambda x: emoji_pattern.sub('', x))

# 5️⃣ كشف اللغة
def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

df["language"] = df["clean_comment"].apply(detect_language)

# 7️⃣ حفظ dataset جديد
df.to_csv("cleaned_comments.csv", index=False)

print("Cleaning finished successfully")
