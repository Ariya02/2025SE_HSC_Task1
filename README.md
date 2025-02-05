# Software Developer Diary - "DevNotes"

This progressive web app is for software developers and teams to securely log the progress of their projects. The PWA is developed as part of a HSC Software Engineering Assignment Task 1 2025. Below outlines the dependencies, security features, specifications for the PWA and User Instructions. 

## Dependencies

- VSCode or GitHub Codespaces (preconfigured for docker)
- Python 3+
- pip install Flask
- pip install SQLite3
- pip install bcrypt
- pip install flask_wtf

## Secure Features

- Strict Content Security Policy
  - No inline `<script></script>`.
  - Restricted `<iframe>` loading
  - CORS JS blocked
- HTML Languaged declared.
- Meta character set declared.
- Private folders use .folderName syntax.
- [Bootstrap 5.3](https://getbootstrap.com/) components served local files.
- CSRFProtect applied to form.
- Form Pattern expression declared.

## User Instructions 

### Set up Environment
1. Launch Codespaces

![Codespace Launch](https://github.com/user-attachments/assets/81fd8418-76a3-4dd1-ba66-739e4448556e)
2. Once codespaces has been launched, in the terminal input:
``` python main.py ```

![Main py ](https://github.com/user-attachments/assets/30ef89c1-fe01-425f-8a37-9d7c6ad019c5)

3. Open the application in a browser for a better view

![Open in Browser](https://github.com/user-attachments/assets/077c9e39-90fa-4779-907f-f571f61918af)

-------------------------------------------------------------------------------------------------------
### Login 
Test Email: admin.user@gmail.com

Test Password: Adminuser1
1. Input the login details above into the email and password fields then click 'Login'

![Login](https://github.com/user-attachments/assets/06e8126b-fd7f-4411-97b1-386cbb36c534)
-------------------------------------------------------------------------------------------------------
### Submit Diary Entry and View

#### Test Data

   **Project Name:** Test My Project
   
   **Summary:** Testing First Submission
   
   **Programming Language:** Other

   **Date & time:** Use current date and time

   **Description:** Testing submission of diary entry for marking
   
1. Homepage - input test data and click submit
   
![Homepage](https://github.com/user-attachments/assets/ff6eb924-e80d-4bde-a44b-cdd803b687a5)

2. Redirect to 'All Entries' page on click

![All diary entries](https://github.com/user-attachments/assets/d77ba309-6a41-4f88-b6ed-dc7c27799a75)

3. To search through specific entry

![Search Entry Nav](https://github.com/user-attachments/assets/4d408ee6-f617-4752-8656-06c1e854f92d)

4. Use today's date in the date field and click enter to see the diary entry from today

![Search Entry](https://github.com/user-attachments/assets/f5c090d8-ae0a-4c1d-b9cd-99f06b22c7a8)
If you would like to see other entries try search: 
```Project Name: My First Project```
```Developer Name: Jane Smith```

### Profile

Go to profile to view user's first name, last name, email and diary entries published by the current user logged in. 

![Profile](https://github.com/user-attachments/assets/008d2306-6703-4df4-9547-2af5812ea6cc)

### Privacy Policy 

To view privacy policy, click on profile and a dropdown menu should show the a button that navigates to the privacy policy page.

![Privacy Policy nav](https://github.com/user-attachments/assets/1cb62cbd-c514-41ef-97cc-d816b562cf3d)
![Privacy policy](https://github.com/user-attachments/assets/7dc94d31-d07c-4886-bbae-0dd4acc25e6b)

### Logout 

![Logout](https://github.com/user-attachments/assets/d2ad55b8-d4de-49c6-ac2a-1cfc7cc2e084)

### Signup Testing

To test the signup implementation, follow the instructions below using the following test data:

**Email:** person1.test@gmail.com

**First name:** Person 1

**Last name:** Test

**Password:** Testlogin1

1. On the login page, click the 'sign up' link where you will be redirected to the signup page. If you are still currently logged in, log out from that user which will navigate you to the login page.

![Signup nav](https://github.com/user-attachments/assets/6fe756bb-2a4b-496e-bc1c-a946e407d874)

2. On the signup page, input the test data into the required fields

![image](https://github.com/user-attachments/assets/31b9fbd6-7557-4d9d-bf11-c7295d26c09b)

------------------------------------------------------------------------------------------------------------------------
## Senior Software Engineer Requirements/Specifications

1. Security evident in all phases of the software development lifecycle
2. Ability for new team members to self-sign up
3. Authentication and session management
4. Developer log entries are time/date stamped
5. Application meets minimum WC3 PWA standards
6. Allow developers to search entries by developer, date, project or log/diary contents
7. The app is modelled using: Level 0 data flow diagram, Structure chart & Data dictionary
8. Optional: API data sharing and 2FA authentication

## Junior Software Engineer Specifications

### General

- Sorting mechanism
- Component that allows for filtering through desired diary entries
- Title and description (brief summary) in each diary entry
- Security features
- Intuitive UI

### Aesthetics

- Dark/light mode option
- Nav bar
- Customisable theme
- Encryption of personal information
