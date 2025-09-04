# Portolio Web Application (FolaDevelops)  

A full-stack portfolio web application demonstrating authentication systems, e-commerce functionality, AI systems, deployment pipelines, and integrated developer projects.  

This project serves as a showcase of my backend and frontend engineering skills, as well as my ability to deploy production-ready systems.  


🔗 **Live Demo:** [foladevelops.onrender.com](https://foladevelops.onrender.com)

---

## 🚀 Features  

- **Authentication System**  
  - Sign-up, login, logout with secure session handling.  
  - Email verification and password reset via one-time codes.  
  - Role-based access (admin vs. user).  

- **E-Commerce Module**  
  - Product listing and order workflow.  
  - Responsive, user-friendly design.  
  - Automated confirmation emails for successful orders.  

- **Deployment & Hosting**  
  - VPS hosting with Nginx, Gunicorn, and PostgreSQL.  
  - SSL security via Let’s Encrypt.  
  - Static file handling through Nginx.  

- **Email Automation**  
  - SMTP integration for account verification, password resets, and order confirmations.  

---

## 🛠️ Tech Stack  

- **Backend:** Python, Flask, SQLAlchemy  
- **Frontend:** HTML, CSS, JavaScript, Jinja templates  
- **Database:** PostgreSQL  
- **Deployment:** VPS (Hostinger), Nginx, Gunicorn, Let’s Encrypt SSL  
- **Email:** SMTP (custom domain)  
- **Version Control:** Git, GitHub  

---



## 🖥️ Preview
### 🔑 Login Page
![Login Page](static/images/demo/login-webpage.png) 
<br><br>
### 🛍️ Product Listing
![Product Listing](static/images/demo/store-page.png)
<br><br>
### ✅ Automated Order Confirmation Email
![Order Successful](static/images/demo/email-template.png) 

---

## 📂 Project Structure  

    fola-develops/
    │── main.py             # Flask app entry point
    │── entities.py         # Database entities
    │── forms.py            # WTForms
    │── templates/          # Jinja HTML templates
    │── static/             # CSS, JS, images
    │── email_templates.py  # Styled email templates
    │── items_data.py       # E-commerce demo items
    │── requirements.txt    # Dependencies
    └── README.md

---

## 🔧 Setup & Installation  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/folajimiabolade/fola-develops.git
   cd fola-develops

2. **Create a virtual environment**  
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/Mac
    venv\Scripts\activate     # On Windows

3. **Install dependencies**  
    ```bash
    pip install -r requirements.txt

4. **Set up environment variables** 
    ```bash
    export DATABASE-URI=your_postgres_or_sqlite_url
    export ADMIN-EMAIL=your_primary_email_for_admin_control
    export EMAIL=your_email_for_smtp
    export PASSWORD=your_password_for_smtp
    export CLOUDINARY_URL=your_cloudinary_cloud_storage_url
    export API-URL=your_green_api_url_for_automated_whatsapp_messages
    export ID-INSTANCE=your_green_api_id
    export API-TOKEN-INSTANCE=your_green_api_token
    export NUMBER=your_green_api_phone_number
    export FLASK-SECRET-KEY=your_flask_secret_key
    export VIDEO-URL=your_video_url

4. **Start the app** 
    ```bash
    flask run

---

## 🌐 Deployment 

- Configured for VPS hosting with Nginx + Gunicorn.

- SSL certificates via Let’s Encrypt.

- PostgreSQL managed securely with environment variables.

- Static assets served directly through Nginx.

---

## 📬 Contact

- **Portfolio (Live Projects):** [foladevelops.onrender.com](https://foladevelops.onrender.com)  
- **GitHub:** [github.com/folajimiabolade](https://github.com/folajimiabolade)  
- **X:** [x.com/onlyonefola](https://x.com/onlyonefola)  
- **LinkedIn:** [linkedin.com/in/folajimi-abolade-379a01362](https://www.linkedin.com/in/folajimi-abolade-379a01362)  
- **Email:** folajimiabolade@gmail.com 

💡 *Feel free to reach out for collaborations, opportunities, or just to connect.*
