import hashlib
import random


def generate_keys():
    # Вибір простого числа q
    q = get_prime_number()

    # Вибір t та простого числа p
    t = random.randint(0, 8)
    p = get_prime_number(lower_bound=2**(511 + 64*t), upper_bound=2**(512 + 64*t))

    # Вибір генератора g
    g = find_generator(p, q)

    # Вибір випадкового x
    x = random.randint(1, q-1)

    # Обчислення y
    y = pow(g, x, p)

    return p, q, g, y, x


def sign_message(message, p, q, g, y, x):
    # Вибір випадкового секретного числа k
    k = random.randint(1, q-1)

    # Обчислення r
    r = pow(g, k, p) % q

    # Обчислення k^-1
    k_inv = pow(k, -1, q)

    # Обчислення хешу повідомлення
    hashed_message = hashlib.sha256(message.encode()).digest()
    h = int.from_bytes(hashed_message, 'big')

    # Обчислення s
    s = (k_inv * (h + x*r)) % q

    if s == 0:
        # Якщо s = 0, повторити процес
        return sign_message(message, p, q, g, y, x)

    return r, s


def verify_signature(message, signature, p, q, g, y):
    r, s = signature

    if r < 0 or r > q or s < 0 or s > q:
        # Перевірка умов на r та s
        return False

    # Обчислення w
    w = pow(s, -1, q)

    # Обчислення хешу повідомлення
    hashed_message = hashlib.sha256(message.encode()).digest()
    h = int.from_bytes(hashed_message, 'big')

    # Обчислення u1 та u2
    u1 = (w * h) % q
    u2 = (w * r) % q

    # Обчислення v
    v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

    # Перевірка підпису
    if v == r:
        return False

    return True


def get_prime_number(lower_bound=2**159, upper_bound=2**160):
    # Генерація випадкового простого числа за допомогою random.getrandbits()
    number = random.getrandbits(160)
    number |= (1 << 159) | 1

    while not is_prime(number):
        number += 2

        if number > upper_bound:
            number = lower_bound

    return number


def is_prime(n, k=50):
    # Перевірка простоти числа за допомогою тесту Міллера-Рабіна
    if n <= 3:
        return n == 2 or n == 3

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                break
        else:
            return False

    return True


def find_generator(p, q):
    # Пошук генератора g
    for h in range(2, p-1):
        g = pow(h, (p-1)//q, p)

        if g != 1:
            return g

    return None


# Приклад використання

# Генерація ключів
p, q, g, y, x = generate_keys()

# Повідомлення для підпису
message = "Hello, world!"

# Підпис повідомлення
signature = sign_message(message, p, q, g, y, x)

# Перевірка підпису
is_valid = verify_signature(message, signature, p, q, g, y)

print("Підпис валідний:", is_valid)



"""Функція generate_keys() генерує ключі для алгоритму DSA. Вона вибирає просте число q та випадкові значення t та p,
 щоб задовольняти вказаним діапазонам. Далі, за допомогою функції find_generator(), знаходиться генератор g для циклічної 
 групи порядка q. Нарешті, вибирається випадкове секретне число x, і обчислюється публічний ключ y.

Функція sign_message(message, p, q, g, y, x) підписує повідомлення message за допомогою секретного ключа x. Вона генерує 
випадкове секретне число k та обчислює r і s згідно з формулами, наведеними в описі алгоритму. Якщо s дорівнює нулю, процес 
повторюється, оскільки це відповідає некоректному підпису. Повертається підпис у вигляді пари (r, s).

Функція verify_signature(message, signature, p, q, g, y) перевіряє підпис signature повідомлення message за допомогою 
публічного ключа (p, q, g, y). Вона перевіряє умови на r і s і обчислює значення w, u1, u2 та v згідно з формулами, 
наведеними в описі алгоритму. Якщо значення v дорівнює r, то підпис вважається валідним і повертається True, інакше 
повертається False.

Функція get_prime_number(lower_bound, upper_bound) генерує випадкове просте число у вказаному діапазоні. Вона використовує 
функцію is_prime(n, k), яка застосовує тест Міллера-Рабіна для перевірки простоти числа.

Функція is_prime(n, k) перевіряє, чи є число n простим, застосовуючи тест Міллера-Рабіна. Вона перевіряє кілька випадкових 
свідків, щоб визначити ймовірність простоти числа.

Функція find_generator(p, q) знаходить генератор g для циклічної групи порядка q в полі Zp. Вона перебирає значення h 
від 2 до p-1 і обчислює g згідно з формулою, наведеною в описі алгоритму."""