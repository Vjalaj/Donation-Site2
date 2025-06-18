<div align="center">

# 🌟 Seva Connect - Complete Donation Platform

### *Serving Humanity Through Compassionate Giving*

[![PHP](https://img.shields.io/badge/PHP-7.4+-777BB4?style=for-the-badge&logo=php&logoColor=white)](https://php.net)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-5.7+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Razorpay](https://img.shields.io/badge/Razorpay-Integration-528DD7?style=for-the-badge&logo=razorpay&logoColor=white)](https://razorpay.com)

**🚀 Modern • 🔐 Secure • 💳 Payment Ready • 📱 Mobile-First • 🆓 Free Setup**

</div>

---

## 📋 Table of Contents

- [✨ **Quick Demo**](#-quick-demo)
- [🎯 **Key Features**](#-key-features)
- [⚡ **5-Minute Setup**](#-5-minute-setup)
- [🔧 **Detailed Setup Guide**](#-detailed-setup-guide)
- [💳 **Payment Setup (Razorpay)**](#-payment-setup-razorpay)
- [🔐 **OAuth Setup (Google & Microsoft)**](#-oauth-setup-google--microsoft)
- [🐍 **Python Services**](#-python-services)
- [🛡️ **Security Features**](#️-security-features)
- [📱 **Usage Guide**](#-usage-guide)
- [🔧 **Troubleshooting**](#-troubleshooting)

---

## ✨ Quick Demo

<div align="center">

### 🌐 **Live Preview**
| **Main Website** | **Admin Dashboard** | **Certificate Sample** |
|:---:|:---:|:---:|
| ![Main Site](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZULgn7jR5IH6sCNm5PjEnH1xTaSLFJLmx8w&s) | ![Admin](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVwcuO5FziSGGWZfP4Kp8ClpqKiUdCyk7fOiykhrbcAehoYlBdZ15Azt3j8Puw2oecqfE&usqp=CAU) | ![Certificate](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDa_mxijI9v_pvjA10Icag3EtDC93yhbTEMA&s) |
| Modern donation interface | Professional admin panel | Automated certificate generation |

### 🎯 **What Makes This Special?**

</div>

> 🎨 **Modern Design** - Beautiful, responsive interface that works on all devices  
> 💳 **Real Payments** - Integrated Razorpay for secure online transactions  
> 📜 **Auto Certificates** - Python-generated membership certificates  
> 🔐 **Enterprise Security** - Google/Microsoft OAuth + encrypted credentials  
> 🚀 **One-Click Setup** - Complete platform running in under 5 minutes  

---

## 🎯 Key Features

<table>
<tr>
<td width="50%">

### 🌟 **Core Features**
- ✅ **8 Noble Causes** - Orphanage, Elderly Care, Healthcare, etc.
- ✅ **Membership System** - ₹1,111 membership with certificates
- ✅ **Modern Admin Panel** - Complete content management
- ✅ **Mobile Responsive** - Perfect on all screen sizes
- ✅ **Light/Dark Themes** - User preference support
- ✅ **Real-time Updates** - Live content synchronization

</td>
<td width="50%">

### 🚀 **Advanced Features**
- 🐍 **Python Backend** - Microservices architecture
- 💳 **Payment Gateway** - Razorpay integration
- 📜 **Certificate Generator** - Automated PDF/PNG certificates
- 🔐 **OAuth Login** - Google & Microsoft authentication
- 🛡️ **Enterprise Security** - Environment-based credentials
- 📊 **Analytics Dashboard** - Payment and user insights

</td>
</tr>
</table>

---

## ⚡ 5-Minute Setup

### 🎯 **For the Impatient** *(Basic Setup)*

```bash
# 1. Prerequisites (Install if not present)
# ✅ XAMPP (for PHP + MySQL)
# ✅ Python 3.8+

# 2. Quick Start
📁 Extract project to: j:\Seva Connect 2.O\
🖱️ Double-click: start_seva_connect.bat
🔍 Check setup: http://localhost:8000/setup.html
🌐 Open: http://localhost:8000
🔐 Admin: http://localhost:8000/admin (admin/admin123)
```

**🎉 Done! Basic platform is running. For payments & OAuth, continue to detailed setup below.**

---

## 🔧 Detailed Setup Guide

### 📦 **Step 1: Install Prerequisites**

<details>
<summary><b>🔽 Click to expand installation details</b></summary>

#### **XAMPP Installation**
1. **Download**: https://www.apachefriends.org/download.html
2. **Install** with default settings
3. **Start Services**: Open XAMPP Control Panel → Start Apache & MySQL

#### **Python Installation**
1. **Download**: https://www.python.org/downloads/
2. **Install**: ✅ Check "Add Python to PATH" during installation
3. **Verify**: Open Command Prompt → Type `python --version`

</details>

### 🗄️ **Step 2: Database Setup**

<details>
<summary><b>🔽 Click to expand database setup</b></summary>

1. **Open phpMyAdmin**: http://localhost/phpmyadmin
2. **Create Database**: 
   - Click "New" → Database name: `seva_connect`
3. **Import Schema**: 
   - Select database → Import tab → Choose `database/seva_connect.sql`
   - Click "Go"

**✅ Database created with sample data!**

</details>

### 📁 **Step 3: Project Setup**

```bash
# Extract project files
📂 Place in: j:\Seva Connect 2.O\

# Install Python dependencies
cd "j:\Seva Connect 2.O\python"
pip install -r requirements.txt

# Setup environment (copy and edit)
copy .env.example .env
# Edit .env with your credentials (see sections below)
```

### 🚀 **Step 4: Launch Platform**

```bash
# Option 1: Automatic (Windows)
🖱️ Double-click: start_seva_connect.bat

# Option 2: Manual
# Terminal 1: Start Python services
cd python
python start_services.py

# Terminal 2: Start PHP server
php -S 0.0.0.0:8000
```

**🌐 Access URLs:**
- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Default Login**: admin / admin123

---

## 💳 Payment Setup (Razorpay)

### 💰 **Free Testing + Live Payments**

<div align="center">

| **Test Mode** | **Live Mode** |
|:---:|:---:|
| 🆓 **Completely Free** | 💰 **2% + ₹2 per transaction** |
| ♾️ Unlimited test transactions | 💳 Real money processing |
| 🧪 Perfect for development | 🚀 Production ready |

</div>

### 📝 **Step-by-Step Razorpay Setup**

<details>
<summary><b>🔽 Click for complete Razorpay setup guide</b></summary>

#### **1. Create Razorpay Account**
```
🌐 Visit: https://dashboard.razorpay.com/
📧 Sign up with email
📱 Verify phone number
🏢 Add business details
```

#### **2. Get API Keys**
```
🔑 Go to: Settings → API Keys
📋 Generate Test Key ID & Secret
💾 Copy both keys (you'll need them)
```

#### **3. Configure in Project**
```bash
# Edit .env file
RAZORPAY_KEY_ID=rzp_test_your_key_here
RAZORPAY_KEY_SECRET=your_secret_here
```

#### **4. Test Payment Flow**
```
💳 Use test cards:
   Card: 4111 1111 1111 1111
   CVV: 123
   Expiry: Any future date
```

#### **5. Go Live (When Ready)**
```
🚀 Generate Live Keys
💰 Add bank account details
✅ Complete KYC verification
🔄 Replace test keys with live keys
```

</details>

### 🔧 **Quick Razorpay Configuration**

```env
# Add to your .env file
RAZORPAY_KEY_ID=rzp_test_1DP5mmOlF5G5ag
RAZORPAY_KEY_SECRET=thisissupersecret

# For testing, you can use these sample credentials
# Replace with your actual keys from Razorpay dashboard
```

---

## 🔐 OAuth Setup (Google & Microsoft)

### 🆓 **100% Free Authentication**

<div align="center">

| **Google OAuth** | **Microsoft OAuth** |
|:---:|:---:|
| ![Google](https://img.shields.io/badge/Google-4285F4?style=for-the-badge&logo=google&logoColor=white) | ![Microsoft](https://img.shields.io/badge/Microsoft-0078D4?style=for-the-badge&logo=microsoft&logoColor=white) |
| **Completely Free** | **Completely Free** |
| No limits, no costs | No limits, no costs |

</div>

### 🔵 **Google OAuth Setup**

<div align="center">
<a href="https://console.developers.google.com/" target="_blank">
<button style="background: #4285f4; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px;">
🚀 <strong>Open Google Cloud Console</strong>
</button>
</a>
</div>

<details>
<summary><b>🔽 Click for complete Google OAuth setup</b></summary>

#### **Step 1: Create Google Cloud Project**
```
🌐 Visit: https://console.developers.google.com/
🆕 Click "New Project"
📝 Project name: "Seva Connect Admin"
✅ Click "Create"
```

#### **Step 2: Enable APIs**
```
📚 Go to: APIs & Services → Library
🔍 Search: "Google+ API" or "Google Identity"
✅ Click "Enable"
```

#### **Step 3: Create OAuth Credentials**
```
🔑 Go to: APIs & Services → Credentials
➕ Click: "Create Credentials" → "OAuth 2.0 Client IDs"
🖥️ Application type: "Web application"
📝 Name: "Seva Connect Admin Auth"
```

#### **Step 4: Configure Redirect URLs**
```
🔗 Authorized redirect URIs:
   Add: http://localhost:8000/auth/callback/google
   Add: http://127.0.0.1:8000/auth/callback/google
💾 Click "Save"
```

#### **Step 5: Copy Credentials**
```
📋 Copy "Client ID" (ends with .googleusercontent.com)
📋 Copy "Client Secret"
📝 Add to your .env file
```

</details>

### 🔴 **Microsoft OAuth Setup**

<div align="center">
<a href="https://portal.azure.com/" target="_blank">
<button style="background: #0078d4; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 16px; cursor: pointer; text-decoration: none; display: inline-block; margin: 10px;">
🚀 <strong>Open Azure Portal</strong>
</button>
</a>
</div>

<details>
<summary><b>🔽 Click for complete Microsoft OAuth setup</b></summary>

#### **Step 1: Access Azure Portal**
```
🌐 Visit: https://portal.azure.com/
🔐 Sign in with Microsoft account
📱 (Create free account if needed)
```

#### **Step 2: Register Application**
```
🔍 Search: "Azure Active Directory"
📱 Go to: App registrations
➕ Click: "New registration"
📝 Name: "Seva Connect Admin"
👥 Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
```

#### **Step 3: Configure Redirect URI**
```
🔗 Redirect URI type: "Web"
📝 URL: http://localhost:8000/auth/callback/microsoft
✅ Click "Register"
```

#### **Step 4: Generate Client Secret**
```
🔑 Go to: Certificates & secrets
➕ Click: "New client secret"
📝 Description: "Seva Connect Secret"
⏰ Expires: 24 months
💾 Click "Add"
📋 Copy the secret VALUE (not ID)
```

#### **Step 5: Copy Application ID**
```
📋 Go to: Overview
📋 Copy "Application (client) ID"
📝 Add both to your .env file
```

</details>

### 🔧 **OAuth Configuration**

```env
# Add to your .env file

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_secret

# Microsoft OAuth  
MICROSOFT_CLIENT_ID=your_microsoft_app_id
MICROSOFT_CLIENT_SECRET=your_microsoft_secret
```

---

## 🐍 Python Services

### 🔄 **Microservices Architecture**

<div align="center">

| **Service** | **Port** | **Purpose** | **Status** |
|:---:|:---:|:---:|:---:|
| 📜 **Certificate API** | 5002 | Generate & download certificates | ✅ |
| 💳 **Payment API** | 5000 | Process Razorpay payments | ✅ |
| 🔐 **OAuth API** | 5001 | Handle Google/Microsoft auth | ✅ |

</div>

### 🚀 **Service Management**

```bash
# Start all services
cd python
python start_services.py

# Check service status
python start_services.py status

# Install dependencies
python start_services.py install
```

### 📊 **API Endpoints**

<details>
<summary><b>🔽 Click to see all API endpoints</b></summary>

#### **Certificate API (Port 5002)**
```
POST /generate-certificate     - Generate member certificate
GET  /download-certificate/<id> - Download certificate file
GET  /certificate-preview/<id>  - Preview certificate (base64)
POST /bulk-generate-certificates - Generate multiple certificates
GET  /certificate-stats        - Get generation statistics
```

#### **Payment API (Port 5000)**
```
POST /create-order             - Create Razorpay payment order
POST /verify-payment           - Verify payment signature
POST /refund-payment           - Process payment refund
GET  /payment-status/<id>      - Get payment status
POST /payment-webhook          - Handle Razorpay webhooks
```

#### **OAuth API (Port 5001)**
```
GET  /auth/google             - Initiate Google login
GET  /auth/microsoft          - Initiate Microsoft login
GET  /auth/callback/google    - Handle Google callback
GET  /auth/callback/microsoft - Handle Microsoft callback
POST /auth/verify             - Verify JWT token
POST /auth/logout             - Logout user
```

</details>

---

## 🛡️ Security Features

<div align="center">

### 🔐 **Enterprise-Grade Security**

| **Feature** | **Implementation** | **Status** |
|:---:|:---:|:---:|
| 🔒 **Password Hashing** | Bcrypt with salt | ✅ |
| 🎫 **Session Management** | JWT tokens + database sessions | ✅ |
| 🌍 **Environment Variables** | All secrets in .env file | ✅ |
| 🛡️ **SQL Injection Protection** | Prepared statements | ✅ |
| 🔐 **OAuth Integration** | Google & Microsoft auth | ✅ |
| 🚫 **CSRF Protection** | Token validation | ✅ |

</div>

### 🔑 **Default Admin Access**

```
🌐 URL: http://localhost:8000/admin
👤 Username: admin
🔐 Password: admin123

⚠️ IMPORTANT: Change password immediately after first login!
```

---

## 📱 Usage Guide

### 👥 **For Regular Users**

<details>
<summary><b>🔽 Click for user guide</b></summary>

#### **Making Donations**
1. 🌐 Visit main website
2. 🎯 Choose a cause
3. 💰 Enter donation amount
4. 📝 Fill donor details
5. 💳 Complete payment via Razorpay

#### **Becoming a Member**
1. 📝 Click "Become a Member"
2. 💰 Pay membership fee (₹1,111)
3. 📜 Receive digital certificate
4. 📧 Get membership confirmation

</details>

### 👨‍💼 **For Admins**

<details>
<summary><b>🔽 Click for admin guide</b></summary>

#### **Admin Panel Features**
- 📊 **Dashboard**: View statistics and recent activity
- 📝 **Content Management**: Edit about text and cause content
- 🖼️ **Photo Management**: Upload and organize images
- 💰 **Donations**: View and manage donation records
- 👥 **Members**: Manage membership data
- 📜 **Certificates**: Generate and download certificates
- ⚙️ **Settings**: Change password and admin preferences

#### **Content Updates**
1. 🔐 Login to admin panel
2. 📝 Go to "Manage Content"
3. ✏️ Edit cause-specific content
4. 💾 Save changes (updates immediately on website)

#### **Certificate Management**
1. 👥 Go to "Members" section
2. 📜 Click "Generate Certificate" for any member
3. 🎨 Choose light or dark theme
4. 💾 Download or preview certificate

</details>

---

## 🔧 Troubleshooting

### ❗ **Common Issues & Solutions**

<details>
<summary><b>🔽 Click for troubleshooting guide</b></summary>

#### **🚫 Admin Login "Network Error"**
```bash
# Step 1: Check database setup
🌐 Visit: http://localhost:8000/setup.html

# Step 2: Ensure XAMPP is running
✅ Open XAMPP Control Panel
✅ Start Apache + MySQL (green status)

# Step 3: Create database if missing
🌐 Visit: http://localhost/phpmyadmin
📁 Create database: seva_connect
📂 Import: database/seva_connect.sql

# Step 4: Use default credentials
👤 Username: admin
🔐 Password: admin123
```

#### **🚫 "Python not found" Error**
```bash
# Solution 1: Check Python installation
python --version

# Solution 2: Add Python to PATH
# Windows: Add Python installation directory to PATH
# Or reinstall Python with "Add to PATH" checked
```

#### **🚫 "PHP not found" Error**
```bash
# Solution: Install XAMPP
# Download from: https://www.apachefriends.org/
# Or add PHP to PATH manually
```

#### **🚫 Database Connection Error**
```bash
# Check XAMPP MySQL is running
# Verify database name: seva_connect
# Check .env file database credentials
```

#### **🚫 Payment Issues**
```bash
# Verify Razorpay keys in .env
# Check if Python payment service is running (port 5000)
# Use test cards for testing
```

#### **🚫 OAuth Not Working**
```bash
# Verify redirect URIs in Google/Microsoft console
# Check client ID and secret in .env
# Ensure OAuth service is running (port 5001)
```

#### **🚫 Certificates Not Generating**
```bash
# Check Python PIL/Pillow installation: pip install Pillow
# Verify certificate service is running (port 5002)
# Check file permissions in certificates folder
```

</details>

### 🆘 **Need Help?**

```
🐛 Issue with setup? Check the troubleshooting section above
📧 Still stuck? Create an issue with:
   - Your operating system
   - Error message (full text)
   - Steps you tried
```

---

<div align="center">

## 🎉 **You're All Set!**

### **Your donation platform is ready to serve humanity! 🌟**

**🌐 Main Site**: http://localhost:8000  
**🔐 Admin Panel**: http://localhost:8000/admin  
**📊 Service APIs**: Ports 5000, 5001, 5002  

---

**Made with ❤️ for humanitarian causes**  
*Serving humanity through technology*

[![Follow](https://img.shields.io/badge/Follow-Repository-blue?style=for-the-badge)](https://github.com)
[![Star](https://img.shields.io/badge/Give%20a-⭐-yellow?style=for-the-badge)](https://github.com)
[![Support](https://img.shields.io/badge/Support-Donate-green?style=for-the-badge)](http://localhost:8000)

</div>

## Setup Instructions

### Prerequisites

1. **XAMPP** (Apache + MySQL + PHP)
   - Download from: https://www.apachefriends.org/download.html
   - Install with default settings

2. **Web Browser** (Chrome, Firefox, Edge, Safari)

### Installation Steps

#### Step 1: Install and Setup XAMPP

1. Download and install XAMPP for Windows
2. Open XAMPP Control Panel
3. Start **Apache** and **MySQL** services
4. Click on **Admin** button next to MySQL to open phpMyAdmin

#### Step 2: Create Database

1. In phpMyAdmin, click on **"New"** in the left sidebar
2. Create a new database named: `seva_connect`
3. Select the database and go to **"Import"** tab
4. Choose the file: `database/seva_connect.sql`
5. Click **"Go"** to import the database structure

#### Step 3: Setup Website Files

1. Copy the entire "Seva Connect 2.O" folder to: `C:\xampp\htdocs\`
2. Rename the folder to: `seva-connect` (optional, for cleaner URLs)
3. Make sure the folder structure looks like:
   ```
   C:\xampp\htdocs\seva-connect\
   ├── index.html
   ├── css/
   ├── js/
   ├── php/
   ├── admin/
   ├── database/
   └── certificates/
   ```

#### Step 4: Set Permissions (Important!)

1. Right-click on the `seva-connect` folder
2. Go to **Properties** → **Security** tab
3. Give **Full Control** permissions to:
   - `IIS_IUSRS` (if using IIS)
   - `Everyone` (for testing purposes)
   - `NETWORK SERVICE`

#### Step 5: Test the Installation & Network Access

1. **Test Locally**:
   - Open your web browser
   - Go to: `http://localhost:8000/`
   - You should see the Seva Connect homepage

2. **Test Network Access**:
   - In VS Code, run the task "Get Local IP Address" to find your computer's IP
   - Other devices on the same network can access via: `http://YOUR_IP:8000/`
   - Example: `http://192.168.1.100:8000/`

3. **Test Features**:
   - Test donations and membership registration (₹1,111 fee)
   - Access admin panel at: `http://localhost:8000/admin/` or `http://YOUR_IP:8000/admin/`
   - Make changes in admin panel and verify real-time updates

### Membership System Changes

**New Membership Features**:
- **Membership Fee**: ₹1,111 (fixed amount)
- **Phone Number**: Now optional field
- **Message Field**: Replaced address with message to team
- **Beautiful Certificates**: Professional design matching your uploaded sample
- **Real-time Updates**: Admin changes reflect immediately

**Certificate Features**:
- Personalized with member name (like "Ram" in your sample)
- Professional design with decorative borders
- "Certificate of Appreciation" format
- Both light and dark theme versions
- Automatic generation upon membership payment

```php
$host = 'localhost';        // XAMPP default
$dbname = 'seva_connect';   // Your database name
$username = 'root';         // XAMPP default username
$password = '';             // XAMPP default password (empty)
```

### Admin Panel Features

Access the admin panel at: `http://localhost/seva-connect/admin/`

**Dashboard**
- View donation statistics
- Total amounts raised
- Member counts
- Recent activities

**Manage Content**
- Edit about text (stored in `admin/about.txt`)
- Update site settings
- Owner information for certificates

**Manage Photos**
- Upload new photos for logo, hero image, gallery
- Delete existing photos
- Photos are stored in `admin/photos/` folder

**Donations Management**
- View all donations
- Filter by cause or search donors
- Export donation data to CSV
- Update donation status

**Members Management**
- View all members
- Search members
- Toggle member status (active/inactive)
- Export member data to CSV
- Download member certificates

**Certificates Management**
- Generate new certificates manually
- View generated certificates
- Download certificates (light/dark theme)
- Email certificates to members

### File Structure

```
seva-connect/
├── index.html              # Main website homepage
├── css/
│   └── style.css          # Main stylesheet with light/dark themes
├── js/
│   └── script.js          # Frontend JavaScript functionality
├── php/
│   ├── db_config.php      # Database connection settings
│   ├── process_donation.php    # Handles donation submissions
│   ├── process_membership.php  # Handles membership registrations
│   └── admin_*.php        # Admin panel backend files
├── admin/
│   ├── index.html         # Admin panel interface
│   ├── admin.css          # Admin panel styles
│   ├── admin.js           # Admin panel JavaScript
│   ├── about.txt          # About text (editable by admin)
│   └── photos/            # Folder for website images
│       ├── logo.png       # Site logo
│       ├── hero-image.jpg # Hero section image
│       └── ...            # Other images
├── database/
│   └── seva_connect.sql   # Database schema and initial data
├── certificates/          # Generated member certificates
└── README.md             # This file
```

### Content Management

#### Changing About Text
1. Go to Admin Panel → Manage Content
2. Edit the about text in the textarea
3. Click "Save Changes"
4. The text will be updated in `admin/about.txt` and reflected on the website

#### Managing Photos
1. Go to Admin Panel → Manage Photos
2. Select photo type (Logo, Hero Image, Gallery)
3. Choose image file and upload
4. Photos are stored in `admin/photos/` folder
5. Update the HTML file to reference new photo paths if needed

#### Certificate Customization
- Light and dark theme certificates are generated automatically
- Owner name on certificates can be changed in Admin Panel → Manage Content → Site Settings
- Certificate templates are in the PHP code and can be customized

### Database Configuration

The database connection settings are in `php/db_config.php`:

```php
$host = 'localhost';        // XAMPP default
$dbname = 'seva_connect';   // Your database name
$username = 'root';         // XAMPP default username
$password = '';             // XAMPP default password (empty)
```

### Cause-Specific Content Management

**New Content Structure**:
Each of the 8 causes now has dedicated folders:

```
admin/causes/
├── orphanage/
│   ├── content.txt         # Cause-specific description
│   └── photos/             # Cause-specific images
├── gowshala/
│   ├── content.txt
│   └── photos/
├── vridha-ashram/
│   ├── content.txt
│   └── photos/
├── health/
│   ├── content.txt
│   └── photos/
├── samuhik-vivah/
│   ├── content.txt
│   └── photos/
├── pooja-rituals/
│   ├── content.txt
│   └── photos/
├── eye-camp/
│   ├── content.txt
│   └── photos/
└── environment/
    ├── content.txt
    └── photos/
```

**How to Update Cause Content**:
1. Edit the `content.txt` file in each cause folder
2. Add photos to the respective `photos/` folders
3. Update your website to reference these new contents and images

### Network Access Setup

**Making Website Accessible on Network**:

1. **Start the Development Server**:
   - Use VS Code task: "Start Seva Connect Development Server"
   - This runs: `php -S 0.0.0.0:8000`

2. **Find Your IP Address**:
   - Use VS Code task: "Get Local IP Address"
   - Or manually check: `ipconfig` in Command Prompt

3. **Access from Other Devices**:
   - Same network devices can access via: `http://YOUR_IP:8000`
   - Example: `http://192.168.1.100:8000`

4. **Firewall Settings** (if needed):
   - Allow PHP through Windows Firewall
   - Port 8000 should be accessible

### Troubleshooting

**Common Issues:**

1. **"Database connection failed"**
   - Make sure MySQL is running in XAMPP
   - Check database name in `php/db_config.php`
   - Ensure database `seva_connect` exists

2. **"Permission denied" errors**
   - Set proper folder permissions
   - Make sure `certificates/` and `admin/photos/` folders are writable

3. **Photos not uploading**
   - Check folder permissions on `admin/photos/`
   - Ensure file size is within PHP limits
   - Check file type is allowed (jpg, png, gif)

4. **Forms not submitting**
   - Check that Apache is running
   - Verify PHP files are in correct location
   - Check browser console for JavaScript errors

**PHP Configuration:**
If you need to upload large files, edit `C:\xampp\php\php.ini`:
```ini
upload_max_filesize = 10M
post_max_size = 10M
max_execution_time = 300
```

### Security Notes

For production use, consider:
1. Change database password from default empty password
2. Add proper user authentication for admin panel
3. Use HTTPS for secure data transmission
4. Implement proper input validation and sanitization
5. Add CSRF protection for forms
6. Regular database backups

### Support and Customization

The codebase is well-structured and documented for easy customization:

- **Frontend**: HTML, CSS, JavaScript (responsive design)
- **Backend**: PHP with PDO for database operations
- **Database**: MySQL with proper indexing and relationships
- **Features**: Modular design for easy feature additions

For additional features or customizations, modify the relevant files and update the database schema as needed.

### License

This project is created for humanitarian purposes. Feel free to use, modify, and distribute for similar noble causes.

---

**Made with ❤️ for serving humanity**
