# بوت الكابشن والهاشتاقات

بوت تلغرام يقدم كابشن + هاشتاقات، سواء صيفطتي صورة أو كتبتي كلمة/موضوع.
اللغة (فرنسية / إنجليزية / دارجة-عربية) تختارها من داخل البوت بـ /start.

## 1) شحال باغي: مفتاحين مجانيين

### أ) توكن ديال Telegram Bot
1. حل تلغرام، دور على **@BotFather**
2. كتب `/newbot` وتبع التعليمات (سمي البوت وعطيه username ينتهي بـ `bot`)
3. غايعطيك توكن، بحال هذا: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`

### ب) مفتاح Gemini API (مجاني)
1. سير لـ https://aistudio.google.com/app/apikey
2. دخل بحساب Google، اضغط "Create API Key"
3. كوبي المفتاح

## 2) تجربة محلية (اختياري، قبل الرفع للسيرفر)

```bash
pip install -r requirements.txt
export TELEGRAM_TOKEN="التوكن ديالك"
export GEMINI_API_KEY="مفتاح Gemini ديالك"
python main.py
```

## 3) الرفع لـ Railway باش يخدم 24/7 حتى ويطفى الحاسوب

1. سير لـ https://railway.app وسجل بحساب GitHub
2. دير حساب GitHub جديد فيه هاد المجلد (`caption_bot`) — أو ارفعو مباشرة بـ Railway CLI
3. فـ Railway: **New Project → Deploy from GitHub repo** → اختار الريبو
4. فقسم **Variables** زيد:
   - `TELEGRAM_TOKEN` = التوكن ديالك
   - `GEMINI_API_KEY` = مفتاح Gemini ديالك
5. Railway غادي يقرا `Procfile` ويشغل البوت كـ worker تلقائيًا
6. Free tier ديال Railway عندها ساعات محدودة فالشهر — إلا خلصتها، بدل لـ **Render.com** (نفس الخطوات تقريبًا، اختار "Background Worker")

## ملاحظات

- اللغة كتبقى محفوظة فالذاكرة ديال البوت طول ما هو خدام. إلا عاود تشغيل البوت (redeploy)، كل واحد لازم يعاود `/start` باش يختار اللغة مرة أخرى. إلا بغيتي تبقى محفوظة نهائيًا حتى بعد redeploy، نقدر نزيدو قاعدة بيانات صغيرة (SQLite) من بعد.
- Gemini free tier فيه حد ديال الطلبات فالدقيقة/اليوم — كافي بزاف لبوت شخصي، ملي يكبر الاستخدام نقدر نبدلو بخطة مدفوعة أو نديرو rate limiting.
