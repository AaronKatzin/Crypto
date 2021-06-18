import twint

def getFollowers(username):
    """"TODO: add error handling in case username doesn't exist"""
    c = twint.Config()
    c.Username = username
    c.Store_object= True
    c.Hide_output = True
    c.Format = "ID {id} | Username {username} | Followers {followers}"
    twint.run.Lookup(c)
    return twint.output.users_list[0].followers