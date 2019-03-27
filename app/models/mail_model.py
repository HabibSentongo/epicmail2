class StaticStrings:
    error_empty = 'No records yet!'
    error_missing = 'No such record'
    error_bad_data = 'Provide correct details'
    error_no_id = 'We can\'t identify you, Signin first'
    msg_deleted = 'Record has been deleted'
    error_savemode = 'You must send the email or save it as draft'
    error_missdestination = 'destination address is missing'
    error_email_exist = 'This email is already associated with another account'
    single_id_selector = "SELECT {} FROM {} WHERE {} = {};"
    two_id_selector = "SELECT * FROM {} WHERE {} = {} AND ({} = {} OR {} = {});"
    single_selector = "SELECT * FROM {} WHERE {} = '{}';"
    selector = "SELECT * FROM {} WHERE {} = {} AND {} = '{}';"
    two_string_selector = "SELECT * FROM {} WHERE {} = '{}' AND {} = '{}';"
    create_email = "INSERT INTO emails(subject, parent_message_id, sender_status, sender_id, reciever_id, reciever_status, message_details)\
    VALUES ('{}',{},'{}',{},{},'{}','{}') RETURNING *;"
    create_user = "INSERT INTO users(email_address, first_name, last_name, password)\
    VALUES ('{}','{}','{}','{}') RETURNING user_id;"
    updater = "UPDATE {} SET {} = '{}' WHERE {} = {};"
    deleter = "DELETE FROM {} WHERE {} = {};"
    create_group = "INSERT INTO groups(group_name, admin, members)\
    VALUES ('{}',{},array{}) RETURNING *"
