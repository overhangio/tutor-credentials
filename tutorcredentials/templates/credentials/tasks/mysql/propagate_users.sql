INSERT credentials.core_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, full_name, lms_user_id)
     SELECT     lms_user.password,
               lms_user.last_login,
               lms_user.is_superuser,
               lms_user.username,
               lms_user.first_name,
               lms_user.last_name,
               lms_user.email,
               lms_user.is_staff,
               lms_user.is_active,
               lms_user.date_joined,
               CASE WHEN NOT ISNULL(lms_profile.name) THEN lms_profile.name ELSE lms_user.first_name + ' ' + lms_user.last_name END as full_name,
               lms_user.id as lms_user_id
     FROM     openedx.auth_user lms_user
               LEFT JOIN openedx.auth_userprofile as lms_profile ON (lms_user.id = lms_profile.user_id)
               LEFT JOIN credentials.core_user credentials_user ON (lms_user.id = credentials_user.lms_user_id)
               LEFT JOIN credentials.core_user credentials_user2 ON (lms_user.username = credentials_user2.username)
     WHERE     (credentials_user.id IS NULL) AND
               (credentials_user2.username IS NULL);
