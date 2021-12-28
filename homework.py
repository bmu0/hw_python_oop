class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.03f} ч.; '
                f'Дистанция: {self.distance:.03f} км; '
                f'Ср. скорость: {self.speed:.03f} км/ч; '
                f'Потрачено ккал: {self.calories:.03f}.')
        pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_object = (InfoMessage(self.__class__.__name__, self.duration,
                       self.get_distance(), self.get_mean_speed(),
                       self.get_spent_calories()))
        return info_object


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        K_1 = 18
        K_2 = 20
        mean_speed = self.get_mean_speed()
        spent_calories = ((K_1 * mean_speed - K_2)
                          * self.weight / self.M_IN_KM * self.duration * 60)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.M_IN_KM = 1000

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        K_1 = 0.035
        K_2 = 0.029
        mean_speed = self.get_mean_speed()
        spent_calories = ((K_1 * self.weight + (mean_speed ** 2 // self.height)
                          * K_2 * self.weight) * self.duration * 60)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.M_IN_KM = 1000

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        K_1 = 1.1
        K_2 = 2
        mean_speed = self.get_mean_speed()
        spent_calories = (mean_speed + K_1) * K_2 * self.weight
        return spent_calories

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM' and len(data) == 5:
        new_obj = Swimming(data[0], data[1], data[2], data[3], data[4])
    if workout_type == 'RUN' and len(data) == 3:
        new_obj = Running(data[0], data[1], data[2])
    if workout_type == 'WLK' and len(data) == 4:
        new_obj = SportsWalking(data[0], data[1], data[2], data[3])
    return new_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
