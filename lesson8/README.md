# lesson8

*Эти задания должны быть выполнены с использованием TDD*

**Прежде чем начать:**
- **Постарайтесь не читать задания наперед.**
- **Делайте по одной задаче за раз.**

Все тесты должны проходить, вне зависимости от свойств окружения
1. Напишите класс Greeter с функцией greet которая получает имя на входе и возвращает строку “Привет <name>”. Параметры метода не должны меняться на протяжении всего упражнения. Структуру класса Greeter вы можете задать по своему усмотрению.
1. greet обрезает пробелы до и после ввода
1. greet конвертирует строку в начинающуюся с большой буквы
1. greet возвращает “Доброе утро <name>” когда текущее время 06:00-12:00
1. greet возвращает “Добрый вечер <name>” когда текущее время 18:00-22:00
1. greet возвращает “Доброй ночи <name>” когда текущее время 22:00-06:00
1. greet пишет лог каждый раз когда вызывается