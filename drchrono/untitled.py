from drchrono.models import Doctor, Patient, Appointment
from drchrono.serializers import DoctorSerializer1, PatientSerializer1, AppointmentSerializer1

data = {u'website': None, u'last_name': u'Su', u'suffix': None, u'specialty': u'Acupuncture', u'profile_picture': u'', u'group_npi_number': None, u'timezone': u'US/Eastern', u'id': 254818, u'first_name': u'Wen-Yuh', u'npi_number': u'', u'country': u'US', u'practice_group_name': u'', u'is_account_suspended': False, u'office_phone': u'3129272532', u'home_phone': u'', u'practice_group': 277763, u'cell_phone': u'3129272532', u'email': u'wsu23@uic.edu', u'job_title': u'API/Developer'}

data = {u'last_name': u'Su', u'id': 254818, u'first_name': u'Wen-Yuh'}
model = Doctor.objects.get(pk=data['id'])

serializer = DoctorSerializer1(data=data)

serializer.is_valid()
serializer.save()



data1 = {u'primary_care_physician': u'', u'last_name': u'Smith', u'emergency_contact_phone': u'', u'date_of_first_appointment': u'2019-11-24', u'updated_at': u'2019-11-27T02:52:55', u'chart_id': u'SMAM000001', u'referring_source': None, u'race': u'white', u'id': 84824281, u'ethnicity': u'not_hispanic', u'employer_state': u'', u'city': u'San Jose', u'first_name': u'Amy', u'middle_name': None, u'doctor': 254818, u'disable_sms_messages': False, u'employer': u'', u'state': u'CA', u'date_of_birth': u'1952-09-02', u'employer_city': u'', u'home_phone': u'(844) 569-8628', u'patient_status': u'A', u'patient_photo_date': None, u'email': u'', u'zip_code': u'95125', u'patient_photo': u'https://89c910a944a358e76e5c-8d4eb89103c5685e8de4aa577c465b04.ssl.cf5.rackcdn.com/patient_photos/2018/07/a9db5a9a-52bf-4470-9160-cda52b9d6757.png', u'emergency_contact_name': u'', u'date_of_last_appointment': u'2019-11-25', u'patient_payment_profile': u'Cash', u'social_security_number': u'525-35-4545', u'address': u'2025 Hamilton Ave', u'employer_zip_code': u'', u'cell_phone': u'(650) 215-6343', u'preferred_language': u'eng', u'responsible_party_name': None, u'nick_name': u'', u'gender': u'Female', u'emergency_contact_relation': None, u'office_phone': u'(844) 569-8628', u'employer_address': u'', u'responsible_party_phone': None, u'offices': [271129], u'responsible_party_relation': None, u'copay': u'', u'default_pharmacy': u'0508272', u'responsible_party_email': None}
data2 = {u'base_recurring_appointment': None, u'color': u'', u'first_billed_date': u'2019-12-03T09:00:00', u'last_billed_date': u'2019-12-03T09:00:00', u'billing_status': u'', u'primary_insurer_payer_id': u'', u'duration': 75, u'appt_is_break': False, u'id': u'135526775', u'billing_notes': [], u'scheduled_time': u'2019-12-03T09:00:00', u'secondary_insurer_name': u'', u'doctor': 254819, u'status': u'Arrived', u'patient': 84824292, u'cloned_from': None, u'exam_room': 1, u'updated_at': u'2019-12-03T02:07:47', u'recurring_appointment': False, u'supervising_provider': None, u'created_at': u'2019-12-03T01:49:23', u'icd10_codes': []}
serializer = PatientSerializer1(data=data1)

data2 = {u'base_recurring_appointment': None, u'color': u'', u'first_billed_date': u'2019-12-03T09:00:00', u'last_billed_date': u'2019-12-03T09:00:00', u'billing_status': u'', u'primary_insurer_payer_id': u'', u'duration': 75, u'appt_is_break': False, u'id': u'135526775', u'billing_notes': [], u'scheduled_time': u'2019-12-03T09:00:00', u'secondary_insurer_name': u'', u'doctor': 254819, u'status': u'Arrived', u'patient': 84824292, u'cloned_from': None, u'exam_room': 1, u'updated_at': u'2019-12-03T02:07:47', u'recurring_appointment': False, u'supervising_provider': None, u'created_at': u'2019-12-03T01:49:23', u'icd10_codes': []}
data3 = {u'profile': None, u'icd9_codes': [], u'office': 271129, u'base_recurring_appointment': None, u'color': u'', u'first_billed_date': u'2019-12-03T12:00:00', u'last_billed_date': u'2019-12-03T12:00:00', u'billing_status': u'', u'primary_insurer_payer_id': u'', u'duration': 30, u'appt_is_break': False, u'id': u'135526778', u'billing_notes': [], u'scheduled_time': u'2019-12-03T12:00:00', u'secondary_insurer_name': u'', u'doctor': 254818, u'primary_insurance_id_number': u'', u'is_walk_in': False, u'billing_provider': None, u'status': u'', u'patient': 84824290, u'cloned_from': None, u'exam_room': 1, u'updated_at': u'2019-12-03T01:49:44', u'reason': u'', u'is_virtual_base': False, u'secondary_insurer_payer_id': u'', u'allow_overlapping': False, u'secondary_insurance_id_number': u'', u'primary_insurer_name': u'', u'recurring_appointment': False, u'supervising_provider': None, u'created_at': u'2019-12-03T01:49:44', u'icd10_codes': [], u'deleted_flag': False, u'notes': u''}

data3 = {u'checkin_time': now(), u'status': u'Arrived', u'icd9_codes': [], u'office': 271129, u'base_recurring_appointment': None, u'color': u'', u'first_billed_date': u'2019-12-05T00:00:00', u'last_billed_date': u'2019-12-05T00:00:00', u'billing_status': u'', u'primary_insurer_payer_id': u'', u'duration': 30, u'appt_is_break': False, u'id': u'135761878', u'billing_notes': [], u'scheduled_time': u'2019-12-05T00:00:00', u'secondary_insurer_name': u'', u'doctor': 254818, u'primary_insurance_id_number': u'', u'is_walk_in': False, u'billing_provider': None, u'primary_insurer_name': u'', u'profile': None, u'patient': 84824290, u'cloned_from': None, u'exam_room': 1, u'updated_at': u'2019-12-05T15:49:03', u'reason': u'', u'secondary_insurer_payer_id': u'', u'allow_overlapping': False, u'secondary_insurance_id_number': u'', u'is_virtual_base': False, u'recurring_appointment': False, u'supervising_provider': None, u'created_at': u'2019-12-05T14:36:39', u'icd10_codes': [], u'deleted_flag': False, u'notes': u''}

serializer = AppointmentSerializer1(data=data3)

model = Appointment.objects.get(pk=serializer.validated_data['id'])
135620212


data = [{u'last_name': u'Su', u'id': 254818, u'first_name': u'Bala'}, {u'last_name': u'Su', u'id': 254818, u'first_name': u'Wen-Yuh'}]