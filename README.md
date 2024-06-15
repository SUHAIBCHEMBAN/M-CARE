M-CARE Clinic

M-CARE Clinic is a comprehensive hospital management web application built with Django. It features separate interfaces for admins and users, facilitating efficient hospital operations and patient management.

Table of Contents

> Features
> Usage
> Hosting
> Technologies Used

1-Features

=> Admin Panel

CRUD Operations: Manage doctors, patients, appointments and other resources.
User Management: Handle user roles and permissions.
Appointment Management: View and manage all appointments.
Payment Management: Track and manage payments.

=> User Interface

Doctor Booking: Search, filter, and book appointments with doctors.
Payment Integration: Secure payment processing with Razorpay.
Email OTP Login: Secure login with OTP sent to the user's email.
Profile Management: Users can manage their profiles, including medical history.

=> Access the application:

Admin Panel: www.mcareclinicservice.live/admin/
User Interface: www.mcareclinicservice.live

2-Usage

=> Admin Panel

Log in using the superuser credentials.
Manage doctors, patients, appointments, and payments through the intuitive dashboard.

=> User Interface

Register and log in using email OTP.
Browse, search, and filter doctors.
Book appointments and make payments securely with Razorpay.
Manage personal profile and view appointment history.

3-Hosting

AWS EC2 and Route 53
M-CARE Clinic is hosted on an AWS EC2 instance, with Route 53 serving as the DNS management service.

4-Technologies Used

Backend: Python Django
Frontend: HTML, CSS, JavaScript (optional for enhancements)
Database: PostgreSQL
Payments: Razorpay integration
Authentication: Email OTP for secure login
Hosting: AWS EC2
Proxy Server: Route 53
Calendar:Flatpicker
Optimize:Debug toolbar
Auto Update:Celery
