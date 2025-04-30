# Mail Project

This project is a web-based email client built using **Django** for the backend and **JavaScript** for the frontend. It allows users to send, receive, and manage emails with features like inbox, sent mail, archiving, and replying.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Compose Email**: Send emails to one or more recipients.
- **Mailbox Views**:
  - Inbox: View received emails.
  - Sent: View sent emails.
  - Archive: Archive and unarchive emails.
- **Email Details**: View email content and mark emails as read.
- **Reply to Emails**: Pre-fill the reply form with the original email's details.
- **Dynamic Frontend**: Built with JavaScript for seamless user interactions.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django database)
- **API**: RESTful API for email operations

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ngxvu/mail.git
   cd mail
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Run the development server:
   ```bash
   python manage.py runserver
   ```

5. Open the application in your browser at `http://127.0.0.1:8000/`.

## API Endpoints

- `GET /emails/<mailbox>`: Fetch emails from a specific mailbox (inbox, sent, archive).
- `POST /emails`: Send a new email.
- `GET /emails/<email_id>`: Retrieve details of a specific email.
- `PUT /emails/<email_id>`: Update email properties (e.g., mark as read or archive).

## File Structure

- `mail/mail/urls.py`: URL routing for the application.
- `mail/mail/views.py`: Backend logic for handling requests.
- `mail/mail/static/mail/inbox.js`: JavaScript for dynamic frontend behavior.
- `mail/mail/templates/mail`: HTML templates for rendering views.

## Usage

1. **Register**: Create a new account.
2. **Log In**: Access your email inbox.
3. **Compose Email**: Send emails to other registered users.
4. **View Emails**: Check your inbox, sent mail, or archived emails.
5. **Reply**: Respond to received emails directly.

## License

This project is for educational purposes and does not include a specific license.
