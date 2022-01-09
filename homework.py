from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.03f} ч.; '
                f'Дистанция: {self.distance:.03f} км; '
                f'Ср. скорость: {self.speed:.03f} км/ч; '
                f'Потрачено ккал: {self.calories:.03f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    action: int
    duration: float
    weight: float

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
        raise NotImplementedError('простой и понятный текст')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_object = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return info_object


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        K_1 = 18
        K_2 = 20
        mean_speed = self.get_mean_speed()
        spent_calories = ((K_1 * mean_speed - K_2)
                          * self.weight / self.M_IN_KM * self.duration * 60)
        return spent_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        K_1 = 0.035
        K_2 = 0.029
        mean_speed = self.get_mean_speed()
        spent_calories = ((K_1 * self.weight + (mean_speed ** 2 // self.height)
                          * K_2 * self.weight) * self.duration * 60)
        return spent_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

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
    dct = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    new_obj = dct[workout_type](*data)
    return new_obj


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
