document.addEventListener('DOMContentLoaded', function () {

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
    document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
    document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
    document.querySelector('#compose').addEventListener('click', compose_email);

    // Add event listener for the compose form, this is a form submission handler
    document.querySelector('#compose-form').onsubmit = send_email;

    // By default, load the inbox
    load_mailbox('inbox');
});

function compose_email() {

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

    // Show the mailbox and hide other views
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Show the mailbox name
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    get_mailbox(mailbox);
}

function send_email(event) {
    event.preventDefault();

    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.error || 'An error occurred.');
                });
            }
            return response.json();
        })
        .then(result => {
            console.log(result);
            load_mailbox('sent');
        })
        .catch(error => {
            console.error(error);
            alert(error.message); // Display error message to the user
        });
}

function get_mailbox(mailbox) {
    // Fetch emails from the specified mailbox
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
            // Clear the email view
            const emailsView = document.querySelector('#emails-view');
            emailsView.innerHTML = '';

            // Iterate through each email and display it
            emails.forEach(email => {
                const emailElement = document.createElement('div');
                emailElement.className = 'email-item';
                emailElement.style.border = '1px solid #ddd';
                emailElement.style.padding = '15px';
                emailElement.style.margin = '5px 0';
                emailElement.style.borderRadius = '5px';
                emailElement.style.cursor = 'pointer';
                emailElement.style.backgroundColor = email.read ? '#f1f1f1' : 'white';
                emailElement.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>${email.sender}</strong> - ${email.subject}
                <span style="color: gray;">(${email.timestamp})</span>
            </div>
            <div>
                <button class="archive-button" style="background: none; border: none; cursor: pointer;">
                    <i class="material-icons archive-button" style="cursor: pointer;">${email.archived ? 'unarchive' : 'archive'}</i>
                </button>
            </div>
        </div>
    `;

                // Add event listener for clicking the email block
                emailElement.addEventListener('click', () => {
                    // Mark email as read and load email details
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            read: true
                        })
                    }).then(() => {
                        load_email(email.id);
                    });
                });

                // Add event listener for the "Archive" button
                emailElement.querySelector('.archive-button').addEventListener('click', (event) => {
                    event.stopPropagation(); // Prevent triggering the email block click
                    fetch(`/emails/${email.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            archived: !email.archived
                        })
                    }).then(() => get_mailbox('inbox'));
                });

                emailsView.appendChild(emailElement);
            });
        })
        .catch(error => console.error('Error loading mailbox:', error));
}

function load_email(email_id) {
    // Fetch the email details
    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            // Show the email details
            const emailsView = document.querySelector('#emails-view');
            emailsView.innerHTML = `
                <h3>${email.subject}</h3>
                <p><strong>From:</strong> ${email.sender}</p>
                <p><strong>To:</strong> ${email.recipients.join(', ')}</p>
                <p><strong>Timestamp:</strong> ${email.timestamp}</p>
                <hr>
                <p>${email.body}</p>
                <button class="reply-button">Reply</button>
            `;

            document.querySelector('.reply-button').addEventListener('click', () => reply_email(email));
        })
        .catch(error => console.error('Error loading email:', error));
}

function reply_email(email) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Pre-fill composition fields
    document.querySelector('#compose-recipients').value = email.sender;
    document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`;
    document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote:\n${email.body}\n\n`;
}