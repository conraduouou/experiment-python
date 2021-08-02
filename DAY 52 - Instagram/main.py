from instagramBot import InstaFollower

# Extra account to use
username = "keyfreelancing"
password = "Godreallylovesme"

# account to follow from
similar_account = "davidjmalan"

bot = InstaFollower(username)

bot.login(password)
bot.unfollow()