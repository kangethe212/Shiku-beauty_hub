# 🔄 MIGRATIONS GUIDE - Professional Features

## ⚠️ IMPORTANT: Run These Commands

After adding all the professional features, you MUST run migrations to create the new database tables.

---

## 🚀 STEP-BY-STEP MIGRATION

### Step 1: Create Migrations

```bash
python manage.py makemigrations beautyhub
```

**What This Does**:
Creates migration files for the 6 new models:
- Video
- DailyOffer
- Currency  
- ProductReview
- SocialMediaLink
- BusinessInfo

Plus updates to the Product model.

**Expected Output**:
```
Migrations for 'beautyhub':
  beautyhub/migrations/0002_auto_XXXXXX.py
    - Create model Video
    - Create model DailyOffer
    - Create model Currency
    - Create model ProductReview
    - Create model SocialMediaLink
    - Create model BusinessInfo
    - Add field price_usd to product
    - Add field price_eur to product
    - Add field price_gbp to product
    - Add field stock_quantity to product
    ... (more fields)
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

**What This Does**:
Creates all the new database tables and adds new columns to existing tables.

**Expected Output**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, beautyhub
Running migrations:
  Applying beautyhub.0002_auto_XXXXXX... OK
```

### Step 3: Create Media Folders

```bash
# Windows
mkdir media\videos
mkdir media\video_thumbnails
mkdir media\offers

# Mac/Linux
mkdir -p media/videos
mkdir -p media/video_thumbnails
mkdir -p media/offers
```

### Step 4: Verify Everything

```bash
# Run server
python manage.py runserver

# Visit admin panel
# http://127.0.0.1:8000/admin/
```

---

## ✅ VERIFICATION CHECKLIST

In the admin panel, you should now see:

- [ ] **Videos** section
- [ ] **Daily Offers** section
- [ ] **Currencies** section
- [ ] **Product Reviews** section
- [ ] **Social Media Links** section
- [ ] **Business Information** section
- [ ] Enhanced Products with new fields

---

## 🎯 INITIAL DATA SETUP

### 1. Add Currencies

```bash
# In Django admin or shell
```

**Recommended Currencies**:
- **USD** (US Dollar) - $
- **EUR** (Euro) - €
- **GBP** (British Pound) - £
- **NGN** (Nigerian Naira) - ₦ (or your local currency)

**Example**:
- Code: USD
- Name: US Dollar
- Symbol: $
- Exchange Rate: 1.0000
- Is Base: Yes
- Active: Yes

### 2. Update Business Information

Go to Admin → Business Information

**Required Fields**:
- Business Name: Her Beauty Hub
- Tagline: Glow. Style. Confidence.
- Phone: (your phone)
- Email: (your email)
- Address: (your address)
- WhatsApp: (with country code)
- Business Hours
- About, Mission, Vision

### 3. Add Social Media Links

Go to Admin → Social Media Links

**Add**:
- Instagram (your profile URL)
- TikTok (your profile URL)
- YouTube (your channel URL)
- WhatsApp (your WhatsApp link)
- Facebook (optional)
- Pinterest (optional)

---

## 🐛 TROUBLESHOOTING

### Issue: "No migrations to apply"

**Solution**: You might already be migrated. Run:
```bash
python manage.py showmigrations beautyhub
```

Look for:
```
[X] 0001_initial
[X] 0002_auto_XXXXXX
```

If missing, run migrations again.

---

### Issue: "Relation does not exist"

**Cause**: Migrations not applied

**Solution**:
```bash
python manage.py migrate --run-syncdb
```

---

### Issue: "Column already exists"

**Cause**: Partial migration

**Solution**:
```bash
# Reset migrations (CAUTION: Development only!)
python manage.py migrate beautyhub zero
python manage.py migrate beautyhub
```

---

### Issue: "Duplicate key value"

**Cause**: Trying to create duplicate entries

**Solution**: Check BusinessInfo - only ONE instance allowed

---

## 🔄 MIGRATION FILES

After running migrations, you'll have:

```
beautyhub/
├── migrations/
│   ├── __init__.py
│   ├── 0001_initial.py (original models)
│   └── 0002_auto_XXXXXX.py (NEW: professional features)
```

---

## 📊 DATABASE CHANGES

### New Tables Created:

1. `beautyhub_video`
2. `beautyhub_dailyoffer`
3. `beautyhub_currency`
4. `beautyhub_productreview`
5. `beautyhub_socialmedialink`
6. `beautyhub_businessinfo`

### Updated Tables:

1. `beautyhub_product` - Added fields:
   - price_usd
   - price_eur
   - price_gbp
   - stock_quantity
   - low_stock_threshold
   - sku
   - weight

---

## 🎯 POST-MIGRATION CHECKLIST

- [ ] Migrations applied successfully
- [ ] Media folders created
- [ ] Admin shows new sections
- [ ] Can add videos
- [ ] Can create offers
- [ ] Can add currencies
- [ ] Business info accessible
- [ ] Social links work
- [ ] Products show new fields

---

## 💾 BACKUP BEFORE MIGRATION (Recommended)

```bash
# Backup database
python manage.py dumpdata > backup_before_pro_features.json

# If needed, restore:
python manage.py loaddata backup_before_pro_features.json
```

---

## 🚀 READY TO GO!

After successful migration, you can:

✅ Upload videos
✅ Create special offers
✅ Add international pricing
✅ Track inventory
✅ Manage reviews
✅ Update business info
✅ Add social links

**Everything is ready for professional use! 🎉**

---

## 📝 QUICK REFERENCE

### Create Migrations:
```bash
python manage.py makemigrations beautyhub
```

### Apply Migrations:
```bash
python manage.py migrate
```

### Check Migration Status:
```bash
python manage.py showmigrations
```

### Create Media Folders:
```bash
mkdir media\videos media\video_thumbnails media\offers
```

### Run Server:
```bash
python manage.py runserver
```

---

**Need Help?** See BACKEND_SETUP.md or PROFESSIONAL_UPGRADE_COMPLETE.md

**Ready to Launch! 🚀✨**

