# ZeroTrace - Professional Setup Guide

## 📂 Project Structure
- `backend/`: FastAPI server with Supabase integration & Blockchain logging.
- `desktop/`: PyQt5 Desktop application with grid animation & credit validation.
- `web/`: Simple landing page for marketing and credit purchases.

## ⚙️ Backend Setup
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create a `.env` file based on `.env.example`.
4. **Supabase Config**:
   - Create a new Supabase project.
   - Table `profiles`: `id (uuid, pk)`, `email (text)`, `credits (int, default 0)`.
   - Table `certificates`: `id (int, pk)`, `user_id (uuid)`, `device_id (text)`, `cert_data (json)`, `created_at (timestamptz)`.
5. Run server: `python main.py`.

## 🖥️ Desktop Setup
1. Navigate to `desktop/`.
2. Ensure `engine/a.exe` is present.
3. Run app: `python app.py`.

## 👤 Sample Test User
- **Email**: `test@example.com`
- **Password**: `password123`
- **Initial Credits**: 5 (Add manually in Supabase `profiles` table for testing).

## 🚀 Flow
1. **Login**: Use the test credentials to enter the desktop app.
2. **Credits**: App will fetch your remaining wipes from the backend.
3. **Wipe**: Select a disk and start. The app validates your credits via API before proceeding.
4. **Finalize**: After wiping, a certificate is generated and logged to the backend's tamper-proof system.
