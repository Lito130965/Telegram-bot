from behave import given, when, then


@given('a new discovered user')
def step_given_new_user(context):
    context.user = {'id': '4444'}


@given('i have one user in database')
def step_given_one_user(context):
    try:
        context.db + [{'id': '0000'}]
    except:
        context.db = [{'id': '0000'}]


@given('i have three users in database')
def step_given_three_users(context):
    try:
        context.db + [{'id': '1111'}, {'id': '2222'}, {'id': '3333'}]
    except:
        context.db = [{'id': '1111'}, {'id': '2222'}, {'id': '3333'}]


@when('bot adding user to a database')
def step_when_user_to_db(context):
    context.db.append(context.user)


@when('user set new emoji')
def step_when_user_set_emoji(context):
    context.db[0]['emoji'] = 'N'


@when('bot getting documents from database')
def step_when_getting_all_docs(context):
    context.docs = context.db


@when("bot getting user's id from database")
def step_when_getting_all_ids(context):
    context.ids = [user['id'] for user in context.db]


@then('i should have four users in database')
def step_then_four_users_in_db(context):
    assert len(context.db) == 4


@then('user emoji should be changed')
def step_then_new_emoji(context):
    assert context.db[0]['emoji'] == 'N'


@then('i should have list with len equals three')
def step_then_three_users_in_db(context):
    assert len(context.db) == 3


