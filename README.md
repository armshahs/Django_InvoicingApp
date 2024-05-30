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
- **Report Generation:** Generate pdf reports for invoices.
- **Reminder Emails:** Send payment reminder emails with pdf attachments.
- **Customization:** Customize invoice templates and settings to suit business needs.


## URL Endpoints

### Authentication

- **Registration:** `/register/`
- **Login:** `/login/`
- **Logout:** `/logout/`

### Invoices

- **Create Invoice:** `/invoice/create/`
- **Edit Invoice:** `/invoice/<invoice_id>/edit/`
- **Delete Invoice:** `/invoice/<invoice_id>/delete/`

### Clients

- **Create Client:** `/client/create/`
- **Edit Client:** `/client/<client_id>/edit/`
- **Delete Client:** `/client/<client_id>/delete/`

### Payments

- **Record Payment:** `/payment/create/`
- **Edit Payment:** `/payment/<payment_id>/edit/`
- **Delete Payment:** `/payment/<payment_id>/delete/`

### Reports

- **Generate Invoice Report:** `/report/invoices/`
- **Generate Payment Report:** `/report/payments/`
- **Generate Client Report:** `/report/clients/`


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
5. Generate invoice pdfs.
6. Send payment reminder emails with pdf attachments

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/my-feature` or `git checkout -b bugfix/fix-issue`.
3. Make your changes and commit them: `git commit -am 'Add new feature'`.
4. Push to your branch: `git push origin feature/my-feature`.
5. Submit a pull request detailing your changes.
