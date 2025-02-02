# Secure Flask Bootstrap PWA Template

This Flask template has been built from the ground up to be a secure Progressive Web App. It includes a secure form and Bootstrap sample components ready to be connected to a SQLite3 database. All minimum PWA standards have been integrated, and placeholder images have been provided for all the icon and image components.

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
Test Email:
Test Password:



## Privacy advice for developers

- The app should have a privacy handling policy
- Only data essential for the app should be collected
- Users should be given the option to download or delete their data
- Passwords should be encrypted, including a salt, before hashing

## Security advice for developers

- All inputs should be sanitised before processing or storing
- If including login, authentication and session management should be implemented
- SSL Encryption and HTTPS should be implemented
- Use Jinga2 components when passing variables to the frontend
- Use query parameters for all SQL queries

## Content advice for developers

- All templates are [Bootstrap 5.3](https://getbootstrap.com/) ready
- [SQLite](https://docs.python.org/3/library/sqlite3.html) has been provided for database design

> [!TIP]
> Developers should [monitor Bootstrap 5.3.3 for discovered vulnerabilities](https://security.snyk.io/package/npm/bootstrap) and patch or update as needed.

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
