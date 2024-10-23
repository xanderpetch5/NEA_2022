import time

from UI import *
import pygame
import sys
import dataGathering
import login
from PIL import Image
import requests


def gather_data(name, choice, username):
    df = login.Database("usernames.db")
    new_history = df.fetch_history(username)
    match choice:
        case "Artist":
            artist = dataGathering.Artist(name)
            new_history += f"{choice}: {artist.get_name()}, "
            return artist
        case "Album":
            album = dataGathering.Album(name)
            new_history += f"{choice}: {album.get_name()}, "
            return album
        case "Song":
            song = dataGathering.Song(name, "name")
            new_history += f"{choice}: {song.get_track_name()}, "
            return song
    df.update_history(username, new_history)
    df.close_database()


def is_password_valid(password):  # 48-57, 65-122
    if len(password) < 4: return False
    for letter in password:
        char = ord(letter)
        if not ((48 <= char <= 57) or (65 <= char <= 90) or (97 <= char <= 122)):
            return False
    return True


def run():
    base_font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    ui_state = 8

    username = ''
    # ENTER MUSIC STATE
    box = TextBox(280, 100, 400, "Enter Query")
    dropdown = DropDown(420, 150, 32, 120, "Toggle", ['Song', 'Artist', 'Album'])
    enter_box = Button(700, 100, 32, 100, "Enter")
    nav_bar = Nav_Bar(['Search', 'User Settings', 'Find Similar'], 175)
    # LOGIN STATE
    username_box = TextBox(280, 50, 400, "Enter Username")
    password_box = PasswordBox(280, 100, 400, "Enter Password")
    login_box = Button(280, 200, 32, 100, "Login")
    sign_up_box = Button(400, 200, 32, 100, "Sign Up")
    login_result_timer = 0

    result = 0  # the result of the user entered details
    # USER SETTINGS
    sign_out_button = Button(750, 50, 80, 200, "Sign Out")
    delete_acc_button = Button(750, 150, 80, 200, "Delete Account")
    clear_history_button = Button(35, 50, 80, 200, "Clear History")
    username_text = Text(280, 50, 'placeholder username', 40, 400, 40)
    user_history_text = Text(280, 110, "User History", 32, 160, 40)
    user_history = Text_Info_Box("placeholder user history", 280, 150, 395, 325)
    password_delete = PasswordBox(750, 250, 200, "Enter Password")
    change_pass_button = Button(750, 300, 80, 200, "Change Password")
    new_change_password = PasswordBox(750, 400, 200, "New Password")
    old_password = PasswordBox(750, 450, 200, "Old Password")
    yes_button = Button(260, 350, 100, 100, "Yes")
    no_button = Button(385, 350, 100, 100, "No")
    delete = False

    # ALBUM RESULTS
    bar_charts = [BarChart(400, 225, 75, 100, 'Acousticness', 100, 75),
                  BarChart(400, 375, 75, 100, 'Speechiness', 100, 75),
                  BarChart(545, 225, 75, 100, 'Loudness', 100, 75), BarChart(545, 375, 75, 100, 'Tempo', 100, 75),
                  BarChart(690, 225, 75, 100, 'Valence', 100, 75),
                  BarChart(690, 375, 75, 100, 'Instrumentalness', 100, 75),
                  BarChart(835, 225, 75, 100, 'Danceability', 100, 75), BarChart(835, 375, 75, 100, 'Energy', 100, 75)]
    album_name_text = Text(400, 50, 'placeholder album', 40, 500, 45)
    album_artist_text = Text(400, 110, 'placeholder artist', 32, 250, 42)
    maxes = [1, 1, 60, 240, 1, 1, 1, 1]
    album_info_box = Text_Info_Box("placeholder album info", 45, 315, 255, 200)
    album_info_box.font_size = 20
    album_name, artist_name = "placholder", "placholder"
    # ARTIST RESULTS
    artist_name_text = Text(180, 55, "placeholder artist", 40, 765, 45)
    artist_bio_text = Text_Info_Box("placholder artist bio", 180, 110, 530, 420)
    top_songs_text = Text_Info_Box("placeholder top songs", 730, 110, 210, 185)
    similar_artists_text = Text_Info_Box("placeholder artists", 730, 300, 210, 230)
    # SONG RESULTS
    song_name_text = Text(300, 50, "placeholder song name", 40, 645, 40)
    song_artist_text = Text(300, 100, "placeholder artist name", 30, 345, 30)
    offsetx = 100
    offsety = 50
    song_bar_charts = [BarChart(400 - offsetx, 225 - offsety, 75, 100, 'Acousticness', 100, 75),
                       BarChart(400 - offsetx, 375, 75, 100, 'Speechiness', 100, 75),
                       BarChart(545 - offsetx, 225 - offsety, 75, 100, 'Loudness', 100, 75),
                       BarChart(545 - offsetx, 375, 75, 100, 'Tempo', 100, 75),
                       BarChart(690 - offsetx, 225 - offsety, 75, 100, 'Valence', 100, 75),
                       BarChart(690 - offsetx, 375, 75, 100, 'Instrumentalness', 100, 75),
                       BarChart(835 - offsetx, 225 - offsety, 75, 100, 'Danceability', 100, 75),
                       BarChart(835 - offsetx, 375, 75, 100, 'Energy', 100, 75)]
    song_info_box = Text_Info_Box("placeholder song info", 45, 245, 205, 250)
    song_info_box.font_size = 20
    # FIND SIMILAR SONG
    similar_text_box = TextBox(280, 100, 400, "Enter Song")
    similar_enter_box = Button(700, 100, 32, 100, "Enter")

    # SIMILAR RESULTS
    song_boxes = [Song_Result(20, 50, "Song1", "Artist", "album1.png"),
                  Song_Result(20, 160, "Song2", "Artist", "album2.png"),
                  Song_Result(20, 270, "Song3", "Artist", "album3.png"),
                  Song_Result(20, 380, "Song4", "Artist", "album4.png")]
    #NOT CONNECTED
    not_connected = Text(000,200,"Not Connected to the Internet, Will Redirect When Connection is Back",40,0,0)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # LOGIN STATE
            # ------------------------------------------
            if ui_state == 0:
                username_box.handle_event(event)
                password_box.handle_event(event)
                login_box.handle_event(event)
                sign_up_box.handle_event(event)
                if (password_box.user_text != ''):
                    if (username_box.user_text != ''):
                        if login_box.pressed:
                            df = login.Database("usernames.db")
                            if df.check_credentials(username_box.user_text, password_box.user_text):
                                username = username_box.user_text
                                username_text.text = f"Username: {username}"
                                user_history.lines = [substring.strip(",") for substring in
                                                      df.fetch_history(username).split(", ")]
                                username_box.user_text = ''
                                password_box.user_text = ''
                                ui_state = 1
                            else:
                                result = 1
                            df.close_database()
                        if sign_up_box.pressed:
                            df = login.Database("usernames.db")
                            if df.check_repeat(username_box.user_text):
                                result = 2
                            else:
                                username = username_box.user_text
                                if is_password_valid(username):
                                    if not is_password_valid(password_box.user_text):
                                        result = 9
                                    else:
                                        df.add_user(username, password_box.user_text)
                                        result = 3
                                else:
                                    result = 8
                            df.close_database()
                            username_box.user_text = ''
                            password_box.user_text = ''
                    else:
                        if login_box.pressed or sign_up_box.pressed:
                            result = 12
                else:
                    if login_box.pressed or sign_up_box.pressed:
                        result =12
            # ------------------------------------------
            # ENTER MUSIC STATE
            elif ui_state == 1:
                box.handle_event(event)
                dropdown.handle_event(event)
                enter_box.handle_event(event)
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change

                if box.user_text != '' and enter_box.pressed:
                    choice = dropdown.selected_option
                    last_ouput = box.user_text
                    if choice is not None:
                        df = login.Database('usernames.db')
                        user_history_str = df.fetch_history(username)
                        user_history_str += f"{choice}: {box.user_text}, "
                        df.update_history(username, user_history_str)
                        user_history.lines = [substring.strip(",") for substring in
                                              df.fetch_history(username).split(", ")]
                        df.close_database()
                        try:
                            music_data = gather_data(last_ouput, choice, username)
                        except:
                            result = 10
                            break
                        if choice == 'Album':

                            album_name = music_data.get_name()
                            artist_name = music_data.get_artist()
                            dataGathering.get_image_png(music_data.get_album_image(), 'image.png')
                            mean_audio_features = music_data.get_average_features()
                            feature_map = {"Acousticness": 0, "Speechiness": 1, "Loudness": 2, "Tempo": 3, "Valence": 4,
                                           "Instrumentalness": 5, "Danceability": 6, "Energy": 7}

                            for i in bar_charts:
                                index = feature_map.get(i.text)
                                if index is not None:
                                    i.bar_value = mean_audio_features[index]
                                    i.bar_max = maxes[index]

                            album_info_box.get_lines(music_data.format_info())
                            ui_state = 3
                        # USER CHOOSES ARTIST
                        if choice == 'Artist':
                            artist_name_text.text = music_data.get_name()
                            artist_bio_text.get_lines(music_data.find_intro_paragraphs())
                            img_urls = music_data.get_album_imgs()
                            image = Image.open("noAlbumFound.png")
                            for i in range(1, 4):
                                if i > 3:
                                    image.save(f"album{i}.png")
                            for count, i in enumerate(img_urls):
                                dataGathering.get_image_png(i, f"album{count + 1}.png")
                            top_songs_text.get_lines(f"Top songs: {music_data.get_top_song()}")
                            similar_artists_text.get_lines(f"Similar Artists: {music_data.similar_artists()}")
                            ui_state = 4
                        if choice == 'Song':
                            song_bar_charts = [BarChart(400 - offsetx, 225 - offsety, 75, 100, 'Acousticness', maxes[0],
                                                        music_data.get_acousticness()),
                                               BarChart(400 - offsetx, 375, 75, 100, 'Speechiness', maxes[1],
                                                        music_data.get_speechiness()),
                                               BarChart(545 - offsetx, 225 - offsety, 75, 100, 'Loudness', maxes[2],
                                                        music_data.get_loudness() + 60),
                                               BarChart(545 - offsetx, 375, 75, 100, 'Tempo', maxes[3],
                                                        music_data.get_tempo()),
                                               BarChart(690 - offsetx, 225 - offsety, 75, 100, 'Valence', maxes[4],
                                                        music_data.get_valence()),
                                               BarChart(690 - offsetx, 375, 75, 100, 'Instrumentalness', maxes[5],
                                                        music_data.get_instrumentalness()),
                                               BarChart(835 - offsetx, 225 - offsety, 75, 100, 'Danceability', maxes[6],
                                                        music_data.get_danceability()),
                                               BarChart(835 - offsetx, 375, 75, 100, 'Energy', maxes[7],
                                                        music_data.get_energy())]
                            song_name_text.text = music_data.get_track_name()
                            song_artist_text.text = music_data.get_artist_name()
                            song_info_box.lines = music_data.format_string_data()

                            try:
                                music_data.get_album_image()
                                image = pygame.image.load("album1.png")
                            except:
                                image = pygame.image.load("noAlbumFound.png")

                            ui_state = 5
            # USER SETTINGS STATE
            elif ui_state == 2:
                sign_out_button.handle_event(event)
                delete_acc_button.handle_event(event)
                user_history.handle_event(event)
                password_delete.handle_event(event)
                new_change_password.handle_event(event)
                change_pass_button.handle_event(event)
                old_password.handle_event(event)
                clear_history_button.handle_event(event)
                if sign_out_button.pressed:
                    ui_state = 0
                if delete_acc_button.pressed:
                    df = login.Database("usernames.db")
                    if df.check_credentials(username, password_delete.user_text):
                        password = password_delete.user_text
                        delete = True

                    else:
                        delete = False
                        result = 6
                    password_delete.user_text = ''
                    df.close_database()
                if change_pass_button.pressed:
                    if is_password_valid(new_change_password.user_text):
                        df = login.Database("usernames.db")
                        if df.check_credentials(username, old_password.user_text):
                            df.change_password(username, new_change_password.user_text)
                            df.close_database()
                            old_password.user_text = ''
                            new_change_password.user_text = ''
                            ui_state = 0
                            result = 5
                        else:
                            result = 6
                    else:
                        result = 9
                if clear_history_button.pressed:
                    df = login.Database("usernames.db")
                    df.update_history(username, "")
                    user_history.lines = [""]
                    df.close_database()

                    result = 7
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change

                if delete:
                    yes_button.handle_event(event)
                    no_button.handle_event(event)
                    if yes_button.pressed:
                        df = login.Database("usernames.db")
                        df.delete_user(username, password)
                        ui_state = 0
                        result = 4
                        delete = False
                        df.close_database()
                        yes_button.pressed = False
                    if no_button.pressed:
                        delete = False
                        no_button.pressed = False

            # ALBUM INFO
            elif ui_state == 3:
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change
                album_info_box.handle_event(event)
            # ARTIST INFO
            elif ui_state == 4:
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change
                artist_bio_text.handle_event(event)
                similar_artists_text.handle_event(event)
                top_songs_text.handle_event(event)
            # SONG INFO
            elif ui_state == 5:
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change

                song_info_box.handle_event(event)
            # SIMILAR SONG
            elif ui_state == 6:
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change

                similar_text_box.handle_event(event)
                similar_enter_box.handle_event(event)
                if similar_enter_box.pressed and len(similar_text_box.user_text) != 0:
                    try:
                        similar_songs = dataGathering.Song(similar_text_box.user_text,"name").return_similar()
                        for count in range(len(song_boxes)):
                            current_song = similar_songs[count]
                            song_boxes[count].song_name.text = current_song.get_track_name()
                            song_boxes[count].artist_name.text = current_song.get_artist_name()
                            song_boxes[count].image = pygame.image.load(f"album{count+1}.png")
                            song_boxes[count].image = pygame.transform.scale(song_boxes[count].image,(100,100))
                            song_boxes[count].uri = current_song.get_track_id()
                            ui_state = 7
                    except:
                        result = 10
                else:
                    if similar_enter_box.pressed:
                        result = 11

            # SIMILAR RESULTS
            elif ui_state == 7:
                change = nav_bar.handle_event(event)
                if change is not None:
                    ui_state = change
                for song_box in song_boxes:
                    song_box.handle_event(event)
                    if song_box.next_button.pressed:
                            try:
                                music_data = dataGathering.Song(song_box.uri,"id")
                                song_bar_charts = [BarChart(400 - offsetx, 225 - offsety, 75, 100, 'Acousticness', maxes[0],
                                                            music_data.get_acousticness()),
                                                   BarChart(400 - offsetx, 375, 75, 100, 'Speechiness', maxes[1],
                                                            music_data.get_speechiness()),
                                                   BarChart(545 - offsetx, 225 - offsety, 75, 100, 'Loudness', maxes[2],
                                                            music_data.get_loudness() + 60),
                                                   BarChart(545 - offsetx, 375, 75, 100, 'Tempo', maxes[3],
                                                            music_data.get_tempo()),
                                                   BarChart(690 - offsetx, 225 - offsety, 75, 100, 'Valence', maxes[4],
                                                            music_data.get_valence()),
                                                   BarChart(690 - offsetx, 375, 75, 100, 'Instrumentalness', maxes[5],
                                                            music_data.get_instrumentalness()),
                                                   BarChart(835 - offsetx, 225 - offsety, 75, 100, 'Danceability', maxes[6],
                                                            music_data.get_danceability()),
                                                   BarChart(835 - offsetx, 375, 75, 100, 'Energy', maxes[7],
                                                            music_data.get_energy())]
                                song_name_text.text = music_data.get_track_name()
                                song_artist_text.text = music_data.get_artist_name()
                                song_info_box.lines = music_data.format_string_data()

                                try:
                                    music_data.get_album_image()
                                    image = pygame.image.load("album1.png")
                                except:
                                    image = pygame.image.load("noAlbumFound.png")

                                ui_state = 5
                            except: result = 10


            # -------------------------------------------

        screen.fill((125, 125, 125))

        # ------------------------------------------
        # LOGIN STATE
        if ui_state == 0:
            password_box.render_text()
            username_box.render_text()
            login_box.render_button()
            sign_up_box.render_button()


        # ENTER MUSIC SEARCH STATE
        elif ui_state == 1:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))

            box.render_text()
            dropdown.render_button()
            enter_box.render_button()
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[0].colour = (125, 125, 125)
            nav_bar.render_buttons()

        # ENTER USER SETTINGS STATE
        elif ui_state == 2:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            clear_history_button.render_button()
            sign_out_button.render_button()
            delete_acc_button.render_button()
            username_text.render_text()
            password_delete.render_text()
            new_change_password.render_text()
            change_pass_button.render_button()
            old_password.render_text()
            user_history_text.render_text()
            user_history.render()

            if delete:
                pygame.draw.rect(screen, (150, 150, 150), (250, 250, 250, 250))
                Text(250, 250, "Are you sure?", 40, 0, 0).render_text()
                yes_button.render_button()
                no_button.render_button()

            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[1].colour = (125, 125, 125)
            nav_bar.render_buttons()

        # ALBUM INFO STATE
        elif ui_state == 3:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[0].colour = (125, 125, 125)
            nav_bar.render_buttons()
            for i in bar_charts:
                i.render()

            album_name_text.text, album_artist_text.text = album_name, artist_name
            album_name_text.render_text()
            album_artist_text.render_text()

            pygame.draw.rect(screen, (100, 100, 100), (45, 45, 260, 260))
            image = pygame.image.load("image.png")
            image = pygame.transform.scale(image, (250, 250))
            screen.blit(image, (50, 50))
            album_info_box.render()
        # artist search screen
        elif ui_state == 4:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[0].colour = (125, 125, 125)
            nav_bar.render_buttons()

            artist_bio_text.render()
            artist_name_text.render_text()

            pygame.draw.rect(screen, (100, 100, 100), (15, 55, 155, 455))

            album1_img = pygame.image.load("album1.png")
            album2_img = pygame.image.load("album2.png")
            album3_img = pygame.image.load("album3.png")
            album1_img = pygame.transform.scale(album1_img, (145, 145))
            album2_img = pygame.transform.scale(album2_img, (145, 145))
            album3_img = pygame.transform.scale(album3_img, (145, 145))
            screen.blit(album1_img, (20, 60))
            screen.blit(album2_img, (20, 210))
            screen.blit(album3_img, (20, 360))

            top_songs_text.render()
            similar_artists_text.render()

        elif ui_state == 5:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[0].colour = (125, 125, 125)
            nav_bar.render_buttons()

            song_name_text.render_text()
            song_artist_text.render_text()
            for i in song_bar_charts:
                i.render()

            pygame.draw.rect(screen, (100, 100, 100), (45, 45, 210, 210))
            image = pygame.transform.scale(image, (200, 200))
            screen.blit(image, (50, 50))
            song_info_box.render()

        # FIND SIMILAR
        elif ui_state == 6:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[2].colour = (125, 125, 125)
            nav_bar.render_buttons()

            similar_enter_box.render_button()
            similar_text_box.render_text()

        elif ui_state == 7:
            pygame.draw.rect(screen, (100, 100, 100), (0, 0, 960, 40))
            for i in nav_bar.buttons:
                i.colour_change = False
                i.colour = (100, 100, 100)
            nav_bar.buttons[2].colour = (125, 125, 125)
            nav_bar.render_buttons()
            for song_box in song_boxes:
                song_box.render()
        elif ui_state == 8:
            screen.fill((100, 100, 100))
            not_connected.render_text()
            try:
                requests.get("http://www.google.com")
                ui_state = 0
            except:
                time.sleep(1)

        # Flash Text On Screen

        if result != 0 and login_result_timer < 60:
            match result:
                case 1:
                    display_text = "Incorrect Username or Password"
                case 2:
                    display_text = "Already Existing User"
                case 3:
                    display_text = "User Added"
                case 4:
                    display_text = "User Deleted"
                case 5:
                    display_text = "Changed Password"
                case 6:
                    display_text = "Incorrect Password"
                case 7:
                    display_text = "Cleared History"
                case 8:
                    display_text = "Username must contain valid character and atleast 4 characters"
                case 9:
                    display_text = "Password must contain valid character and atleast 4 characters"
                case 10:
                    display_text = "Error finding music"
                case 11:
                    display_text = "Must Enter Song"
                case 12:
                    display_text = "Must Enter characters into the text box"
                case _:
                    display_text = ""
            text_surface = base_font.render(display_text, True, (255, 255, 255))

            screen.blit(text_surface, (280, 375))
            login_result_timer += 1
            if login_result_timer == 60:
                login_result_timer = 0
                result = 0

        # -------------------------------------------

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()
