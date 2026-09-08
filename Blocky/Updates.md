# Blocky Updates

A running record of recent features, fixes, patches, and deployment notes.

## 2026-09-07

### 22:31:57 -11:00 | Supabase schema prepared

- Added `backend/supabase_schema.sql`.
- Documented the complete PostgreSQL schema for the current application.
- Included the following tables:
  - `items`
  - `users`
  - `auth_sessions`
  - `login_attempts`
  - `lesson_progress`
- Added primary keys, foreign keys, unique constraints, defaults, and indexes.
- Added cascade deletion from users to sessions and lesson progress.
- Confirmed that the schema is ready to run in the Supabase SQL Editor.

**Database status:** The schema has been created in Supabase by the project owner. Flask migrations have not been run against the Supabase database yet.

### 22:20 | Authentication and session hardening

- Added Flask authentication using server-side sessions.
- Added secure password hashing with Werkzeug.
- Added generated development secret support using Python's `secrets` module.
- Added persistent session tracking with:
  - Session ID
  - User ID
  - Creation time
  - Last activity time
  - Expiry time
  - IP address
  - User agent
  - Revocation time
- Added session restoration after frontend reloads.
- Added active session listing through `GET /api/auth/sessions`.
- Added logout session revocation.

### 22:10 | Login protection patch

- Added database-backed failed-login tracking.
- Limited failed login attempts to five per hour for each email and IP address pair.
- Added HTTP `429` responses after the limit is reached.
- Kept the limit configurable through backend configuration constants.
- Verified the behavior with isolated backend tests:
  - First five failed attempts return `401`.
  - The next failed attempt returns `429`.

### 22:00 | Learning progress and points

- Added persistent lesson completion records.
- Added one point for each unique completed lesson.
- Prevented duplicate lesson completions from awarding duplicate points.
- Added progress endpoint:
  - `GET /api/auth/progress`
- Added completion endpoint:
  - `POST /api/auth/lessons/<lesson_id>/complete`
- Connected the frontend roadmap to the backend progress system.
- Added progress restoration when the SQL learning page opens.

### 21:50 | Settings and profile customization

- Added the settings page with square section panels for:
  - Profile
  - Privacy
  - Points
  - Lessons completed
  - Appearance
- Added display name updates.
- Added profile picture uploads through Flask.
- Limited profile pictures to 2 MB.
- Supported PNG, JPEG, and WebP uploads.
- Stored profile pictures in the database as binary data.
- Added theme preferences:
  - Paper/light
  - Dark
  - Red and white
  - Blue and white
  - Black and white
- Added theme persistence through the backend.

### 21:35 | SQL learning roadmap

- Reworked the SQL learning page into a roadmap-style experience.
- Added connected lesson nodes and completion states.
- Added lessons for:
  - `SELECT`
  - `WHERE`
  - `JOIN`
  - `GROUP BY`
- Added query examples and result previews.
- Added a no-reload completion animation.
- Added progress and points display.
- Added a PostgreSQL Windows x64 setup guide.

### 21:20 | Visual membership plans

- Added a frontend-only plans page at `#plans`.
- Added Free tier:
  - Free for 5 days
  - Foundation SQL lessons
  - Basic roadmap access
  - Progress and points tracking
- Added Standard tier at `£5.99` per month:
  - Advanced roadmaps
  - Expanded SQL exercises
  - Progress insights
- Added Gold tier at `£10.99` per month:
  - Advanced roadmaps
  - Isolated test environments
  - Project-based practice
  - Priority feature access
- Added responsive pricing cards and a highlighted Standard tier.
- No payment provider or payment backend has been connected yet.

### 21:00 | Frontend maintenance cleanup

- Split the frontend into maintainable components:
  - `App.jsx`
  - `SQLLearning.jsx`
  - `Settings.jsx`
  - `Plans.jsx`
- Reorganized the stylesheet into grouped sections.
- Added small comments only for non-obvious layout behavior.
- Removed unnecessary inline complexity and decorative symbols.
- Added direct hash navigation for:
  - `#sql`
  - `#settings`
  - `#plans`

## Validation completed today

- React lint passed.
- React production build passed.
- Python compilation passed.
- Backend diagnostics passed for edited source files.
- Auth signup and login passed.
- Session tracking passed.
- Logout and session clearing passed.
- Lesson points and duplicate-completion protection passed.
- Theme update passed.
- Profile picture upload passed.
- Supabase schema formatting and project diff checks passed.

## Pending deployment task

Run the Flask migration command only after confirming the Supabase connection string and password are valid:

```powershell
cd backend
flask --app app.app:create_app db upgrade
```

Because `backend/supabase_schema.sql` already describes the current schema, do not run both the full SQL schema script and the initial Flask migrations against the same empty Supabase database unless the migration history is intentionally coordinated.
