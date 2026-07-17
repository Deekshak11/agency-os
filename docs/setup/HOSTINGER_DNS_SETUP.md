# Hostinger DNS Records - What to Add for Mailgun

## ✅ Keep Existing Records (Don't Touch!)

**Main domain (@) records stay as-is:**
- MX @ → SMTP.GOOGLE.COM (priority 1) ✅
- TXT @ → "v=spf1 include:_spf.google.com ~all" ✅
- TXT google._domainkey → (your Google DKIM) ✅

**Why?** Your main email (ava@getaevylabs.com) uses Google Workspace. Keep it separate!

---

## ➕ Add These 4 New Records for Mailgun

Copy-paste these into Hostinger DNS management:

### 1. DKIM Record (TXT)
```
Type: TXT
Name: krs._domainkey.replies
Content: k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDhco8RY0stTJmqCAM3W+zx5nVG7vUuiTM+ArqJif0/iyl7/fZoMoB4LnlbUmt8fvcCQTrmnzga2977af2XKgiSqtBclEtp74dIxWapCltAyf7mxiOiNCePdakST/950QxIrBVr/qgLaWiiJYrCeXn9rEGhad/85PEJGpUhccfUjwIDAQAB
TTL: 3600
```

### 2. SPF Record (TXT)
```
Type: TXT
Name: replies
Content: v=spf1 include:mailgun.org ~all
TTL: 3600
```

### 3. MX Record #1
```
Type: MX
Name: replies
Content: mxa.mailgun.org
Priority: 10
TTL: 3600
```

### 4. MX Record #2
```
Type: MX
Name: replies
Content: mxb.mailgun.org
Priority: 10
TTL: 3600
```

---

## 🎯 Why This Setup Works

**Subdomain Strategy** (YouTuber best practice):
- Main domain: `getaevylabs.com` → Google Workspace (protected)
- Reply subdomain: `replies.getaevylabs.com` → Mailgun webhooks
- **Benefit**: If Mailgun gets spam complaints, main domain reputation stays clean

**What Happens:**
1. You send email from `ava@getaevylabs.com` (Google)
2. Reply-To header: `test@replies.getaevylabs.com` (Mailgun)
3. Prospect replies → Mailgun receives → Instant webhook → Modal → Fulfillment

---

## ⏱️ Next Steps

1. **Add records** in Hostinger (copy-paste the 4 records above)
2. **Wait 10-15 minutes** for DNS propagation
3. **Verify in Mailgun**: Click "Verify DNS Settings"
4. **Should show**: ✅ All records verified

Then we create the Route and test!
