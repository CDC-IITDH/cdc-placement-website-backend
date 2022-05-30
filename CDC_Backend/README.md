# API References

1. [**Common APIs**](#common-apis)
   1. [**api/login/**](#apilogin)
2. [**Student APIs**](#student-portal-apis)
   1. [**api/student/profile/**](#apistudentprofile)
   2. [**api/student/getDashboard/**](#apistudentgetdashboard)
   3. [**api/student/addResume/**](#apistudentaddresume)
   4. [**api/student/deleteResume/**](#apistudentdeleteresume)
   5. [**api/student/submitApplication/**](#apistudentsubmitapplication)
3. [**Admin APIs**](#admin-portal-apis)
   1. [**api/admin/markStatus/**](#apiadminmarkstatus)
   2. [**api/admin/getDashboard/**](#apiadmingetdashboard)
   3. [**api/admin/updateDeadline/**](#apiadminupdatedeadline)
   4. [**api/admin/updateOfferAccepted**](#apiadminupdateofferaccepted)
   5. [**api/admin/updateEmailVerified**](#apiadminupdateemailverified)
   6. [**api/admin/updateAdditionalInfo**](#apiadminupdateadditionalinfo)
   7. [**api/admin/getApplications**](#apiadmingetApplications)
   8. [**api/admin/submitApplication**](#apiadminsubmitApplication)
   9. [**api/admin/generateCSV**](#apiadmingeneratecsv)
   10. [**api/admin/addPPO**](#apiadminaddppo)
   11. [**api/admin/getStudentApplication**](#apiadmingetstudentapplication)
4. [**Company APIs**](#company-portal-apis)
   1. [**api/company/addPlacement/**](#apicompanyaddplacement)
5. [**Common Errors**](#common-errors)

---

# Common APIs

## `api/login/`

This Api is used to Verify the user and find out the role he/she has

### How to Use?

Send a `POST` request to `api/login/`<br>
Request_Body:

```json
{}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Login",
  "message": "Verified",
  "user_type": ["student"]
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- user_type: Tells us about the role the user possess. Can have these values
  - student
  - Admin

### Status Codes

The possible responses for this api request are as follows

| Status Codes | Possible Messages |
| ------------ | ----------------- |
| 200 OK       | `Verified`        |

You may see some different errors which can be seen [here](#common-errors)

---

# Student Portal APIs

## `api/student/profile`

This Api is used to get the profile of the student.

### How to Use?

Send a `GET` request to `api/student/profile`<br>
Request_Body:

```json
{}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Student Profile",
  "message": "Details Found",
  "details": {
    "id": "190010036",
    "resume_list": [
      {
        "link": "https://storage.googleapis.com/cdc-backend-attachments/resume/190010036%2F8KIOT3PW1JIS718_CSE-V-SEM.pdf",
        "name": "8KIOT3PW1JIS718_CSE-V-SEM.pdf"
      }
    ],
    "offers": [
      {
        "designation": "Software Developer",
        "company_name": "Make My Trip",
        "application_id": "LLW4STE76GEJYOR"
      }
    ],
    "roll_no": 190010036,
    "name": "Gowtham Sai",
    "batch": "2019",
    "branch": "CSE",
    "phone_number": 9390291911,
    "cpi": "9.15"
  }
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- details: Has the student data.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Details Found`        |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/student/getDashboard`

This Api is used to get all the placements applicable to the student and his applications which he has already applied.

### How to Use?

Send a `GET` request to `api/student/getDashboard`<br>

Request_Body:

```json
{}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

> Only users with `student` role can access this Api.

### Response

Response is a Json with these fields

```json
{
  "action": "Get Dashboard - Student",
  "message": "Data Found",
  "placements": [
    {
      "id": "Q54IRZZMC3RP8F6",
      "company_details_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FI5U4RDTV0OP0EM0_2019+Student+Details+-+Total%28State+Sort%29+-+Copy.pdf",
          "name": "I5U4RDTV0OP0EM0_2019 Student Details - Total(State Sort) - Copy.pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FW04JWWNNMIBX0JX_2019+Student+Details+-+Total%28State+Sort%29.pdf",
          "name": "W04JWWNNMIBX0JX_2019 Student Details - Total(State Sort).pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FT1BXP98WBT9BHOR_AP0313017732021LL-Driving+Licence+-+Copy.pdf",
          "name": "T1BXP98WBT9BHOR_AP0313017732021LL-Driving Licence - Copy.pdf"
        }
      ],
      "description_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FC78TE2Z67BPZ41O_CSE-V-SEM.pdf",
          "name": "C78TE2Z67BPZ41O_CSE-V-SEM.pdf"
        }
      ],
      "compensation_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2F8D5OFQ46H43DD3S_module5And6Attendance.pdf",
          "name": "8D5OFQ46H43DD3S_module5And6Attendance.pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FG8OU2PE919PFKSR_Print+Application11.pdf",
          "name": "G8OU2PE919PFKSR_Print Application11.pdf"
        }
      ],
      "selection_procedure_details_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FDZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_",
          "name": "DZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FN490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3",
          "name": "N490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3"
        }
      ],
      "company_name": "Make My Trip",
      "address": "MakeMyTrip India Pvt. Ltd.5, Awagarh House, MG Road(next to Bachoomal collections)Agra (UP), - 282002India",
      "company_type": "Private Sector",
      "nature_of_business": "Technology",
      "website": "www.makemytrip.com",
      "company_details": "This s a very nice company",
      "is_company_details_pdf": true,
      "city": "Mumbai",
      "state": "Maharashtra",
      "country": "India",
      "pin_code": 530013,
      "city_type": "Domestic",
      "designation": "Software Developer",
      "description": "very nice job",
      "is_description_pdf": true,
      "compensation_CTC": 1200000,
      "compensation_gross": 1100000,
      "compensation_take_home": 1000000,
      "compensation_bonus": 10000,
      "compensation_details": "very good compensation",
      "is_compensation_details_pdf": true,
      "bond_details": "nil",
      "selection_procedure_rounds": [
        "Resume Shortlisting",
        "Technical Interview",
        "HR Interview"
      ],
      "selection_procedure_details": "All rounds are complusory",
      "is_selection_procedure_details_pdf": true,
      "tier": "4",
      "tentative_date_of_joining": "2022-01-15",
      "allowed_batch": ["2018", "2019"],
      "allowed_branch": ["CSE", "EE"],
      "tentative_no_of_offers": 5,
      "other_requirements": "above 8 cpi",
      "additional_info": ["School", "Home Town"],
      "deadline_date": "2021-12-04",
      "created_at": "2021-12-02T20:12:21+05:30"
    }
  ],
  "placementApplication": [
    {
      "id": "LLW4STE76GEJYOR",
      "placement": {
        "id": "Q54IRZZMC3RP8F6",
        "company_details_pdf_links": [
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FI5U4RDTV0OP0EM0_2019+Student+Details+-+Total%28State+Sort%29+-+Copy.pdf",
            "name": "I5U4RDTV0OP0EM0_2019 Student Details - Total(State Sort) - Copy.pdf"
          },
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FW04JWWNNMIBX0JX_2019+Student+Details+-+Total%28State+Sort%29.pdf",
            "name": "W04JWWNNMIBX0JX_2019 Student Details - Total(State Sort).pdf"
          },
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FT1BXP98WBT9BHOR_AP0313017732021LL-Driving+Licence+-+Copy.pdf",
            "name": "T1BXP98WBT9BHOR_AP0313017732021LL-Driving Licence - Copy.pdf"
          }
        ],
        "description_pdf_links": [
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FC78TE2Z67BPZ41O_CSE-V-SEM.pdf",
            "name": "C78TE2Z67BPZ41O_CSE-V-SEM.pdf"
          }
        ],
        "compensation_pdf_links": [
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2F8D5OFQ46H43DD3S_module5And6Attendance.pdf",
            "name": "8D5OFQ46H43DD3S_module5And6Attendance.pdf"
          },
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FG8OU2PE919PFKSR_Print+Application11.pdf",
            "name": "G8OU2PE919PFKSR_Print Application11.pdf"
          }
        ],
        "selection_procedure_details_pdf_links": [
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FDZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_",
            "name": "DZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_"
          },
          {
            "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FN490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3",
            "name": "N490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3"
          }
        ],
        "company_name": "Make My Trip",
        "address": "MakeMyTrip India Pvt. Ltd.5, Awagarh House, MG Road(next to Bachoomal collections)Agra (UP), - 282002India",
        "company_type": "Private Sector",
        "nature_of_business": "Technology",
        "website": "www.makemytrip.com",
        "company_details": "This s a very nice company",
        "is_company_details_pdf": true,
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "pin_code": 530013,
        "city_type": "Domestic",
        "designation": "Software Developer",
        "description": "very nice job",
        "is_description_pdf": true,
        "compensation_CTC": 1200000,
        "compensation_gross": 1100000,
        "compensation_take_home": 1000000,
        "compensation_bonus": 10000,
        "compensation_details": "very good compensation",
        "is_compensation_details_pdf": true,
        "bond_details": "nil",
        "selection_procedure_rounds": [
          "Resume Shortlisting",
          "Technical Interview",
          "HR Interview"
        ],
        "selection_procedure_details": "All rounds are complusory",
        "is_selection_procedure_details_pdf": true,
        "tier": "4",
        "tentative_date_of_joining": "2022-01-15",
        "allowed_batch": ["2018", "2019"],
        "allowed_branch": ["CSE", "EE"],
        "tentative_no_of_offers": 5,
        "other_requirements": "above 8 cpi",
        "additional_info": ["School", "Home Town"],
        "deadline_date": "2021-12-04",
        "created_at": "2021-12-02T20:12:21+05:30"
      },
      "resume_link": "https://storage.googleapis.com/cdc-backend-attachments/resume/LLW4STE76GEJYOR%2F8KIOT3PW1JIS718_CSE-V-SEM.pdf",
      "additional_info": "{\"School\": \"Narayana English Medium High School\", \"Home Town\": \"Vizag\"}",
      "selected": null,
      "applied_at": "2021-12-02T21:58:18.032466+05:30"
    }
  ]
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- placements: Array of Placement Objects
- placementApplication: Array of Placement Application Objects

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Data Found`           |
| 404 Not Found   | `Student Not Found`    |
| 400 BAD_REQUEST | `Something Went Wrong` |

You can see some common errors [here](#common-errors)

---

## `api/student/addResume/`

This Api is used to add resumes by a student.

### How to Use?

Send a `POST` request to `api/student/addResume/`<br>

> Only users with `student` role can access this Api.

Request_Body:

```json
{
  "file": "__FILE_OBJECT__"
}
```

> Excepted to send Form Data

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Upload Resume",
  "message": "Resume Added"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes | Possible Messages |
| ------------ | ----------------- |
| 200 OK       | `Resume Added`    |

You can see some common errors [here](#common-errors)

---

## `api/student/deleteResume/`

This Api is used to delete resumes added by a student.

### How to Use?

Send a `POST` request to `api/student/deleteResume/`<br>

> Only users with `student` role can access this Api.

Request_Body:

```json
{
  "resume_file_name": "8ZJ44RIS9914SO4_Resume for Google STEP.pdf"
}
```

### Response

Response is a Json with these fields

```json
{
  "action": "Delete Resume",
  "message": "Resume Deleted"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes  | Possible Messages |
| ------------- | ----------------- |
| 200 OK        | `Resume Deleted`  |
| 404 NOT FOUND | `File Not Found`  |

You can see some common errors [here](#common-errors)

---

## `api/student/submitApplication/`

This Api is used to submit application to Placements.

### How to Use?

Send a `POST` request to `api/student/submitApplication/`<br>

> Only users with `student` role can access this Api.

Request_Body:

```json
{
  "opening_type": "Placement",
  "opening_id": "Q54IRZZMC3RP8F6",
  "resume_file_name": "8KIOT3PW1JIS718_CSE-V-SEM.pdf",
  "additional_info": {
    "School": "Narayana English Medium High School",
    "Home Town": "Vizag"
  }
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

- opening_type: Can be Placement
- opening_id: Opening Id unique to each opening.
- additional_info: This is the info which the Placement demands besides the normal user data which has to
  asked and sent. These fields can be found in the Placement Details.

### Response

Response is a Json with these fields

```json
{
  "action": "Submit Application",
  "message": "Application Submitted"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes  | Possible Messages                  |
| ------------- | ---------------------------------- |
| 200 OK        | `Application Submitted`            |
| 403 FORBIDDEN | `Application is already Submitted` |
| 403 FORBIDDEN | `Placement Not Approved`           |
| 404 NOT FOUND | `RESUME_FILE_NAME Not Found`       |

You can see some common errors [here](#common-errors)

---

# Admin Portal APIs

## `api/admin/markStatus`

This Api is used to mark the status for application for a specific placement.

### How to Use?

Send a `POST` request to `api/admin/markStatus`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6",
  "student_list": [
    {
      "student_id": "190010036",
      "student_selected": "true"
    },
    {
      "student_id": "190050022",
      "student_selected": "false"
    }
  ]
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Mark Status",
  "message": "Marked Status"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Marked Status`        |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/getDashboard`

This Api is used to get all the placements.

### How to Use?

Send a `GET` request to `api/admin/getdashboard`<br>

Request_Body:

```json
{}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Get Dashboard - Admin",
  "message": "Data Found",
  "new": [],
  "ongoing": [
    {
      "id": "Q54IRZZMC3RP8F6",
      "company_details_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FI5U4RDTV0OP0EM0_2019+Student+Details+-+Total%28State+Sort%29+-+Copy.pdf",
          "name": "I5U4RDTV0OP0EM0_2019 Student Details - Total(State Sort) - Copy.pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FW04JWWNNMIBX0JX_2019+Student+Details+-+Total%28State+Sort%29.pdf",
          "name": "W04JWWNNMIBX0JX_2019 Student Details - Total(State Sort).pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FT1BXP98WBT9BHOR_AP0313017732021LL-Driving+Licence+-+Copy.pdf",
          "name": "T1BXP98WBT9BHOR_AP0313017732021LL-Driving Licence - Copy.pdf"
        }
      ],
      "description_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FC78TE2Z67BPZ41O_CSE-V-SEM.pdf",
          "name": "C78TE2Z67BPZ41O_CSE-V-SEM.pdf"
        }
      ],
      "compensation_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2F8D5OFQ46H43DD3S_module5And6Attendance.pdf",
          "name": "8D5OFQ46H43DD3S_module5And6Attendance.pdf"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FG8OU2PE919PFKSR_Print+Application11.pdf",
          "name": "G8OU2PE919PFKSR_Print Application11.pdf"
        }
      ],
      "selection_procedure_details_pdf_links": [
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FDZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_",
          "name": "DZTQQ6YBGBQ47PY_screencapture-onlinesbi-sbi-sbicollect-fsssuccessresponseredirect-htm-2021-07-19-18_"
        },
        {
          "link": "https://storage.googleapis.com/cdc-backend-attachments/company_attachments/Q54IRZZMC3RP8F6%2FN490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3",
          "name": "N490PUXJEEN4JZ9_screencapture-onlinesbi-sbi-sbicollect-payment-suvidhapayment-htm-2021-07-19-23_12_3"
        }
      ],
      "company_name": "Make My Trip",
      "address": "MakeMyTrip India Pvt. Ltd.5, Awagarh House, MG Road(next to Bachoomal collections)Agra (UP), - 282002India",
      "company_type": "Private Sector",
      "nature_of_business": "Technology",
      "website": "www.makemytrip.com",
      "company_details": "This s a very nice company",
      "is_company_details_pdf": true,
      "contact_person_name": "Gowtham",
      "phone_number": 9390291911,
      "email": "saisurya3127@gmail.com",
      "city": "Mumbai",
      "state": "Maharashtra",
      "country": "India",
      "pin_code": 530013,
      "city_type": "Domestic",
      "designation": "Software Developer",
      "description": "very nice job",
      "is_description_pdf": true,
      "compensation_CTC": 1200000,
      "compensation_gross": 1100000,
      "compensation_take_home": 1000000,
      "compensation_bonus": 10000,
      "compensation_details": "very good compensation",
      "is_compensation_details_pdf": true,
      "bond_details": "nil",
      "selection_procedure_rounds": [
        "Resume Shortlisting",
        "Technical Interview",
        "HR Interview"
      ],
      "selection_procedure_details": "All rounds are complusory",
      "is_selection_procedure_details_pdf": true,
      "tier": "4",
      "tentative_date_of_joining": "2022-01-15",
      "allowed_batch": ["2018", "2019"],
      "allowed_branch": ["CSE", "EE"],
      "tentative_no_of_offers": 5,
      "other_requirements": "above 8 cpi",
      "additional_info": ["School", "Home Town"],
      "email_verified": false,
      "offer_accepted": null,
      "deadline_date": "2021-12-04",
      "created_at": "2021-12-02T20:12:21+05:30"
    }
  ],
  "previous": []
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- ongoing: Gives us the list of placements that are accepting applications.
- previous: Gives us the list of placements that stopped accepting applications.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Data Found`           |
| 400 BAD_REQUEST | `Something Went Wrong` |

You can see some common errors [here](#common-errors)

---

## `api/admin/updateDeadline`

This Api is used to update deadline for a specific placement.

### How to Use?

Send a `POST` request to `api/admin/updateDeadline`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6",
  "deadline_datetime": "2021-12-06 16:28:18 +0530"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Update Deadline",
  "message": "Deadline Updated"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Deadline Updated`     |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/updateOfferAccepted`

This Api is used to update offer verification state for a specific placement.

### How to Use?

Send a `POST` request to `api/admin/updateOfferAccepted`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6",
  "offer_accepted": "true"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Update Offer Accepted",
  "message": "Offer Accepted Updated"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages       |
| --------------- | ----------------------- |
| 200 OK          | `Update Offer Accepted` |
| 400 BAD_REQUEST | `Something Went Wrong`  |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/updateEmailVerified`

This Api is used to update email verification state for a specific placement.

### How to Use?

Send a `POST` request to `api/admin/updateEmailVerified`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6",
  "email_verified": "false"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Update Email Verified",
  "message": "Email Verified Updated"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Email Verified Updated` |
| 400 BAD_REQUEST | `Something Went Wrong`   |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/updateAdditionalInfo`

This Api is used to update additional_info for a specific placement.

### How to Use?

Send a `POST` request to `api/admin/updateAdditionalInfo`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6",
  "additional_info": ["School", "Place of Living", "Research Interests"]
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Update Additional Info",
  "message": "Additional Info Updated"
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages         |
| --------------- | ------------------------- |
| 200 OK          | `Additional Info Updated` |
| 400 BAD_REQUEST | `Something Went Wrong`    |

You may see some different errors which can be seen [here](#common-errors)

---

<!-- new branch -->

## `api/admin/getApplications`

This api is used to fetch all the applications applied by students for all placements

### How to Use?

Send a `POST` request to `api/admin/getApplications`<br>
Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Get Applications",
  "message": "Data Found",
  "applications": []
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Data Found`           |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/submitApplication`

This api is used to submit a students application

Request_Body:

```json
{
  "applications_id": "F28IRGGMC3RP8Y8",
  "student_id": "200010022",
  "opening_id": "Q54IRZZMC3RP8F6",
  "additional_info": {
    "School": "Lions International",
    "City": "Banglore"
  },
  "resume_file_name": "8KIOT3PW1JIS718_CSE-V-SEM.pdf"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Add Student Application",
  "message": "Application Added"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `Application Added`    |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/generateCSV`

This api is used to generate a CSV file that contains sequential details of all the applications

Request_Body:

```json
{
  "opening_id": "Q54IRZZMC3RP8F6"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Create CSV",
  "message": "CSV Created",
  "file": "csv_file_link"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `CSV created`          |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/addPPO`

This api is used to add a PPO for a student in the corresponding company

Request_Body:

```json
{
  "company_name": "Geeks for Geeks",
  "compensation_gross": "1000000",
  "offer_accepted": "true",
  "student_id": "200010022",
  "designation": "Technical Content Writer",
  "tier": "4"
}
```

### Response

Response is a Json with these fields

```json
{
  "action": "Add PPO",
  "message": "PPO Added"
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | `PPO Added`            |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

## `api/admin/getStudentApplication`

This api is used to fetch the application details of the required student

Request_Body:

```json
{
  "student_id": "200010022",
  "opening_id": "Q54IRZZMC3RP8F6"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

### Response

Response is a Json with these fields

```json
{
  "action": "Get Student Application",
  "application_found": "true",
  "application_info": {
    "id": "F28IRGGMC3RP8Y8",
    "additional_info": ,
    "resume": "resume_link"
  },
  "student_details": {
    "name": "John",
    "batch": "2020",
    "branch": "MMAE",
    "resume_list":
  }
}
```

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages      |
| --------------- | ---------------------- |
| 200 OK          | ``                     |
| 400 BAD_REQUEST | `Something Went Wrong` |

You may see some different errors which can be seen [here](#common-errors)

---

# Company Portal APIs

## `api/company/addPlacement/`

This Api is used to add placements.

### How to Use?

Send a `POST` request to `api/company/addPlacement`<br>

Request_Body:

```json
{
  "company_name": ["Make My Trip"],
  "address": [
    "MakeMyTrip India Pvt. Ltd.\n5, Awagarh House, MG Road\n(next to Bachoomal collections)\nAgra (UP), - 282002\nIndia"
  ],
  "company_type": ["Private Sector"],
  "nature_of_business": ["Technology"],
  "website": ["www.makemytrip.com"],
  "company_details": ["This s a very nice company"],
  "is_company_details_pdf": ["true"],
  "contact_person_name": ["Gowtham"],
  "phone_number": ["9390291911"],
  "email": ["saisurya3127@gmail.com"],
  "city": ["Mumbai"],
  "state": ["Maharashtra"],
  "country": ["India"],
  "pincode": ["530013"],
  "designation": ["Software Developer"],
  "description": ["very nice job"],
  "is_description_pdf": ["true"],
  "compensation_ctc": ["1200000"],
  "compensation_gross": ["1100000"],
  "compensation_take_home": ["1000000"],
  "compensation_bonus": ["10000"],
  "compensation_details": ["very good compensation"],
  "is_compensation_details_pdf": ["true"],
  "bond_details": ["nil"],
  "selection_procedure_rounds": [
    "['Resume Shortlisting', 'Technical Interview', 'HR Interview']"
  ],
  "selection_procedure_details": ["All rounds are complusory"],
  "is_selection_procedure_details_pdf": ["true"],
  "tentative_date_of_joining": ["15-01-2022"],
  "allowed_branch": ["['CSE', 'EE']"],
  "tentative_no_of_offers": ["5"],
  "other_requirements": ["above 8 cpi"],
  "company_details_pdf": ["__FILE_OBJECT__", "__FILE_OBJECT__"],
  "description_pdf": ["__FILE_OBJECT__"],
  "compensation_details_pdf": ["__FILE_OBJECT__"],
  "selection_procedure_details_pdf": ["__FILE_OBJECT__", "__FILE_OBJECT__"]
}
```

### Response

Response is a Json with these fields

```json
{
  "action": "Add Placement",
  "message": "Placement Added Successfully"
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.

### Status Codes

The possible responses for this api request are as follows

| Status Codes  | Possible Messages              |
| ------------- | ------------------------------ |
| 200 OK        | `Placement Added Successfully` |
| 404 NOT FOUND | `Something went wrong`         |

You can see some common errors [here](#common-errors)

---

## `Common Errors`

Some common errors that you may see while accessing the Apis

| Status Codes     | Possible Messages                                        | Possible Reasons                                                                             |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 401 UNAUTHORIZED | `Authorization Header Not Found`                         | Check for the authorization header in you request and the prefix( Should use `Bearer`) used. |
| 401 UNAUTHORIZED | `Access Denied. You are not allowed to use this service` | Your may not have required access to those access those Apis.                                |
| 401 UNAUTHORIZED | `Token has wrong audience`                               | You may be using wrong credentials for Google OAuth2.0.                                      |
| 404 NOT FOUND    | `User Not Found. Contact CDC for more details`           | You may not be a user at CDC, IIT Dharwad. Please contact us to get your user account        |
| 400 BAD_REQUEST  | `Error Occurred`                                         | Any random Error which can be seen in the {error} string.                                    |
| 400 BAD_REQUEST  | `Something went wrong`                                   | Any random Error which can be seen in the {error} string.                                    |
