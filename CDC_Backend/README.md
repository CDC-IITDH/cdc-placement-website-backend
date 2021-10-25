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
4. [**Common Errors**](#common-errors)

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
    "user_type": [
        "student"
    ]
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
        "id": "fdgdb",
        "roll_no": 190010036,
        "name": "Gowtham Sai",
        "batch": "THIRD",
        "branch": "CSE",
        "phone_number": 9390291911,
        "resumes": [
           "XB85F4RIGBF5VJN_Cv-Gowtham.pdf"
        ],
        "cpi": "9.02"
    }
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- details: Has the student data.

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Details Found`          |
| 400 BAD_REQUEST | `Error Occurred {error}` | 

You may see some different errors which can be seen [here](#common-errors)

---

## `api/student/getDashboard`

This Api is used to get all the placements applicable to the student.

### How to Use?

Send a `GET` request to `api/student/Dashboard`<br>

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
    "action": "Placement and Internships",
    "message": "Data Found",
    "placements": [
        {
            "id": "fdgdb121",
            "designation": "Software Developer",
            "description": "nice job",
            "start_date": "2021-06-17",
            "city": "Mumbai",
            "city_type": "Domestic",
            "compensation": 1200000,
            "compensation_details": "",
            "allowed_batch": [
                "THIRD",
                "FOURTH"
            ],
            "allowed_branch": [
                "CSE",
                "EE",
                "ME"
            ],
            "attachments": [],
            "rounds": [
                "Resume Shortlisting",
                "Technical Test",
                "Interview"
            ],
            "additional_info": [
                "school",
                "place of study",
                "language"
            ],
            "status": "Resume Shortlisting",
            "rounds_details": {
                "Interview": "One -to-One interview",
                "Technical Test": "Online Technical test which will be monitored remotely",
                "Resume Shortlisting": "Resume will be seen"
            },
           "company_details": {
                "id": "fdgdb",
                "name": "Apple",
                "address": "California",
                "companyType": "Technology",
                "website": ""
            }
        }
    ],
    "placementApplication": [
        {
            "id": "dsdads",
            "application_status": "Resume Shortlisting",
            "resume": "XB85F4RIGBF5VJN_Cv-Gowtham.pdf",
            "additional_info": {
                "school": "Delhi Public School",
                "language": "Telugu",
                "place of study": "Visakhapatnam"
            },
            "selected": null,
            "placement": "fdgdb121"
        }
    ]   
}
```

- action: Tells us about the message creator<Br>
- message: Tells us what happened with our Request.
- placements: Has the placements data.
- internships: Has the internships data.
- application_status: Can have many names
  - Accepting Applications
  - One of the Round Names
  - Completed
- selected: Can take three Values
  - null: Student is still in the Selection process
  - true: Student is Selected
  - false: Student is not selected

### Status Codes

The possible responses for this api request are as follows

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ | 
| 200 OK          | `Resume Added`           |
| 400 BAD_REQUEST | `Error Occurred {error}` |

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

This Api is used to submit application to Internships/Placements.

### How to Use?

Send a `POST` request to `api/student/submitApplication/`<br>

> Only users with `student` role can access this Api.

Request_Body:

```json
{
  "opening_type": "Placement",
  "opening_id": "fgervsdgdsf",
  "resume_file_name": "1FYE0PQZZ508HR6_Resume for Google STEP.pdf",
  "additional_info": {
    "school": "Narayana English Medium",
    "place of study": "Vizag",
    "language": "Telugu"
  }
}
```

> Headers <br>
> Authorization: "Bearer {tokenID}"

- opening_type: Can be Placement/Internship
- opening_id: Opening Id unique to each opening.
- additional_info: This is the info which the Internship/Placement demands besides the normal user data which has to
  asked and sent. These fields can be found in the Internship Details.

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
  "opening_id": "RIDNK323JD3JD",
  "student_list": [
    "DBJDH32JDDDRE",
    "HFJGJHE7JGDHE"
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

| Status Codes    | Possible Messages        |
| --------------- | ------------------------ |
| 200 OK          | `Marked Status`          |
| 400 BAD_REQUEST | `Error Occurred` | 

You may see some different errors which can be seen [here](#common-errors)

---

## `Common Errors`

Some common errors that you may see while accessing the Apis

| Status Codes     | Possible Messages                                        | Possible Reasons                                                                             |
| ---------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 401 UNAUTHORIZED | `Authorization Header Not Found`                         | Check for the authorization header in you request and the prefix( Should use `Bearer`) used. |
| 401 UNAUTHORIZED | `Access Denied. You are not allowed to use this service` | Your may not have required access to those access those Apis.                                |
| 401 UNAUTHORIZED | `Token has wrong audience`                               | You may be using wrong credentials for Google OAuth2.0.                                      |
| 404 NOT FOUND    | `User Not Found. Contact CDC for more details`           | You may not be a user at CDC, IIT Dharwad. Please contact us to get your user account        |
| 400 BAD_REQUEST  | `Error Occurred {error}`                                 | Any random Error which can be seen in the {error} string.                                    |


