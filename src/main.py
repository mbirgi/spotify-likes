import spotify
import utils

# login
sp = spotify.login(
    scope='playlist-read-private playlist-modify-private user-library-read'
)
user = sp.current_user()

# check login success:
# displayName = user['display_name']
# print(displayName)