import hashlib
import time

class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    @staticmethod
    def hash_password(password):
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __str__(self):
        return f"User(nickname='{self.nickname}', age={self.age})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, User) and self.nickname == other.nickname


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __str__(self):
        return f"Video(title='{self.title}', duration={self.duration}, adult_mode={self.adult_mode})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Video) and self.title == other.title


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        hashed_password = User.hash_password(password)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                print(f"Добро пожаловать, {nickname}!")
                return
        print("Неправильный логин или пароль")

    def register(self, nickname, password, age):
        for user in self.users:
            if user.nickname == nickname:
                print(f"Пользователь {nickname} уже существует")
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user
        print(f"Пользователь {nickname} успешно зарегистрирован и вошёл в систему")

    def log_out(self):
        if self.current_user:
            print(f"До свидания, {self.current_user.nickname}!")
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if video not in self.videos:
                self.videos.append(video)

    def get_videos(self, keyword):
        keyword = keyword.lower()
        return [video.title for video in self.videos if keyword in video.title.lower()]

    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу")
                    return

                print(f"Начинаем просмотр: {video.title}")
                for second in range(video.time_now + 1, video.duration + 1):
                    print(second, end=" ")
                    time.sleep(0.1)  # Уменьшено для удобства
                print("\nКонец видео")
                video.time_now = 0
                return

        print("Видео не найдено")

    def __str__(self):
        return f"UrTube(current_user={self.current_user}, users={len(self.users)}, videos={len(self.videos)})"


# Проверка
ur = UrTube()

v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')

ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')

ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
