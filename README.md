# Invoicing App using Django


## Overview

This project is an invoicing application built using Django, designed to help businesses manage their invoicing process efficiently. It provides features for creating invoices, managing clients, tracking payments, and generating pdf invoices.

**Links:**
1. Frontend code - https://github.com/armshahs/invoiceapp_frontend_vue
2. Product demo - https://www.youtube.com/watch?v=XpkBB3E0O5I


## Features

- **Invoice Creation:** Create and manage invoices.
- **Client Management:** Manage client information and track client interactions.
- **Payment Tracking:** Track payments and monitor outstanding balances.
- **Report Generation:** Generate PDF reports for invoices.
- **Reminder Emails:** Send payment reminder emails with PDF attachments.
- **Customization:** Customize invoice templates and settings to suit business needs.


## URL Endpoints

### Authentication

- **Registration:** `api/v1/users/`
- **Login:** `api/v1/token/login/`
- **Logout:** `api/v1/token/logout/`


### Clients

- **Client List:** GET `api/v1/clients/` 
- **Create Client:** POST `api/v1/clients/` 
- **Edit Client:** PUT/PATCH `api/v1/clients/<int:id>/`
- **Delete Client:** DELETE `api/v1/clients/<int:id>/`


### Teams

- **Get Team:** GET `api/v1/teams/`
- **Create Team:** POST `api/v1/teams/`
- **Edit Team:** PUT/PATCH `api/v1/teams/<int:id>/`
- **Delete Team:** DELETE `api/v1/teams/<int:id>/`


### Invoices

- **Invoice List:** GET `api/v1/invoices/`
- **Create Invoice:** POST `api/v1/invoices/`
- **Edit Invoice:** PUT/PATCH `api/v1/invoices/<int:id>/`
- **Delete Invoice:** DELETE `api/v1/invoices/<int:id>/`
- **Items in a given invoice Invoice (invoice_id as query param):** `/api/v1/items/?invoice_id=<int: id>`


### Invoice PDF Generation

- **Download invoice PDF:**  `api/v1/invoices/<int:invoice_id>/generate_pdf/`


### Reminder Emails with PDF attachments

- **Invoice send email reminder:**  `api/v1/invoices/<int:invoice_id>/send_reminder/`


## Installation

### Prerequisites

- Python 3.x
- Django

### Steps

1. Clone the repository:

```bash
git clone https://github.com/armshahs/invoicing_app_django.git
```

2. Navigate to the project directory:

```bash
cd invoicing_app_django
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```



## Usage

1. Register for a new account or login if you already have one.
2. Create clients by navigating to the Clients section and adding client details.
3. Create invoices for clients, specifying the items, quantities, and prices.
4. Track payments by recording payments against invoices.
5. Generate invoice PDFs.
6. Send payment reminder emails with PDF attachments

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/my-feature` or `git checkout -b bugfix/fix-issue`.
3. Make your changes and commit them: `git commit -am 'Add new feature'`.
4. Push to your branch: `git push origin feature/my-feature`.
5. Submit a pull request detailing your changes.
