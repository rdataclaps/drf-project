# drf-project

http://127.0.0.1:8000/api/user/register/   ->By using this api we will be able to create a new user for that we need to give the email, name, tc(True or False) fields and than it will create a new user and provide access_token and refresh_token


http://127.0.0.1:8000/api/user/login/ ->This api will login the user if account is already created for that we need to give the correct email and password.If email or password anything is wrong than it will give the error. And this api also give the access_token and refresh_token


http://127.0.0.1:8000/api/user/register/  -> This api will provide the user profile by the access_token.


http://127.0.0.1:8000/api/user/change_password/ ->By using this api we will be able to change the password if we know the current password, for that we need to give the old_password,new_password,confirm_new_password


http://127.0.0.1:8000/api/user/send_reset_password_email/ ->This api is responsible to send the email. Where uid and token is provided to reset the password if we forgot the previos password.


http://127.0.0.1:8000/api/user/reset_password/<uid>/<token>/  ->By using this api we will be able to change the password if we forgot the previous password because we got the uid and token in email by providing the uid and token the password will reset.