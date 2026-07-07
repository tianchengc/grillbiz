# Meta Graph API Setup & Token Renewal Guide

Use this guide to set up automatic Instagram posting via the Meta Graph API and manage access tokens.

---

## Part 1: Initial Facebook & Instagram Connection Setup

### 1. Convert Instagram to a Professional Business Account
You must have an Instagram Business or Creator account to use the Graph API.
1. In the Instagram Mobile App, go to your **Profile**.
2. Tap the menu icon (**☰**) -> **Settings and privacy**.
3. Tap **Account type and tools** (or **Professional tools**).
4. Tap **Switch to professional account** and select **Business**.

### 2. Connect Instagram to a Facebook Page
Meta requires a Facebook Page to act as the administrative bridge to the API.
1. Create a Facebook Page for your brand/project.
2. Link the accounts from your **Instagram Profile** -> **Edit profile** -> **Page** (select your Facebook Page).
3. Confirm the link from your **Facebook Page Settings** -> **Linked Accounts** -> **Instagram** (ensure your account displays as connected).

### 3. Register a Meta Developer Application
1. Go to the [Meta for Developers Portal](https://developers.facebook.com/apps/).
2. Click **Create App** and choose **Business** as the app type (this links it to Meta Business Suite).
3. Add the **Instagram Graph API** product to your app dashboard.
4. In the app dashboard, navigate to **Roles** -> **Roles** and ensure your Facebook account is designated as an **Administrator** or **Developer**.

---

## Part 2: Generating Scopes & Long-Lived Access Tokens

To publish content, you need an access token with these permissions:
* `instagram_basic`
* `instagram_content_publish`
* `pages_show_list`

### Step 1: Generate a Short-Lived Token (Explorer)
1. Go to the [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. Select your newly created **Meta App** in the top-right dropdown.
3. Under **User or Page**, select **Get Token** -> **Get User Access Token**.
4. Check the boxes for the required scopes:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_show_list`
5. Click **Generate Access Token** and complete the Facebook login prompt.
6. Copy the generated string. This is your **Short-Lived User Access Token** (expires in 1-2 hours).

### Step 2: Convert to a Long-Lived Access Token (60-Day Expiry)
1. Navigate to the [Meta Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/).
2. Paste the short-lived token into the text field and click **Debug**.
3. Scroll to the bottom of the details page and click **Extend Access Token**.
4. Re-enter your password if prompted.
5. **Result:** Copy the newly generated **Long-Lived Access Token** (expires in 60 days). Save this token and your Instagram Account ID into your project's `.env` file.

---

## Part 3: Configuration Variables
Save the credentials to the **`.env`** file at the root of your project workspace:

```env
# Instagram API Credentials
IG_ACCESS_TOKEN=your_long_lived_access_token_here
IG_ACCOUNT_ID=your_numeric_instagram_account_id_here
```
