### Overview Backend Structure

Django + Jquery + Ajax + Bootstrap

##### Basic MTV Framework
```
Models
    |-- Doctors
    |
    |-- Patients
    |
    |-- Appointments

Views 
    |-- Home Page(IndexView)
    |
    |-- Patient CheckIn Form(Patient CheckIn View)
    |
    |-- Demographic Form(Patient Update Info View)
    |
    |-- Update Patient Status(Appointment View[Arrived, In Session, Complete, Cancelled])
    |
    |-- Login, Logout, Sync Data from Remote

Templates
    |-- base.html
    |
    |-- index.html
    |
    |-- checkin.html
    |
    |-- confirm_appointment.html
    |
    |-- patient_info.html
```

##### Improve the Form Rendering
```
Forms
    |-- CheckIn Form
    |
    |-- Patient Update Info Form
```

##### Improve on the API Driven Web Application
```
Serializers

[deserializer]
    |-- Doctor
    |
    |-- Patient
    |
    |-- Appointment

[serializer]
    |-- RetrieveAppointment
```

